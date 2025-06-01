from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import uuid
from datetime import datetime

# 导入自定义模块
from config import settings
from database import get_db
from models import User, Task, Style, Credit
from auth import get_current_user, create_access_token
from openai_service import generate_image
from dao.user_dao import UserDAO
from dao.style_dao import get_styles, create_style, get_style_categories
from dao.task_dao import create_task, get_task_by_id, update_task_status
from dao.credit_dao import get_credit_by_user_id, create_credit, update_credit_amount
from wechat_service import get_wechat_session

# 创建FastAPI应用
app = FastAPI(title="Pictora API", description="AI图片生成应用的后端API")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该限制为前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建上传目录
os.makedirs("uploads", exist_ok=True)
os.makedirs("results", exist_ok=True)

# 挂载静态文件目录
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/results", StaticFiles(directory="results"), name="results")

# 请求模型
class StyleRequest(BaseModel):
    name: str
    description: Optional[str] = None
    prompt_template: str
    preview_image: Optional[str] = None
    category: Optional[str] = None
    popular: int = 0

class TaskRequest(BaseModel):
    style_id: str
    custom_prompt: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    password: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str

# 路由
@app.get("/")
async def read_root():
    return {"message": "欢迎使用Pictora AI图片生成API"}

# 用户相关路由
@app.post("/users/register")
async def register_user(user: UserCreate, db=Depends(get_db)):
    # 检查用户名是否已存在
    existing_user = await UserDAO.get_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    # 创建新用户
    new_user = User.create(user.username, user.password, user.email)
    result = await UserDAO.create(db, new_user)
    # 为新用户创建初始积分
    initial_credit = Credit(user_id=str(result.id), amount=10, is_vip=False)
    await create_credit(db, initial_credit)
    return {"message": "注册成功", "user_id": str(result.id)}

@app.post("/users/login")
async def login_user(code: str, db=Depends(get_db)):
    # Get WeChat session info using the code
    try:
        wx_session = await get_wechat_session(code)
        openid = wx_session.get('openid')
        session_key = wx_session.get('session_key')
        
        if not openid:
            raise HTTPException(status_code=400, detail="Invalid WeChat code")
            
        # Check if user exists, if not create new user
        db_user = await UserDAO.get_by_openid(db, openid)
        if not db_user:
            # Create new user with WeChat openid
            new_user = User.create_wechat_user(openid)
            db_user = await UserDAO.create(db, new_user)
            # Create initial credits for new user
            initial_credit = Credit(user_id=str(db_user.id), amount=10, is_vip=False)
            await create_credit(db, initial_credit)
            
        # Generate access token
        access_token = create_access_token(data={
            "sub": str(db_user.id),
            "openid": openid,
            "session_key": session_key
        })
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "is_new_user": db_user.is_new if hasattr(db_user, 'is_new') else False
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"WeChat login failed: {str(e)}")

@app.get("/users/me")
async def get_user_profile(current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    # 获取用户积分信息
    credit_info = await get_credit_by_user_id(db, current_user["id"])
    return {
        "username": current_user["username"],
        "email": current_user["email"],
        "credits": credit_info.amount if credit_info else 0,
        "is_vip": credit_info.is_vip if credit_info else False
    }

# 风格效果相关路由
@app.get("/styles")
async def get_styles_route(category_id: Optional[int] = None, limit: int = 10, offset: int = 0, db=Depends(get_db)):
    styles = await get_styles(db, category_id, limit, offset)
    return styles

@app.get("/styles/recent")
async def get_recent_styles_route(current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    styles = await get_user_recent_styles(db, current_user.id)
    return styles

@app.post("/styles", status_code=status.HTTP_201_CREATED)
async def create_style_route(style: StyleRequest, db=Depends(get_db), current_user: dict = Depends(get_current_user)):
    if not current_user.get("is_admin", False):
        raise HTTPException(status_code=403, detail="只有管理员可以创建风格")
    new_style = Style(
        name=style.name,
        description=style.description,
        prompt_template=style.prompt_template,
        preview_image=style.preview_image,
        category=style.category,
        is_popular=style.is_popular
    )
    result = await create_style(db, new_style)
    return {"id": str(result.id), **new_style.dict()}

# 图片生成任务相关路由
@app.post("/tasks")
async def create_task(
    task: TaskRequest,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db=Depends(get_db)
):
    # 检查用户积分
    credit_info = await db.credits.find_one({"user_id": current_user["_id"]})
    if not credit_info or credit_info["amount"] <= 0:
        raise HTTPException(status_code=402, detail="积分不足，请充值")
    
    # 获取选择的风格
    style = await db.styles.find_one({"_id": task.style_id})
    if not style:
        raise HTTPException(status_code=404, detail="风格不存在")
    
    # 保存上传的图片
    file_extension = os.path.splitext(file.filename)[1]
    file_name = f"{uuid.uuid4()}{file_extension}"
    file_path = f"uploads/{file_name}"
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # 创建任务
    new_task = Task(
        user_id=current_user["_id"],
        style_id=task.style_id,
        input_image=file_path,
        custom_prompt=task.custom_prompt,
        status="pending",
        created_at=datetime.now()
    )
    
    result = await db.tasks.insert_one(new_task.dict())
    task_id = str(result.inserted_id)
    
    # 扣减积分
    await db.credits.update_one(
        {"user_id": current_user["_id"]},
        {"$inc": {"amount": -1}}
    )
    
    # 异步处理图片生成（实际项目中应该使用消息队列或后台任务）
    # 这里简化处理，直接调用OpenAI API
    try:
        # 构建完整提示词
        prompt = style["prompt_template"]
        if task.custom_prompt:
            prompt += f" {task.custom_prompt}"
        
        # 调用OpenAI生成图片
        result_image_path = await generate_image(file_path, prompt, task_id)
        
        # 更新任务状态
        await db.tasks.update_one(
            {"_id": task_id},
            {"$set": {"status": "completed", "output_image": result_image_path}}
        )
        
        return {"task_id": task_id, "status": "completed", "message": "图片生成成功"}
    except Exception as e:
        # 更新任务状态为失败
        await db.tasks.update_one(
            {"_id": task_id},
            {"$set": {"status": "failed", "error": str(e)}}
        )
        return {"task_id": task_id, "status": "failed", "message": str(e)}

@app.get("/tasks")
async def get_user_tasks(status: Optional[str] = None, current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    # 构建查询条件
    query = {"user_id": current_user["_id"]}
    if status:
        query["status"] = status
    
    # 查询用户任务
    tasks = await db.tasks.find(query).sort("created_at", -1).to_list(50)
    return tasks

@app.get("/tasks/{task_id}")
async def get_task(task_id: str, current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    # 查询任务
    task = await db.tasks.find_one({"_id": task_id, "user_id": current_user["_id"]})
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在或无权访问")
    
    return task

@app.post("/tasks/{task_id}/retry")
async def retry_task(task_id: str, current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    # 查询任务
    task = await db.tasks.find_one({"_id": task_id, "user_id": current_user["_id"]})
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在或无权访问")
    
    if task["status"] != "failed":
        raise HTTPException(status_code=400, detail="只能重试失败的任务")
    
    # 检查用户积分
    credit_info = await db.credits.find_one({"user_id": current_user["_id"]})
    if not credit_info or credit_info["amount"] <= 0:
        raise HTTPException(status_code=402, detail="积分不足，请充值")
    
    # 获取风格
    style = await db.styles.find_one({"_id": task["style_id"]})
    if not style:
        raise HTTPException(status_code=404, detail="风格不存在")
    
    # 更新任务状态
    await db.tasks.update_one(
        {"_id": task_id},
        {"$set": {"status": "pending", "error": None}}
    )
    
    # 扣减积分
    await db.credits.update_one(
        {"user_id": current_user["_id"]},
        {"$inc": {"amount": -1}}
    )
    
    # 重新生成图片
    try:
        # 构建完整提示词
        prompt = style["prompt_template"]
        if task["custom_prompt"]:
            prompt += f" {task['custom_prompt']}"
        
        # 调用OpenAI生成图片
        result_image_path = await generate_image(task["input_image"], prompt, task_id)
        
        # 更新任务状态
        await db.tasks.update_one(
            {"_id": task_id},
            {"$set": {"status": "completed", "output_image": result_image_path}}
        )
        
        return {"task_id": task_id, "status": "completed", "message": "图片重新生成成功"}
    except Exception as e:
        # 更新任务状态为失败
        await db.tasks.update_one(
            {"_id": task_id},
            {"$set": {"status": "failed", "error": str(e)}}
        )
        return {"task_id": task_id, "status": "failed", "message": str(e)}

# VIP相关路由
@app.post("/vip/subscribe")
async def subscribe_vip(current_user: dict = Depends(get_current_user), db=Depends(get_db)):
    # 在实际项目中，这里应该有支付逻辑
    # 这里简化处理，直接将用户设为VIP并增加积分
    
    await db.credits.update_one(
        {"user_id": current_user["_id"]},
        {"$set": {"is_vip": True}, "$inc": {"amount": 100}}
    )
    
    return {"message": "VIP订阅成功，已增加100积分"}

# 启动服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

@app.get("/styles/categories")
async def get_style_categories_route(limit: int = 10, offset: int = 0, db=Depends(get_db)):
    categories = await get_style_categories(db, limit, offset)
    return categories
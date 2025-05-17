import os
import aiohttp
import base64
from config import settings

async def generate_image(input_image_path: str, prompt: str, task_id: str) -> str:
    """使用OpenAI API生成图片
    
    Args:
        input_image_path: 输入图片路径
        prompt: 提示词
        task_id: 任务ID
        
    Returns:
        str: 生成的图片路径
    """
    # 读取输入图片并转换为base64
    with open(input_image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    # 准备API请求
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}"
    }
    
    payload = {
        "model": "dall-e-3",  # 使用DALL-E 3模型
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024",
        "response_format": "b64_json"
    }
    
    # 如果有输入图片，添加到请求中
    if base64_image:
        payload["image"] = base64_image
    
    # 调用OpenAI API
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.openai.com/v1/images/generations",
                headers=headers,
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"OpenAI API错误: {error_text}")
                
                result = await response.json()
                
                # 解析结果
                image_data = base64.b64decode(result["data"][0]["b64_json"])
                
                # 保存生成的图片
                result_path = f"results/{task_id}.png"
                with open(result_path, "wb") as f:
                    f.write(image_data)
                
                return result_path
    except Exception as e:
        raise Exception(f"图片生成失败: {str(e)}")
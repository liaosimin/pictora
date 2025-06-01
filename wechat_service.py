import aiohttp
from config import settings

async def get_wechat_session(code: str) -> dict:
    """获取微信小程序会话信息"""
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    params = {
        'appid': settings.WECHAT_APP_ID,
        'secret': settings.WECHAT_APP_SECRET,
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                if 'errcode' in data and data['errcode'] != 0:
                    raise Exception(f"WeChat API error: {data['errmsg']}")
                return data
            else:
                raise Exception(f"WeChat API request failed with status {response.status}")
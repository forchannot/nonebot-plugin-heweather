import base64
import re
from io import BytesIO

from nonebot import on_regex
from nonebot.adapters.cqhttp import Bot, Message, MessageEvent, MessageSegment

from .convrt_pic import *
from .get_weather import *

weather = on_regex(r".*?(.*)天气.*?", priority=1)


def img_to_b64(pic: Image.Image) -> str:
    buf = BytesIO()
    pic.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    return "base64://" + base64_str


def get_msg(msg) -> str:
    msg1 = re.search(r".*?(.*)天气.*?", msg)
    msg2 = re.search(r".*?天气(.*).*?", msg)
    msg1 = msg1.group(1).replace(" ", "")
    msg2 = msg2.group(1).replace(" ", "")
    msg = msg1 if msg1 else msg2

    return msg


@weather.handle()
async def _(bot: Bot, event: MessageEvent):
    city = get_msg(event.get_plaintext())
    if city:
        try:
            data = await get_City_Weather(city)
        except KeyError:
            await weather.finish("这个地方不在天气数据库中哦 >_<")
        img = draw(data)
        b64 = img_to_b64(img)
        await weather.finish(MessageSegment.image(b64))
    else:
        await weather.finish("地点是...空气吗?? >_<")

from typing import Optional

import telegram
import asyncio

bot = telegram.Bot(token='6449437431:AAHcRsW40265UtbWiWGSTKsfSry6jovizPU')
channel_id = '591524139'


async def safety_eye_pro_alert(text: Optional[str] = None, video_path: Optional[str] = None, img_path: Optional[str] = None):
    # Send a text message
    await bot.send_message(chat_id=channel_id, text=text)
    await bot.send_photo(chat_id=channel_id, photo=open("D:\\lableingSilryuk.png",'rb'))
    await bot.send_video(chat_id=channel_id, video=open('D:\\test.mp4', 'rb'))
    return ("success")


async def send_text(text: str):
    # Send a text message
    await bot.send_message(chat_id=channel_id, text=text)
    return ("success")


if __name__ == "__main__":
    asyncio.run(safety_eye_pro_alert("this is garry's test."))

# # Send a photo
# bot.send_photo(chat_id=channel_id, photo=open('/path/to/photo.jpg', 'rb'))
#
# # Send a vide
# bot.send_video(chat_id=channel_id, video=open('/path/to/video.mp4', 'rb'))
#
# # Send a document
# bot.send_document(chat_id=channel_id, document=open('/path/to/document.pdf', 'rb'))

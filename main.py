from pyrogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
import os, pyrogram, json
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from requests import get
import logging
import asyncio

logging.basicConfig(level=logging.INFO)

# conifg
with open('config.json', 'r') as f: CONFIGDATA = json.load(f)

# app
TOKEN = os.environ.get("TOKEN") or CONFIGDATA.get("TOKEN", "")
HASH = os.environ.get("HASH") or CONFIGDATA.get("HASH", "")
ID = os.environ.get("ID") or CONFIGDATA.get("ID", "")
fsub_id = os.environ.get('FSUB_ID', '-1001678093514')
if len(fsub_id) == 0:
    logging.error("FSUB_ID variable is missing! Exiting now")
    exit(1)
else:
    fsub_id = int(fsub_id)

fsub_id2 = os.environ.get('FSUB_ID2', '-1001855342933')
if len(fsub_id2) == 0:
    logging.error("FSUB_ID2 variable is missing! Exiting now")
    exit(1)
else:
    fsub_id2 = int(fsub_id2)
app = Client("my_bot", api_id=ID, api_hash=HASH, bot_token=TOKEN)

# channles
CHANNELS = get("https://iptv-org.github.io/api/channels.json").json()
print("Total Channels:",len(CHANNELS))
CHANNELS_BY_ID = {channel.get("id","None"): channel for channel in CHANNELS}

# refresh
def refresh():
    streams = get("https://iptv-org.github.io/api/streams.json").json()
    online = []
    for stream in streams: 
        if stream.get("status","online") == "online" and stream.get("channel",None) is not None:
            channel_id = stream["channel"]
            if channel_id in CHANNELS_BY_ID.keys():
                channel = CHANNELS_BY_ID[channel_id]
                stream["name"] = channel["name"]
            online.append(stream)
    print("Total Streams:",len(online))
    return online

# streams
STREAM_LINK = os.environ.get("STREAM") or CONFIGDATA.get("STREAM", "")
STREAMS = refresh()

# settings
COLMS = 2
ROWS = 15

async def is_user_member(client, user_id):
    try:
        member = await client.get_chat_member(fsub_id, user_id)
        member = await client.get_chat_member(fsub_id2, user_id)
        logging.info(f"User {user_id} membership status: {member.status}")
        if member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"Error checking membership status for user {user_id}: {e}")
        return False
@app.on_message(filters.command(["start"]))
async def echo(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    user_mention = message.from_user.mention
    is_member = await is_user_member(client, user_id)
    
    join_button = InlineKeyboardButton("ᴊᴏɪɴ ❤️🚀", url="https://t.me/movie_time_botonly")
    developer_button = InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ ⚡️", url="https://t.me/fligher")
    bt_button=InlineKeyboardButton("Bot List🤖",url="https://te.legra.ph/TRUMBOTS-BOTS-LIST-06-01")
    reply_markup = InlineKeyboardMarkup([[join_button, developer_button],[bt_button]])

    
    if not is_member:
        join_button1 = InlineKeyboardButton("CHANNEL 1", url="https://t.me/movie_time_botonly")
        join_button2 = InlineKeyboardButton("CHANNEL 2", url="https://t.me/+ExBm8lEipxRkMTA1")
        reply_markup = InlineKeyboardMarkup([[join_button1],[join_button2]])
        await message.reply_text("😈ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴍʏ ᴄʜᴀɴɴᴇʟs ᴛᴏ ᴜsᴇ ᴍᴇ😈.", reply_markup=reply_markup)
        return

    
    await app.send_message(message.chat.id,
        f"__Hello {message.from_user.mention},\nWatch IPTV streams right in Telegram App, send name of the channel bot will respond with available streams to watch,\nThere are 6000+ online streams available from all over the world all the time.Based in your area it will work.", reply_to_message_id=message.id, disable_web_page_preview=True, reply_markup=reply_markup)

@app.on_message(filters.command(["about"]))
async def about_command(client,message):
    text = f"""
🌀 ᴄʜᴀɴɴᴇʟ : <a href="https://t.me/MOVIE_Time_BotOnly">​🇹​​🇷​​🇺​​🇲​​🇧​​🇴​​🇹​​🇸</a>
🌺 ʜᴇʀᴏᴋᴜ : <a href="https://heroku.com/">ʜᴇʀᴏᴋᴜ</a>
📑 ʟᴀɴɢᴜᴀɢᴇ : <a href="https://www.python.org/">ᴘʏᴛʜᴏɴ 3.10.5</a>
🇵🇲 ғʀᴀᴍᴇᴡᴏʀᴋ : <a href="https://docs.pyrogram.org/">ᴘʏʀᴏɢʀᴀᴍ 2.0.30</a>
👲 ᴅᴇᴠᴇʟᴏᴘᴇʀ : <a href="https://t.me/fligher">​🇲​​🇾​​🇸​​🇹​​🇪​​🇷​​🇮​​🇴​</a></b>
"""

    # Buttons
    buttons = [
        [
            InlineKeyboardButton('👥 Group', url=f"https://t.me/trumbotchat"),
            InlineKeyboardButton('TRUMBOTS', url=f"https://t.me/movie_time_botonly")
            ],[
            InlineKeyboardButton('❤️Me', url=f"https://t.me/fligher"),
            InlineKeyboardButton('Bot Lists 🤖', url=f"https://te.legra.ph/TRUMBOTS-BOTS-LIST-06-01"),
            ]
    ]
    x=await message.reply_photo(
        photo="https://th.bing.com/th/id/OIG4.kIKwAP6q4rN21rOhb71Z?pid=ImgGn",
        caption=text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    await asyncio.sleep(10)
    await message.delete()
    await x.delete()

# text
@app.on_message(filters.text)
async def tvname(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    user_mention = message.from_user.mention
    search = message.text
    is_member = await is_user_member(client, user_id)
    
    if not is_member:
        join_button1 = InlineKeyboardButton("CHANNEL 1", url="https://t.me/movie_time_botonly")
        join_button2 = InlineKeyboardButton("CHANNEL 2", url="https://t.me/+ExBm8lEipxRkMTA1")
        reply_markup = InlineKeyboardMarkup([[join_button1],[join_button2]])
        await message.reply_text("😈ʏᴏᴜ ᴍᴜsᴛ ᴊᴏɪɴ ᴍʏ ᴄʜᴀɴɴᴇʟs ᴛᴏ ᴜsᴇ ᴍᴇ😈.", reply_markup=reply_markup)
        return
    
    


    tvs = [InlineKeyboardButton(text = x.get("name",x["channel"]),
                                web_app=WebAppInfo(url = STREAM_LINK + "?url=" + x["url"]))
                                for x in STREAMS if search.lower() in x.get("name",x["channel"]).lower()]
    
    print("Total Results for",search,"is",len(tvs))
    if len(tvs) == 0:
       await app.send_message(message.chat.id,"No Results Found",reply_to_message_id=message.id)
        return
    
    main = []
    for i in range(0, len(tvs), COLMS): main.append(tvs[i:i+COLMS])
    
    await app.send_message(message.chat.id, '__Click on any one Channel__',
    reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(main[:ROWS]))


# infinty polling
app.run()

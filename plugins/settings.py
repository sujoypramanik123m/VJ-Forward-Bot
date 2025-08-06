# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import asyncio 
from database import Db, db
from script import Script
from pyrogram import Client, filters
from .test import get_configs, update_configs, CLIENT, parse_buttons
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .db import connect_user_db

CLIENT = CLIENT()

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_message(filters.command('settings'))
async def settings(client, message):
   await message.reply_text(
     "<b>Hᴇʀᴇ Is Tʜᴇ Sᴇᴛᴛɪɴɢs Pᴀɴᴇʟ⚙\n\nᴄʜᴀɴɢᴇ ʏᴏᴜʀ sᴇᴛᴛɪɴɢs ᴀs ʏᴏᴜʀ ᴡɪsʜ 👇</b>",
     reply_markup=main_buttons()
     )

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

@Client.on_callback_query(filters.regex(r'^settings'))
async def settings_query(bot, query):
  user_id = query.from_user.id
  i, type = query.data.split("#")
  buttons = [[InlineKeyboardButton('back', callback_data="settings#main")]]
  if type=="main":
     await query.message.edit_text(
       "<b>Hᴇʀᴇ Is Tʜᴇ Sᴇᴛᴛɪɴɢs Pᴀɴᴇʟ⚙\n\nᴄʜᴀɴɢᴇ ʏᴏᴜʀ sᴇᴛᴛɪɴɢs ᴀs ʏᴏᴜʀ ᴡɪsʜ 👇</b>",
       reply_markup=main_buttons())
  elif type=="extra":
       await query.message.edit_text(
         "<b>Hᴇʀᴇ Is Tʜᴇ Exᴛʀᴀ Sᴇᴛᴛɪɴɢs Pᴀɴᴇʟ⚙</b>",
         reply_markup=extra_buttons())
  elif type=="bots":
     buttons = [] 
     _bot = await db.get_bot(user_id)
     usr_bot = await db.get_userbot(user_id)
     if _bot is not None:
        buttons.append([InlineKeyboardButton(_bot['name'],
                         callback_data=f"settings#editbot")])
     else:
        buttons.append([InlineKeyboardButton('✚ Add bot ✚', 
                         callback_data="settings#addbot")])
     if usr_bot is not None:
        buttons.append([InlineKeyboardButton(usr_bot['name'],
                         callback_data=f"settings#edituserbot")])
     else:
        buttons.append([InlineKeyboardButton('✚ Add User bot ✚', 
                         callback_data="settings#adduserbot")])
     buttons.append([InlineKeyboardButton('back', 
                      callback_data="settings#main")])
     await query.message.edit_text(
       "<b><u>My Bots</b></u>\n\n<b>You can manage your bots in here</b>",
       reply_markup=InlineKeyboardMarkup(buttons))

  elif type=="addbot":
     await query.message.delete()
     bot = await CLIENT.add_bot(bot, query)
     if bot != True: return
     await query.message.reply_text(
        "<b>bot token successfully added to db</b>",
        reply_markup=InlineKeyboardMarkup(buttons))

  elif type=="adduserbot":
     await query.message.delete()
     user = await CLIENT.add_session(bot, query)
     if user != True: return
     await query.message.reply_text(
        "<b>session successfully added to db</b>",
        reply_markup=InlineKeyboardMarkup(buttons))

  elif type=="channels":
     buttons = []
     channels = await db.get_user_channels(user_id)
     for channel in channels:
        buttons.append([InlineKeyboardButton(f"{channel['title']}",
                         callback_data=f"settings#editchannels_{channel['chat_id']}")])
     buttons.append([InlineKeyboardButton('✚ Add Channel ✚', 
                      callback_data="settings#addchannel")])
     buttons.append([InlineKeyboardButton('back', 
                      callback_data="settings#main")])
     await query.message.edit_text( 
       "<b><u>My Channels</b></u>\n\n<b>you can manage your target chats in here</b>",
       reply_markup=InlineKeyboardMarkup(buttons))

  elif type=="addchannel":  
     await query.message.delete()
     chat_ids = await bot.ask(chat_id=query.from_user.id, text="<b>❪ SET TARGET CHAT ❫\n\nForward a message from Your target chat\n/cancel - cancel this process</b>")
     if chat_ids.text=="/cancel":
        return await chat_ids.reply_text(
                  "<b>process canceled</b>",
                  reply_markup=InlineKeyboardMarkup(buttons))
     elif not chat_ids.forward_date:
        return await chat_ids.reply("**This is not a forward message**")
     else:
        chat_id = chat_ids.forward_from_chat.id
        title = chat_ids.forward_from_chat.title
        username = chat_ids.forward_from_chat.username
        username = "@" + username if username else "private"
     chat = await db.add_channel(user_id, chat_id, title, username)
     await query.message.reply_text(
        "<b>Successfully updated</b>" if chat else "<b>This channel already added</b>",
        reply_markup=InlineKeyboardMarkup(buttons))

  elif type=="editbot": 
     bot = await db.get_bot(user_id)
     TEXT = Script.BOT_DETAILS if bot['is_bot'] else Script.USER_DETAILS
     buttons = [[InlineKeyboardButton('❌ Remove ❌', callback_data=f"settings#removebot")
               ],
               [InlineKeyboardButton('back', callback_data="settings#bots")]]
     await query.message.edit_text(
        TEXT.format(bot['name'], bot['id'], bot['username']),
        reply_markup=InlineKeyboardMarkup(buttons))
     
  elif type=="edituserbot": 
     bot = await db.get_userbot(user_id)
     TEXT = Script.USER_DETAILS
     buttons = [[InlineKeyboardButton('❌ Remove ❌', callback_data=f"settings#removeuserbot")
               ],
               [InlineKeyboardButton('back', callback_data="settings#bots")]]
     await query.message.edit_text(
        TEXT.format(bot['name'], bot['id'], bot['username']),
        reply_markup=InlineKeyboardMarkup(buttons))
     
  elif type=="removebot":
     await db.remove_bot(user_id)
     await query.message.edit_text(
        "<b>successfully updated</b>",
        reply_markup=InlineKeyboardMarkup(buttons))
     
  elif type=="removeuserbot":
     await db.remove_userbot(user_id)
     await query.message.edit_text(
        "<b>successfully updated</b>",
        reply_markup=InlineKeyboardMarkup(buttons))
     
  elif type.startswith("editchannels"): 
     chat_id = type.split('_')[1]
     chat = await db.get_channel_details(user_id, chat_id)
     buttons = [[InlineKeyboardButton('❌ Remove ❌', callback_data=f"settings#removechannel_{chat_id}")
               ],
               [InlineKeyboardButton('back', callback_data="settings#channels")]]
     await query.message.edit_text(
        f"<b><u>📄 CHANNEL DETAILS</b></u>\n\n<b>- TITLE:</b> <code>{chat['title']}</code>\n<b>- CHANNEL ID: </b> <code>{chat['chat_id']}</code>\n<b>- USERNAME:</b> {chat['username']}",
        reply_markup=InlineKeyboardMarkup(buttons))

  elif type.startswith("removechannel"):
     chat_id = type.split('_')[1]
     await db.remove_channel(user_id, chat_id)
     await query.message.edit_text(
        "<b>successfully updated</b>",
        reply_markup=InlineKeyboardMarkup(buttons))

  elif type=="caption":
     buttons = []
     data = await get_configs(user_id)
     caption = data['caption']
     if caption is None:
        buttons.append([InlineKeyboardButton('✚ Add Caption ✚', 
                      callback_data="settings#addcaption")])
     else:
        buttons.append([InlineKeyboardButton('See Caption', 
                      callback_data="settings#seecaption")])
        buttons[-1].append(InlineKeyboardButton('🗑️ Delete Caption', 
                      callback_data="settings#deletecaption"))
     buttons.append([InlineKeyboardButton('back', 
                      callback_data="settings#main")])
     await query.message.edit_text(
        "<b><u>CUSTOM CAPTION</b></u>\n\n<b>You can set a custom caption to videos and documents. Normaly use its default caption</b>\n\n<b><u>AVAILABLE FILLINGS:</b></u>\n- <code>{filename}</code> : Filename\n- <code>{size}</code> : File size\n- <code>{caption}</code> : default caption",
        reply_markup=InlineKeyboardMarkup(buttons))

  elif type=="seecaption":   
     data = await get_configs(user_id)
     buttons = [[InlineKeyboardButton('🖋️ Edit Caption', 
                  callback_data="settings#addcaption")
               ],[
               InlineKeyboardButton('back', 
                 callback_data="settings#caption")]]
     await query.message.edit_text(
        f"<b><u>YOUR CUSTOM CAPTION</b></u>\n\n<code>{data['caption']}</code>",
        reply_markup=InlineKeyboardMarkup(buttons))

  elif type=="deletecaption":
     await update_configs(user_id, 'caption', None)
     await query.message.edit_text(
        "<b>successfully updated</b>",
        reply_markup=InlineKeyboardMarkup(buttons))

  elif type=="addcaption":
     await query.message.delete()
     caption = await bot.ask(query.message.chat.id, "Send your custom caption\n/cancel - <code>cancel this process</code>")
     if caption.text=="/cancel":
        return await caption.reply_text(
                  "<b>process canceled !</b>",
                  reply_markup=InlineKeyboardMarkup(buttons))
     try:
         caption.text.format(filename='', size='', caption='')
     except KeyError as e:
         return await caption.reply_text(
            f"<b>wrong filling {e} used in your caption. change it</b>",
            reply_markup=InlineKeyboardMarkup(buttons))
     await update_configs(user_id, 'caption', caption.text)
     await caption.reply_text(
        "<b>successfully updated</b>",
        reply_markup=InlineKeyboardMarkup(buttons))

  elif type=="button":
     buttons = []
     button = (await get_configs(user_id))['button']
     if button is None:
        buttons.append([InlineKeyboardButton('✚ Add Button ✚', 
                      callback_data="settings#addbutton")])
     else:
        buttons.append([InlineKeyboardButton('👀 See Button', 
                      callback_data="settings#seebutton")])
        buttons[-1].append(InlineKeyboardButton('🗑️ Remove Button ', 
                      callback_data="settings#deletebutton"))
     buttons.append([InlineKeyboardButton('back', 
                      callback_data="settings#main")])
     await query.message.edit_text(
        "<b><u>CUSTOM BUTTON</b></u>\n\n<b>You can set a inline button to messages.</b>\n\n<b><u>FORMAT:</b></u>\n`[Forward bot][buttonurl:https://t.me/mychannelurl]`\n",
        reply_markup=InlineKeyboardMarkup(buttons))

  elif type=="addbutton":
     await query.message.delete()
     ask = await bot.ask(user_id, text="**Send your custom button.\n\nFORMAT:**\n`[forward bot][buttonurl:https://t.me/url]`\n")
     button = parse_buttons(ask.text.html)
     if not button:
        return await ask.reply("**INVALID BUTTON**")
     await update_configs(user_id, 'button', ask.text.html)
     await ask.reply("**Successfully button added**",
             reply_markup=InlineKeyboardMarkup(buttons))

  elif type=="seebutton":
      button = (await get_configs(user_id))['button']
      button = parse_buttons(button, markup=False)
      button.append([InlineKeyboardButton("back", "settings#button")])
      await query.message.edit_text(
         "**YOUR CUSTOM BUTTON**",
         reply_markup=InlineKeyboardMarkup(button))

  elif type=="deletebutton":
     await update_configs(user_id, 'button', None)
     await query.message.edit_text(
        "**Successfully button deleted**",
        reply_markup=InlineKeyboardMarkup(buttons))

  elif type=="database":
     buttons = []
     db_uri = (await get_configs(user_id))['db_uri']
     if db_uri is None:
        buttons.append([InlineKeyboardButton('✚ Add Mongo Url ', 
                      callback_data="settings#addurl")])
     else:
        buttons.append([InlineKeyboardButton('👀 See Url', 
                      callback_data="settings#seeurl")])
        buttons[-1].append(InlineKeyboardButton('❌ Remove Url ', 
                      callback_data="settings#deleteurl"))
     buttons.append([InlineKeyboardButton('back', 
                      callback_data="settings#main")])
     await query.message.edit_text(
        "<b><u>DATABASE</u>\n\nDatabase is required for store your duplicate messages permenant. other wise stored duplicate media may be disappeared when after bot restart.</b>",
        reply_markup=InlineKeyboardMarkup(buttons))

  elif type=="addurl":
     await query.message.delete()
     uri = await bot.ask(user_id, "<b>please send your mongodb url.</b>\n\n<i>get your Mongodb url from [MangoDb](https://mongodb.com)</i>", disable_web_page_preview=True)
     if uri.text=="/cancel":
        return await uri.reply_text(
                  "<b>process canceled !</b>",
                  reply_markup=InlineKeyboardMarkup(buttons))
     if not uri.text.startswith("mongodb+srv://") and not uri.text.endswith("majority"):
        return await uri.reply("<b>Invalid Mongodb Url</b>",
                   reply_markup=InlineKeyboardMarkup(buttons))
     connect, udb = await connect_user_db(user_id, uri.text, "test")
     if connect:
        await udb.drop_all()
        await udb.close()
     else:
        return await uri.reply("<b>Invalid Mongodb Url Cant Connect With This Uri</b>",
                  reply_markup=InlineKeyboardMarkup(buttons))
     await update_configs(user_id, 'db_uri', uri.text)
     await uri.reply("**Successfully database url added**",
             reply_markup=InlineKeyboardMarkup(buttons))

  elif type=="seeurl":
     db_uri = (await get_configs(user_id))['db_uri']
     await query.answer(f"DATABASE URL: {db_uri}", show_alert=True)

  elif type=="deleteurl":
     await update_configs(user_id, 'db_uri', None)
     await query.message.edit_text(
        "**Successfully your database url deleted**",
        reply_markup=InlineKeyboardMarkup(buttons))

  elif type=="filters":
     await query.message.edit_text(
        "<b><u>💠 CUSTOM FILTERS 💠</b></u>\n\n**configure the type of messages which you want forward**",
        reply_markup=await filters_buttons(user_id))

  elif type=="nextfilters":
     await query.edit_message_reply_markup(
        reply_markup=await next_filters_buttons(user_id))

  elif type.startswith("updatefilter"):
     i, key, value = type.split("-")
     if value=="True":
        await update_configs(user_id, key, False)
     else:
        await update_configs(user_id, key, True)
     if key in ["poll", "protect", "voice", "animation", "sticker", "duplicate"]:
        return await query.edit_message_reply_markup(
           reply_markup=await next_filters_buttons(user_id)) 
     await query.edit_message_reply_markup(
        reply_markup=await filters_buttons(user_id))

  elif type=="thumbnail":
     buttons = []
     data = await get_configs(user_id)
     thumbnail = data.get("thumbnail", None)
     if thumbnail is None:
        buttons.append([InlineKeyboardButton("✚ Add Thumbnail ✚", 
                      callback_data="settings#addthumbnail")])
     else:
        buttons.append([InlineKeyboardButton("See Thumbnail", 
                      callback_data="settings#seethumbnail")])
        buttons[-1].append(InlineKeyboardButton("🗑 Delete Thumbnail", 
                      callback_data="settings#deletethumbnail"))
     buttons.append([InlineKeyboardButton("back", 
                      callback_data="settings#main")])
     await query.message.edit_text(
        "<b>CUSTOM THUMBNAIL</b>\n\nYou can set a custom thumbnail to videos and documents. Normaly use its default thumbnail.",
        reply_markup=InlineKeyboardMarkup(buttons))

  elif type=="addthumbnail":
     await query.message.delete()
     photo = await bot.ask(query.message.chat.id, "Send your custom thumbnail photo\n/cancel - cancel this process")
     if photo.text=="/cancel":
        return await photo.reply_text(
                  "<b>process canceled !</b>",
                  reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("back", callback_data="settings#thumbnail")]]))
     if not photo.photo:
        return await photo.reply_text("<b>This is not a photo !</b>",
                  reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("back", callback_data="settings#thumbnail")]]))
     await update_configs(user_id, "thumbnail", photo.photo.file_id)
     await photo.reply_text(
        "<b>successfully updated</b>",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("back", callback_data="settings#thumbnail")]]))

  elif type=="seethumbnail":
     data = await get_configs(user_id)
     thumbnail = data.get("thumbnail", None)
     if thumbnail:
        await bot.send_photo(
           chat_id=query.message.chat.id,
           photo=thumbnail,
           caption="<b>YOUR CUSTOM THUMBNAIL</b>",
           reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("back", callback_data="settings#thumbnail")]])
        )
        await query.message.delete()
     else:
        await query.message.edit_text(
           "<b>No thumbnail found!</b>",
           reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("back", callback_data="settings#thumbnail")]])
        )

  elif type=="deletethumbnail":
     await update_configs(user_id, "thumbnail", None)
     await query.message.edit_text(
        "<b>successfully updated</b>",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("back", callback_data="settings#thumbnail")]]))

  elif type=="quality":
     await query.message.edit_text(
        "<b><u>QUALITY SETTINGS</b></u>\n\n<b>Configure the quality settings for media files</b>",
        reply_markup=await quality_buttons(user_id))

  elif type.startswith("updatequality"):
     i, key, value = type.split("-")
     if value=="True":
        await update_configs(user_id, key, False)
     else:
        await update_configs(user_id, key, True)
     await query.edit_message_reply_markup(
        reply_markup=await quality_buttons(user_id))

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

def main_buttons():
    buttons = [
        [InlineKeyboardButton('🤖 Bots', callback_data="settings#bots"),
         InlineKeyboardButton('📢 Channels', callback_data="settings#channels")],
        [InlineKeyboardButton('📝 Caption', callback_data="settings#caption"),
         InlineKeyboardButton('🔘 Button', callback_data="settings#button")],
        [InlineKeyboardButton('🗄️ Database', callback_data="settings#database"),
         InlineKeyboardButton('⚙️ Filters', callback_data="settings#filters")],
        [InlineKeyboardButton('🏞️ Tʜᴜᴍʙɴᴀɪʟ', callback_data="settings#thumbnail"),
         InlineKeyboardButton('🎛️ Quality', callback_data="settings#quality")],
        [InlineKeyboardButton('Extra Settings', callback_data="settings#extra")]
    ]
    return InlineKeyboardMarkup(buttons)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def filters_buttons(user_id):
    data = await get_configs(user_id)
    buttons = [
        [InlineKeyboardButton(f"Photos : {data['photo']}", callback_data="settings#updatefilter-photo-{data['photo']}"),
         InlineKeyboardButton(f"Videos : {data['video']}", callback_data="settings#updatefilter-video-{data['video']}")],
        [InlineKeyboardButton(f"Documents : {data['document']}", callback_data="settings#updatefilter-document-{data['document']}"),
         InlineKeyboardButton(f"Audios : {data['audio']}", callback_data="settings#updatefilter-audio-{data['audio']}")],
        [InlineKeyboardButton('Next ➡️', callback_data="settings#nextfilters")],
        [InlineKeyboardButton('back', callback_data="settings#main")]
    ]
    return InlineKeyboardMarkup(buttons)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def next_filters_buttons(user_id):
    data = await get_configs(user_id)
    buttons = [
        [InlineKeyboardButton(f"Voice : {data['voice']}", callback_data="settings#updatefilter-voice-{data['voice']}"),
         InlineKeyboardButton(f"Animation : {data['animation']}", callback_data="settings#updatefilter-animation-{data['animation']}")],
        [InlineKeyboardButton(f"Sticker : {data['sticker']}", callback_data="settings#updatefilter-sticker-{data['sticker']}"),
         InlineKeyboardButton(f"Poll : {data['poll']}", callback_data="settings#updatefilter-poll-{data['poll']}")],
        [InlineKeyboardButton(f"Protect Content : {data['protect']}", callback_data="settings#updatefilter-protect-{data['protect']}"),
         InlineKeyboardButton(f"Duplicate : {data['duplicate']}", callback_data="settings#updatefilter-duplicate-{data['duplicate']}")],
        [InlineKeyboardButton('⬅️ Back', callback_data="settings#filters")],
        [InlineKeyboardButton('back', callback_data="settings#main")]
    ]
    return InlineKeyboardMarkup(buttons)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def file_size_buttons(user_id):
    data = await get_configs(user_id)
    buttons = [
        [InlineKeyboardButton(f"50 MB : {'✅' if data['file_size'] == 50000000 else '❌'}", callback_data="settings#file_size-50000000"),
         InlineKeyboardButton(f"100 MB : {'✅' if data['file_size'] == 100000000 else '❌'}", callback_data="settings#file_size-100000000")],
        [InlineKeyboardButton(f"200 MB : {'✅' if data['file_size'] == 200000000 else '❌'}", callback_data="settings#file_size-200000000"),
         InlineKeyboardButton(f"400 MB : {'✅' if data['file_size'] == 400000000 else '❌'}", callback_data="settings#file_size-400000000")],
        [InlineKeyboardButton(f"1 GB : {'✅' if data['file_size'] == 1000000000 else '❌'}", callback_data="settings#file_size-1000000000"),
         InlineKeyboardButton(f"2 GB : {'✅' if data['file_size'] == 2000000000 else '❌'}", callback_data="settings#file_size-2000000000")],
        [InlineKeyboardButton('back', callback_data="settings#main")]
    ]
    return InlineKeyboardMarkup(buttons)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

async def quality_buttons(user_id):
    data = await get_configs(user_id)
    buttons = [
        [InlineKeyboardButton(f"Video : {data['video_quality']}", callback_data="settings#updatequality-video_quality-{data['video_quality']}"),
         InlineKeyboardButton(f"Audio : {data['audio_quality']}", callback_data="settings#updatequality-audio_quality-{data['audio_quality']}")],
        [InlineKeyboardButton('back', callback_data="settings#main")]
    ]
    return InlineKeyboardMarkup(buttons)

# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

def extra_buttons():
    buttons = [
        [InlineKeyboardButton('back', callback_data="settings#main")]
    ]
    return InlineKeyboardMarkup(buttons)



from pyrogram import Client,  filters
from time import time
from config import Config
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helper_fns.helper import get_readable_time, savetoken, USER_DATA, get_media, timex, delete_all, delete_trash
from helper_fns.pbar import progress_bar
from config import botStartTime
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper_fns.watermark import vidmark



############Variables##############
sudo_users = eval(Config.SUDO_USERS)
USER = Config.USER



################Start####################
@Client.on_message(filters.command('start'))
async def startmsg(client, message):
    user_id = message.chat.id
    text = f"Hi {message.from_user.mention(style='md')}, I Am Alive."
    await client.send_message(chat_id=user_id,
                                text=text,reply_markup=InlineKeyboardMarkup(
                            [[
                                    InlineKeyboardButton(
                                        f'⭐ Bot By 𝚂𝚊𝚑𝚒𝚕 ⭐',
                                        url='https://t.me/nik66')
                                ], [
                                    InlineKeyboardButton(
                                        f'❤ Join Channel ❤',
                                        url='https://t.me/nik66x')
                                ]]
                        ))
    return


################Time####################
@Client.on_message(filters.command(["time"]))
async def timecmd(client, message):
    user_id = message.chat.id
    userx = message.from_user.id
    if userx in sudo_users:
        currentTime = get_readable_time(time() - botStartTime)
        await client.send_message(chat_id=message.chat.id,
                                text=f'♻Bot Is Alive For {currentTime}')
        return
    else:
        await client.send_message(chat_id=user_id,
                                text=f"❌Only Authorized Users Can Use This Command")
        return


##############Req######################
@Client.on_message(filters.command(["add"]))
async def add(client, message):
    user_id = message.chat.id
    vdata = {}
    q = 1
    while True:
            data = {}
            try:
                        ask = await client.ask(user_id, f'*️⃣ Send Me Video No. {str(q)}\n\n🔶Send `stop` To Stop\n⏳Request Time Out In 60 Seconds', timeout=60, filters=(filters.document | filters.video | filters.text))
                        video = ask.id
                        try:
                            if not ask.video or ask.document:
                                    if ask.text == "stop":
                                            await ask.request.delete()
                                            break
                        except:
                            pass
                        if ask.video or ask.document:
                            file_type = ask.video or ask.document
                            if file_type.mime_type.startswith("video/"):
                                data['chat'] = user_id
                                data['vid'] =  video
                        else:
                            continue
                        ask = await client.ask(user_id, f'*️⃣ Send Me Thumbnail For Video No. {str(q)}\n\n🔷Send `pass` for default Thumbnail\n🔶Send `stop` To Stop\n⏳Request Time Out In 60 Seconds', timeout=60, filters=(filters.document | filters.photo | filters.text))
                        thumb = ask.id
                        try:
                            if not ask.photo or ask.document:
                                    if ask.text == "stop":
                                            await ask.request.delete()
                                            break
                                    else:
                                        data['thumb'] = False
                        except:
                            pass
                        if ask.photo or (ask.document and ask.document.mime_type.startswith("image/")):
                                data['thumb'] = True
                                data['tid'] =  thumb
                        else:
                            data['thumb'] = False
                        ask = await client.ask(user_id, f'*️⃣ If You Want To Remux Subitle To This Video, Send Subtitle File or If  You Dont Want To Remux Send `pass`\n\n🔶Send `stop` To Stop\n⏳Request Time Out In 60 Seconds', timeout=60, filters=(filters.document | filters.text))
                        sub = ask.id
                        try:
                            if not ask.document:
                                    if ask.text == "stop":
                                            await ask.request.delete()
                                            break
                                    else:
                                            data['sub'] = False
                                            vdata[q] = data
                                            q+=1
                                            continue
                        except:
                            pass
                        if ask.document:
                            file_type = ask.document
                            if not file_type.mime_type.startswith("video/"):
                                ask = await client.ask(user_id, f'*️⃣ Send Remux Type\n\n`softremove`  ,   `softmux`    ,   `hardmux`\n\nIf  You Dont Want To Remux Send `pass`\n\n🔶Send `stop` To Stop\n⏳Request Time Out In 60 Seconds', timeout=60, filters=filters.text)
                                valid = ['softremove', 'softmux', 'hardmux']
                                if ask.text == "stop":
                                            await ask.request.delete()
                                            break
                                if ask.text == "pass":
                                            data['sub'] = False
                                if ask.text in valid:
                                        data['sub'] = True
                                        data['sid'] = sub
                                        data['smode'] = ask.text
                                else:
                                    data['sub'] = False
                        else:
                            data['sub'] = False
                        vdata[q] = data
                        q+=1
            except Exception as e:
                    print(e)
                    await client.send_message(user_id, "🔃❗Tasked Has Been Cancelled.")
                    break
            await ask.request.delete()
    caption=f"🧩Total Files: {str(q-1)}"
    zxx = open('Nik66Bots.txt', "w", encoding="utf-8")
    zxx.write(str(vdata))
    zxx.close()
    await client.send_document(chat_id=user_id, document='data.txt', caption=caption)
    return



###############start remux##############

@Client.on_message(filters.command('process'))
async def process(bot, message):
        user_id = message.chat.id
        userx = message.from_user.id
        if userx in sudo_users:
                try:
                                file_id = int(message.reply_to_message.id)
                                filetype = message.reply_to_message.document
                except:
                        try:
                                ask = await bot.ask(user_id, '*️⃣ Send Bot Dict File', timeout=60, filters=filters.document)
                                filetype = ask.document
                        except:
                                await bot.send_message(user_id, "🔃Timed Out! Tasked Has Been Cancelled.")
                                return
                        file_id = ask.id
        try:
                file_size = filetype.file_size
                if int(file_size)>512000:
                        await bot.send_message(chat_id=user_id, text="❌Invalid File")
                        return
        except Exception as e:
            print(e)
            await bot.send_message(chat_id=user_id,
                text=f"❗Error: {str(e)}")
            return
        m = await bot.get_messages(user_id, file_id, replies=0)
        DEFAULT_DOWNLOAD_DIR = f"./{str(user_id)}_ongoing_dict.txt"
        await bot.download_media(m, DEFAULT_DOWNLOAD_DIR)
        users_open1 = open(DEFAULT_DOWNLOAD_DIR, 'r', encoding="utf-8")
        dic = eval(str(users_open1.read()))
        users_open1.close()
        dvalue = 'File'
        dvaluex = 'Files'
        try:
                m0 = await bot.ask(user_id, f'*️⃣ {str(len(dic))} {dvaluex} Found. Where You Want To Start Process Out Of These {str(len(dic))} {dvaluex}❔\n\n🔘Quick Notes:\n\n🔸Send 3-8 If You Want To Process From {dvalue} No. 3 To {dvalue} No. 8\n🔸Send 3- If You Want To Process Only {dvalue} No. 3\n🔸Send 3 If You Want To Process From {dvalue} No. 3 To Last {dvalue}', timeout=90, filters=filters.text)
                m0_text = m0.text
                if '-' in m0_text:
                        limiter = m0_text.split("-")
                        if len(limiter)>2:
                                await bot.send_message(user_id, "❗Invalied Values.")
                                return
                        try:
                                limit = int(limiter[0]) - 1
                                if len(limiter[1])==0:
                                        limit_to = int(limiter[0])
                                else:
                                        limit_to = int(limiter[1])
                        except:
                                await bot.send_message(user_id, "❗Invalied Values.")
                                return
                else:        
                        try:
                                limit = int(m0_text) - 1
                                if limit<0:
                                        limit = 0
                                limit_to = len(dic)
                        except ValueError:
                                await m.reply('❗Error: Value Must Be Numerical.')
                                return
        except:
                await bot.send_message(user_id, "🔃Timed Out! Tasked Has Been Cancelled.")
                return
        if limit_to>len(dic):
                await bot.send_message(user_id, "❗Invalied Values.")
                return
        countx = 1
        failed = {}
        success = {}
        for i in range(limit, limit_to):
                remnx = str((limit_to-limit)-countx)
                est_start_time = timex()
                value = i+1
                datam = dic[value]
                vid = datam['vid']
                chat_id = datam['chat']
                m = await bot.get_messages(chat_id, vid, replies=0)
                media = get_media(m)
                file_name = media.file_name
                dl_loc = f'./RAW/{file_name}'
                file_size = media.file_size
                start_time = timex()
                datam = (file_name, f"{str(countx)}/{str(limit_to-limit)}", remnx, '🔽Downloading')
                reply = await bot.send_message(chat_id=user_id,
                                        text=f"🔽Starting Download ({str(countx)}/{str(limit_to-limit)})\n🎟️File: {file_name}\n🧶Remaining: {str(remnx)}")
                the_media = await bot.download_media(
                                message=m,
                                file_name=dl_loc,
                                progress=progress_bar,
                                progress_args=(reply,start_time,*datam)
                        )
                if the_media is None:
                        await delete_trash(the_media)
                        await reply.delete()
                        failed[value] = datam
                        continue
                duration = 0
                metadata = extractMetadata(createParser(the_media))
                if metadata.has("duration"):
                        duration = metadata.get('duration').seconds
                output_vid = f"./{str(file_name)}.mp4"
                progress = f"./{str(file_name)}_progress.txt"
                watermark_path = f'./watermark.jpg'
                preset = 'ultrafast'
                watermark_position = "5:5"
                watermark_size = "7"
                datam = (file_name, f"{str(countx)}/{str(limit_to-limit)}", remnx, '🧿Adding Watermark')
                try:
                        output_vid = await vidmark(the_media, reply, progress, watermark_path, output_vid, duration, preset, watermark_position, watermark_size, datam)
                except Exception as err:
                        await reply.edit(f"❗Unable to add Watermark!\n\n{str(err)}")
                        await delete_all("./RAW")
                        return
                print(output_vid)
                break
        return
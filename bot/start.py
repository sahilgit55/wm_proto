from pyrogram import Client,  filters
from time import time
from config import Config
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helper_fns.helper import get_readable_time, saveconfig, deleteconfig, USER_DATA, get_media, timex, delete_all, delete_trash, new_user, create_process_file
from helper_fns.pbar import progress_bar
from config import botStartTime
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper_fns.watermark import vidmarkx, hardmux_vidx
from helper_fns.muxer import softremove_vid, hardmux_vid, softmux_vid
from string import ascii_lowercase, digits
from random import choices
from helper_fns.process import append_master_process, remove_master_process, get_master_process, append_sub_process, remove_sub_process, get_sub_process



############Variables##############
sudo_users = eval(Config.SUDO_USERS)
USER = Config.USER
wpositions = {'5:5': 'Set Top Left', 'main_w-overlay_w-5:5': 'Set Top Right', '5:main_h-overlay_h': 'Set Bottom Left', 'main_w-overlay_w-5:main_h-overlay_h-5': 'Set Bottom Right'}


################Start####################
@Client.on_message(filters.command('start'))
async def startmsg(client, message):
    user_id = message.chat.id
    userx = message.from_user.id
    if userx not in USER_DATA():
            await new_user(userx)
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
    if userx not in USER_DATA():
            await new_user(userx)
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
    userx = message.from_user.id
    if userx not in USER_DATA():
            await new_user(userx)
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
    await client.send_document(chat_id=user_id, document='Nik66Bots.txt', caption=caption)
    return



###############start remux##############

@Client.on_message(filters.command('process'))
async def process(bot, message):
        user_id = message.chat.id
        userx = message.from_user.id
        if userx not in USER_DATA():
                await new_user(userx)
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
        process_id = str(''.join(choices(ascii_lowercase + digits, k=10)))
        append_master_process(process_id)
        mtime = timex()
        for i in range(limit, limit_to):
                if process_id in get_master_process():
                                stime = timex()
                                subprocess_id = str(''.join(choices(ascii_lowercase + digits, k=10)))
                                append_sub_process(subprocess_id)
                                remnx = str((limit_to-limit)-countx)
                                value = i+1
                                data = dic[value]
                                vid = data['vid']
                                chat_id = data['chat']
                                m = await bot.get_messages(chat_id, vid, replies=0)
                                media = get_media(m)
                                file_name = media.file_name
                                dl_loc = f'./RAW/{file_name}'
                                start_time = timex()
                                datam = (file_name, f"{str(countx)}/{str(limit_to-limit)}", remnx, '🔽Downloading Video', '𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍𝚎𝚍')
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
                                        await reply.edit(f"❗Unable to Download Media!\n\n{str(err)}\n\n{str(data)}")
                                        failed[value] = data
                                        continue
                                duration = 0
                                metadata = extractMetadata(createParser(the_media))
                                if metadata.has("duration"):
                                        duration = metadata.get('duration').seconds
                                output_vid = f"./{str(file_name)}"
                                progress = f"./{str(file_name)}_progress.txt"
                                await create_process_file(progress)
                                await delete_trash(output_vid)
                                watermark_path = f'./watermark.jpg'
                                preset = 'ultrafast'
                                watermark_position = "5:5"
                                watermark_size = "7"
                                datam = (file_name, f"{str(countx)}/{str(limit_to-limit)}", remnx, '🛺Adding Watermark', stime, mtime)
                                try:
                                        output_vid_res = await vidmarkx(the_media, reply, progress, watermark_path, output_vid, duration, preset, watermark_position, watermark_size, datam,subprocess_id, process_id)
                                except Exception as err:
                                        await reply.edit(f"❗Unable to add Watermark!\n\n{str(err)}\n\n{str(data)}")
                                        await delete_all("./RAW")
                                        await delete_trash(progress)
                                        failed[value] = data
                                        continue
                                await delete_trash(progress)
                                if output_vid_res[0]:
                                        if data['sub']:
                                                sid = data['sid']
                                                subm = await bot.get_messages(chat_id, sid, replies=0)
                                                media = get_media(subm)
                                                sub_name = media.file_name
                                                sub_loc = f'./RAW/{sub_name}'
                                                start_time = timex()
                                                datam = (sub_name, f"{str(countx)}/{str(limit_to-limit)}", remnx, '🔽Downloading Subtitle', '𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍𝚎𝚍')
                                                subtitle = await bot.download_media(
                                                                message=subm,
                                                                file_name=sub_loc,
                                                                progress=progress_bar,
                                                                progress_args=(reply,start_time,*datam)
                                                        )
                                                if subtitle is None:
                                                        await delete_trash(subtitle)
                                                        await reply.edit(f"❗Unable to Download Subtitle!\n\n{str(err)}\n\n{str(data)}")
                                                        failed[value] = data
                                                        continue
                                                sub_mode = data['smode']
                                                datam = (file_name, f"{str(countx)}/{str(limit_to-limit)}", remnx, '🎮Remuxing Subtitles', stime, mtime)
                                                remux_preset =  'ultrafast'
                                                await create_process_file(progress)
                                                if sub_mode=="softremove":
                                                        output_vid = await softremove_vid(output_vid, sub_loc, reply)
                                                elif sub_mode=="softmux":
                                                        output_vid = await softmux_vid(output_vid, sub_loc, reply)
                                                elif sub_mode=="hardmux":
                                                        output_vid = await hardmux_vidx(output_vid, sub_loc, reply, subprocess_id, remux_preset, duration, progress, process_id, datam)
                                        cc = "test"
                                        datam = (file_name, f"{str(countx)}/{str(limit_to-limit)}", remnx, '🔼Uploadinig', '𝚄𝚙𝚕𝚘𝚊𝚍𝚎𝚍')
                                        await bot.send_video(
                                                        chat_id=user_id,
                                                        video=output_vid,
                                                        caption=cc,
                                                        supports_streaming=True,
                                                        duration=duration,
                                                        thumb='./thumb.jpg',
                                                        progress=progress_bar,
                                                        progress_args=(reply,start_time, *datam))
                else:
                        break
        return



################Cancel Process###########
@Client.on_message(filters.command(["cancel"]))
async def cancell(client, message):
  user_id = message.chat.id
  userx = message.from_user.id
  if userx not in USER_DATA():
            await new_user(userx)
  if userx in sudo_users:
        if len(message.command)==3:
                processx = message.command[1]
                process_id = message.command[2]
                try:
                        if processx=='sp':
                                        remove_sub_process(process_id)
                                        await client.send_message(chat_id=user_id,
                                                        text=f'✅Successfully Cancelled.')
                        elif processx=='mp':
                                        remove_master_process(process_id)
                                        await client.send_message(chat_id=user_id,
                                                        text=f'✅Successfully Cancelled.')
                except Exception as e:
                        await client.send_message(chat_id=user_id,
                                        text=f'❗No Running Processs With This ID')
                return
        else:
                await client.send_message(chat_id=user_id,
                                        text=f'❗Give Me Process ID To Cancel.')
  else:
        await client.send_message(chat_id=user_id,
                                text=f"❌Only Authorized Users Can Use This Command")
        return


##############Setting################
@Client.on_message(filters.command(["settings"]))
async def settings(_, message):
                userx = message.from_user.id
                userx = message.from_user.id
                if userx not in USER_DATA():
                        await new_user(userx)
                watermark_position = USER_DATA()[userx]['watermark']['position']
                watermark_size = USER_DATA()[userx]['watermark']['size']
                watermark_preset = USER_DATA()[userx]['watermark']['preset']
                muxer_preset = USER_DATA()[userx]['muxer']['preset']
                positions = {'Set Top Left':"position_5:5", "Set Top Right": "position_main_w-overlay_w-5:5", "Set Bottom Left": "position_5:main_h-overlay_h", "Set Bottom Right": "position_main_w-overlay_w-5:main_h-overlay_h-5"}
                sizes = [5,7,10,13,15,17,20,25,30,35,40,45]
                pkeys = list(positions.keys())
                KeyBoard = []
                KeyBoard.append([InlineKeyboardButton(f"🔶Watermark Position - {wpositions[watermark_position]}🔶", callback_data="lol-wposition")])
                WP1 = []
                WP2 = []
                zx = 1
                for z in pkeys:
                    s_position = positions[z].replace('position_', '')
                    if s_position !=watermark_position:
                            datam = z
                    else:
                        datam = f"{str(z)} 🟢"
                    keyboard = InlineKeyboardButton(datam, callback_data=str(positions[z]))
                    if zx<3:
                        WP1.append(keyboard)
                    else:
                        WP2.append(keyboard)
                    zx+=1
                KeyBoard.append(WP1)
                KeyBoard.append(WP2)
                KeyBoard.append([InlineKeyboardButton(f"🔶Watermark Size - {str(watermark_size)}%🔶", callback_data="lol-wsize")])
                WS1 = []
                WS2 = []
                WS3 = []
                zz = 1
                for x in sizes:
                    vlue = f"size_{str(x)}"
                    if int(watermark_size)!=int(x):
                        datam = f"{str(x)}%"
                    else:
                        datam = f"{str(x)}% 🟢"
                    keyboard = InlineKeyboardButton(datam, callback_data=vlue)
                    if zz<5:
                            WS1.append(keyboard)
                    elif zz<9:
                            WS2.append(keyboard)
                    else:
                            WS3.append(keyboard)
                    zz+=1
                KeyBoard.append(WS1)
                KeyBoard.append(WS2)
                KeyBoard.append(WS3)
                KeyBoard.append([InlineKeyboardButton(f"🔶Watermark Preset - {watermark_preset}🔶", callback_data="lol-wpset")])
                presets = ['ultrafast', 'veryfast']
                WP = []
                for pp in presets:
                    if watermark_preset!=pp:
                        datam = pp
                    else:
                        datam = f"{str(pp)} 🟢"
                    keyboard = InlineKeyboardButton(datam, callback_data=f'wpreset_{str(pp)}')
                    WP.append(keyboard)
                KeyBoard.append(WP)
                KeyBoard.append([InlineKeyboardButton(f"🔶Muxer Preset - {muxer_preset}🔶", callback_data="lol-mpset")])
                MP = []
                for pp in presets:
                    if muxer_preset!=pp:
                        datam = pp
                    else:
                        datam = f"{str(pp)} 🟢"
                    keyboard = InlineKeyboardButton(datam, callback_data=f'mpreset_{str(pp)}')
                    MP.append(keyboard)
                KeyBoard.append(MP)
                await message.reply_text(
                        text="Settings",
                        disable_web_page_preview=True,
                        reply_markup= InlineKeyboardMarkup(KeyBoard)
                        )
                return
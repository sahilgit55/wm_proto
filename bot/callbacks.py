from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from helper_fns.helper import USER_DATA, saveconfig, check_filex, delete_all, delete_trash
from os import listdir
from os.path import isfile




############Variables##############
sudo_users = eval(Config.SUDO_USERS)
wpositions = {'5:5': 'Top Left', 'main_w-overlay_w-5:5': 'Top Right', '5:main_h-overlay_h': 'Bottom Left', 'main_w-overlay_w-5:main_h-overlay_h-5': 'Bottom Right'}




############CallBack##############
@Client.on_callback_query()
async def newbt(client, callback_query):
        txt = callback_query.data
        user_id = callback_query.message.chat.id
        userx = callback_query.from_user.id
        print(txt)
        # await callback_query.message.delete()
        
        
        if txt.startswith("position_") or txt.startswith("size_") or txt.startswith("wpreset_") or txt.startswith("mpreset_"):
                new_position = txt.split("_", 1)[1]
                if txt.startswith("position_"):
                    await saveconfig(userx, 'watermark', 'position', new_position)
                elif txt.startswith("size_"):
                    await saveconfig(userx, 'watermark', 'size', new_position)
                elif txt.startswith("wpreset_"):
                    await saveconfig(userx, 'watermark', 'preset', new_position)
                elif txt.startswith("mpreset_"):
                    await saveconfig(userx, 'muxer', 'preset', new_position)
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
                watermark_path = f'./{str(userx)}_watermark.jpg'
                watermark_check = await check_filex(watermark_path)
                if watermark_check:
                        key = [InlineKeyboardButton(f"🔶Watermark - Found✅🔶", callback_data="lol-water")]
                else:
                        key = [InlineKeyboardButton(f"🔶Watermark - Not Found❌🔶", callback_data="lol-water")]
                KeyBoard.append(key)
                try:
                    await callback_query.message.edit(
                        text="Settings",
                        disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup(KeyBoard))
                except Exception as e:
                    print(e)
                return
    
        elif txt.startswith("lol"):
            data = txt.split('-')
            keyx = data[1]
            if keyx=='water':
                watermark_path = f'./{str(userx)}_watermark.jpg'
                try:
                    await client.send_document(chat_id=user_id, document=watermark_path, caption=f"Nik66Bots")
                except:
                    await callback_query.answer(
                                f'⚡Nik66Bots⚡',
                                show_alert=True
                            )
            else:
                await callback_query.answer(
                                f'⚡Nik66Bots⚡',
                                show_alert=True
                            )
            return
        elif txt == "renewme":
            await callback_query.message.delete()
            g_d_list = ['db_handler.py', 'config.py', 'bot', 'requirements.txt', 'Dockerfile', 'config.env', 'helper_fns', 'docker-compose.yml', 'thumb.jpg', 'main.py']
            g_list = listdir()
            g_del_list = list(set(g_list) - set(g_d_list))
            deleted = []
            if len(g_del_list) != 0:
                for f in g_del_list:
                    if isfile(f):
                        if not(f.endswith(".session")) and not(f.endswith(".session-journal")):
                            print(f)
                            await delete_trash(f)
                            deleted.append(f)
                    else:
                        print(f)
                        await delete_all(f)
                        deleted.append(f)
                text = f"✔Deleted {len(deleted)} objects 🚮\n\n{str(deleted)}"
                try:
                        await callback_query.answer(
                                text,
                                show_alert=True)
                except:
                    await client.send_message(chat_id=user_id,
                            text=text)
                    
            else:
                await callback_query.answer(
                        f"Nothing to clear 🙄",
                        show_alert=True)
            return
        
        elif txt.startswith("notdelete"):
            await callback_query.answer(
                        f"Ok Dont Waste My Time😂",
                        show_alert=True)
            return
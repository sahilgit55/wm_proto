from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from helper_fns.helper import USER_DATA, saveconfig


############Variables##############
sudo_users = eval(Config.SUDO_USERS)



############CallBack##############
@Client.on_callback_query()
async def newbt(client, callback_query):
        txt = callback_query.data
        user_id = callback_query.message.chat.id
        userx = callback_query.from_user.id
        print(txt)
        # await callback_query.message.delete()
        
        
        # if txt.startswith(""):
        #     await callback_query.answer(
        #                 f'❗Login Has Expired, Try Login Again With /login.',
        #                 show_alert=True
        #             )
        #     return
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
                if watermark_position == "5:main_h-overlay_h":
                    position_tag = "Bottom Left"
                elif watermark_position == "main_w-overlay_w-5:main_h-overlay_h-5":
                    position_tag = "Bottom Right"
                elif watermark_position == "main_w-overlay_w-5:5":
                    position_tag = "Top Right"
                elif watermark_position == "5:5":
                    position_tag = "Top Left"
                else:
                    position_tag = "Top Left"

                watermark_size = USER_DATA()[userx]['watermark']['size']
                if int(watermark_size) == 5:
                    size_tag = "5%"
                elif int(watermark_size) == 7:
                    size_tag = "7%"
                elif int(watermark_size) == 10:
                    size_tag = "10%"
                elif int(watermark_size) == 15:
                    size_tag = "15%"
                elif int(watermark_size) == 20:
                    size_tag = "20%"
                elif int(watermark_size) == 25:
                    size_tag = "25%"
                elif int(watermark_size) == 30:
                    size_tag = "30%"
                elif int(watermark_size) == 35:
                    size_tag = "35%"
                elif int(watermark_size) == 40:
                    size_tag = "40%"
                elif int(watermark_size) == 45:
                    size_tag = "45%"
                else:
                    size_tag = "7%"
                watermark_preset = USER_DATA()[userx]['watermark']['preset']
                muxer_preset = USER_DATA()[userx]['muxer']['preset']
                positions = {'Set Top Left':"position_5:5", "Set Top Right": "position_main_w-overlay_w-5:5", "Set Bottom Left": "position_5:main_h-overlay_h", "Set Bottom Right": "position_main_w-overlay_w-5:main_h-overlay_h-5"}
                sizes = [5,7,10,13,15,17,20,25,30,35,40,45]
                pkeys = list(positions.keys())
                KeyBoard = []
                KeyBoard.append([InlineKeyboardButton(f"🔶Watermark Position - {position_tag}🔶", callback_data="lol-wposition")])
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
                KeyBoard.append([InlineKeyboardButton(f"🔶Watermark Size - {size_tag}🔶", callback_data="lol-wsize")])
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
                await callback_query.message.edit(
                    text="Settings",
                    disable_web_page_preview=True,
                    reply_markup=InlineKeyboardMarkup(KeyBoard))
                # except Exception as e:
                #     await callback_query.answer(
                #         f'❗{str(e)}',
                #         show_alert=True
                #     )
        return
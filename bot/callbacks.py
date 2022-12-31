from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config
from helper_fns.helper import USER_DATA


############Variables##############
sudo_users = eval(Config.SUDO_USERS)



############CallBack##############
@Client.on_callback_query()
async def newbt(client, callback_query):
        txt = callback_query.data
        user_id = callback_query.message.chat.id
        print(txt)
        await callback_query.message.delete()
        
        
        if txt.startswith(""):
            await callback_query.answer(
                        f'❗Login Has Expired, Try Login Again With /login.',
                        show_alert=True
                    )
            return
            
        return
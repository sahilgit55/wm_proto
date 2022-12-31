from config import Config
from db_handler import Database
from time import time
from config import botStartTime
from os import remove
from shutil import rmtree
from asyncio import get_event_loop


db = Database()



############Variables##############
User_Data = eval(Config.User_Data)
CREDIT = Config.CREDIT


############Helper Functions##############
def get_readable_time(seconds: int) -> str:
    result = ''
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f'{days}d'
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f'{hours}h'
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f'{minutes}m'
    seconds = int(seconds)
    result += f'{seconds}s'
    return result



def get_human_size(num):
    base = 1024.0
    sufix_list = ['B','KB','MB','GB','TB','PB','EB','ZB', 'YB']
    for unit in sufix_list:
        if abs(num) < base:
            return f"{round(num, 2)} {unit}"
        num /= base



class Timer:
    def __init__(self, time_between=5):
        self.start_time = time()
        self.time_between = time_between

    def can_send(self):
        if time() > (self.start_time + self.time_between):
            self.start_time = time()
            return True
        return False

def timex():
    return time()


def hrb(value, digits= 2, delim= "", postfix=""):
    """Return a human-readable file size.
    """
    if value is None:
        return None
    chosen_unit = "B"
    for unit in ("KB", "MB", "GB", "TB"):
        if value > 1000:
            value /= 1024
            chosen_unit = unit
        else:
            break
    return f"{value:.{digits}f}" + delim + chosen_unit + postfix


def getbotuptime():
    return get_readable_time(time() - botStartTime)


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]

##########Save Token###############
def USER_DATA():
    return User_Data

##########Save Token###############
async def savetoken(user_id, token, user):
    try:
        if user_id not in User_Data:
            User_Data[user_id] = {}
            User_Data[user_id]['gtoken'] = {}
            User_Data[user_id]['gtoken'][user] = token
        else:
            User_Data[user_id]['gtoken'][user] = token
        data = await db.add_datam(str(User_Data), CREDIT, "User_Data")
        return data
    except Exception as e:
        print(e)
        return False
    

##########Delete Token###############
async def deletetoken(user_id, user):
        try:
            del User_Data[user_id]['gtoken'][user]
            data = await db.add_datam(str(User_Data), CREDIT, "User_Data")
            print("🔶Token Deleted Successfully")
            return data
        except Exception as e:
            print("🔶Failed To Delete Token")
            print(e)
            return False

##########Get BOT###############
def get_media(message):
        media_types = (
            "audio",
            "document",
            "photo",
            "sticker",
            "animation",
            "video",
            "voice",
            "video_note",
        )
        for attr in media_types:
            media = getattr(message, attr, None)
            if media:
                return media
            

##########Clean##########
async def delete_trash(file):
    try:
        remove(file)
    except Exception as e:
        print(e)

async def delete_all(dir):
    try:
        rmtree(dir)
    except Exception as e:
        print(e)
        
        
########Background#############

async def create_backgroud_task(x):
    task = get_event_loop().create_task(x)
    return task
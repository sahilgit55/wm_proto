from datetime import datetime
from config import Config
from motor.motor_asyncio import AsyncIOMotorClient
from pytz import timezone


IST = timezone('Asia/Kolkata')
bot_username = Config.BOT_USERNAME
MONGODB_URI = Config.MONGODB_URI


# def get_human_size(num):
#     base = 1024.0
#     sufix_list = ['B','KB','MB','GB','TB','PB','EB','ZB', 'YB']
#     for unit in sufix_list:
#         if abs(num) < base:
#             return f"{round(num, 2)} {unit}"
#         num /= base


class Database:
    def __init__(self):
        self._client = AsyncIOMotorClient(MONGODB_URI)
        self.db = self._client[bot_username]


    async def add_datam(self, datam, id, colz):
        try:
                col = self.db[colz]
                valu = await self.is_data_exist(id, colz)
                if valu==False:
                    print("🔶Adding Data In New Collection")
                    datetime_ist = datetime.now(IST)
                    tmxzx = str(datetime_ist.strftime('%A %d %B %Y, %I:%M:%S %p'))
                    data_links = dict(
                        id=id,
                        data=datam,
                        date=tmxzx
                    )
                    await col.insert_one(data_links)
                    return True
                else:
                    valuz = await self.get_data(id, colz)
                    dict1 = eval(valuz)
                    dict2 = eval(datam)
                    print("🔶Adding Data In Previous Collection")
                    if dict1==dict2:
                        print("🔶Skipping Saving As Same Data Already Exists")
                        return True
                    dict1.update(dict2)
                    findict = str(dict1)
                    await self.update_data(findict, id, colz)
                    return True
        except Exception as e:
            print(e)
            return False

    async def is_data_exist(self, id, colz):
        col = self.db[colz]
        chat = await col.find_one({'id': id})
        return True if chat else False

    async def get_data(self, id, colz):
        col = self.db[colz]
        user = await col.find_one({'id': id})
        return user.get('data', None)

    async def update_data(self, datam, id, colz):
        col = self.db[colz]
        datetime_ist = datetime.now(IST)
        tmxzx = str(datetime_ist.strftime('%A %d %B %Y, %I:%M:%S %p'))
        await col.update_one({'id': id}, {'$set': {'data': datam, 'date': tmxzx}})
        return

############################

    # async def total_chat_count(self, colz):
    #     col = self.db[colz]
    #     count = await col.count_documents({})
    #     return count

    # async def get_all_chats(self, colz):
    #     col = self.db[colz]
    #     all_chats = col.find({})
    #     lio = []
    #     async for x in all_chats:
    #         lio.append(x)
    #     return lio

    # async def delete_chat(self, id, colz):
    #     col = self.db[colz]
    #     await col.delete_many({'id': id})

    
    # async def get_datazz(self, id, colz, batch):
    #     col = self.db[colz]
    #     user = await col.find_one({'id': id, 'batch': batch})
    #     return user
    
    # async def get(self, id, colz):
    #     col = self.db[colz]
    #     user = await col.find_one({'id': id})
    #     return user
    
    # async def getcstats(self, id):
    #     user = await self.db.command("collstats", id) 
    #     return get_human_size(user.get('storageSize', None))
    
    # async def getdstats(self):
    #     user = await self.db.command("dbstats") 
    #     return get_human_size(user.get('storageSize', None))
    
    # async def listcol(self):
    #     user = await self. db.list_collection_names()
    #     return user

    # async def allcstats(self):
    #     user = await self.db.list_collection_names()
    #     lio = ""
    #     for colz in user:
    #          user = await self.db.command("collstats", colz) 
    #          lio = lio + f"`{str(colz)}`" + " - " + str(get_human_size(user.get('storageSize', None))) + '\n'
    #     finlio = f"Database Status:\n\n{lio[:-1]}"
    #     return finlio
    
    # async def delcol(self, id):
    #     user = await self.db.drop_collection(id)
    #     return user

    # async def deldat(self, id):
    #     user = await self._client.drop_database(id)
    #     return user

    # async def add_datamlogs(self, datam, batch, id, colz):
    #     col = self.db[colz]
    #     valu = await self.is_data_exist(id, colz, batch)
    #     if valu==False:
    #         datetime_ist = datetime.now(IST)
    #         tmxzx = str(datetime_ist.strftime('%A %d %B %Y, %I:%M:%S %p'))
    #         data_links = dict(
    #             id=id,
    #             batch=batch,
    #             data=datam,
    #             date=tmxzx
    #         )
    #         await col.insert_one(data_links)
    #         del data_links, tmxzx, datetime_ist, datam
    #         return
    #     else:
    #         await self.update_data(datam, id, colz, batch)
    #         del datam
    #         return

    # async def getcolsize(self, id):
    #     user = await self.db.command("collstats", id) 
    #     return user.get('storageSize', None)
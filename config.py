from os import getenv
from pymongo import MongoClient
from dotenv import load_dotenv
from os.path import exists
from time import time
from pyrogram import Client

if exists('config.env'):
  load_dotenv('config.env')
  


botStartTime = time()


        
        
def get_mongo_data(MONGODB_URI, BOT_USERNAME, id, colz):
        mongo_client = MongoClient(MONGODB_URI)
        mongo_db = mongo_client[BOT_USERNAME]
        col = mongo_db[colz]
        print("🔶Getting Data From Database")
        item_details = col.find({"id" : id})
        data = False
        for item in item_details:
                        data = item.get('data')
        if data:
            print("🟢Data Found In Database")
            return data
        else:
            print("🟡Data Not Found In Database")
            return "{}"


class Config:
    API_ID = int(getenv("API_ID",""))
    API_HASH = getenv("API_HASH","")
    TOKEN = getenv("TOKEN","")
    Session_String = getenv("Session_String","")
    SUDO_USERS = getenv("SUDO_USERS","")
    CREDIT = getenv("CREDIT","")
    MONGODB_URI = getenv("MONGODB_URI","")
    BOT_USERNAME = getenv("BOT_USERNAME","")
    CHANNEL_USERNAME = getenv("CHANNEL_USERNAME", "")
    User_Data = get_mongo_data(MONGODB_URI, BOT_USERNAME, CREDIT, "User_Data")
    USER = Client(
			name = "User_BoT",
			session_string = Session_String,
			api_id = API_ID,
			api_hash = API_HASH
		)
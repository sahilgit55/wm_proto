from pyrogram import Client

Session_String = 'BQBjDKNEaNKYaRxhGw_I7YUaDgyVuWdkB3s81KsLdn-I9M_ehD1htvyNcX1Bgdi_H0tJ239SA8a7JtR6hm2HaPUM8vmuWhqrTFZL6XDH9XKVfHaSIRHcNwbNRva7HoUae2gOPdF-1XxjU3UpaeM5ZrTBStar82e7d0GT2cWxciI_eGFSfvQN0FLKBQzfzvR-p8bX_fWzolblXL9Vge2BO8RHgEVh_HiYY300csBe0BXG0qinSrZCBVFpehetfAK-W3ebyNNd1Es3ktZ2d-PaCQBrvap4EosUwmweLzjy6RpSbW4AXtuXRWkaNEJ_TUlqceU_vswkxL2atFi5ysdZsJzSUu7VXgA'
API_ID =8763712
API_HASH = '835d27216f117e22a5c192b89a4ce457'

USER = Client(
			name = "WatermarkBOT",
			session_string = Session_String,
			api_id = int(API_ID),
			api_hash = API_HASH
		)

USER.start()

ct = USER.get_chat("watermarkbottt")


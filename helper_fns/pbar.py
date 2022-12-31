from asyncio import sleep as asynciosleep
from pyrogram.errors import FloodWait
from helper_fns.helper import hrb, getbotuptime, Timer, timex



def get_progress_bar_string(current,total):
    completed = int(current) / 8
    total = int(total) / 8
    p = 0 if total == 0 else round(completed * 100 / total)
    p = min(max(p, 0), 100)
    cFull = p // 6
    p_str = '■' * cFull
    p_str += '□' * (16 - cFull)
    p_str = f"[{p_str}]"
    return p_str

timer = Timer(7)

async def progress_bar(current,total,reply,start,*datam):
      if timer.can_send():
        now = timex()
        diff = now - start
        if diff < 1:
            return
        else:
            perc = f"{current * 100 / total:.1f}%"
            elapsed_time = round(diff)
            speed = current / elapsed_time
            sp=str(hrb(speed))+"ps"
            tot=hrb(total)
            cur=hrb(current)
            progress = get_progress_bar_string(current,total)
            try:
                name = datam[0]
                opt = datam[1]
                remnx = datam[2]
                ptype = datam[3]
                botupt = getbotuptime()
                pro_bar = f"🔼{str(ptype)} ({opt})\n🎟️Name: {name}\n🧶Remaining: {str(remnx)} Classes\n\n\n {str(progress)}\n\n ┌ 𝙿𝚛𝚘𝚐𝚛𝚎𝚜𝚜:【 {perc} 】\n ├ 𝚂𝚙𝚎𝚎𝚍:【 {sp} 】\n ├ 𝚄𝚙𝚕𝚘𝚊𝚍𝚎𝚍:【 {cur} 】\n └ 𝚂𝚒𝚣𝚎:【 {tot} 】\n\n\n♥️Bot Uptime: {str(botupt)}"
                await reply.edit(pro_bar)
            
            except FloodWait as e:
                    await asynciosleep(e.value)
            except Exception as e:
                    print(e)

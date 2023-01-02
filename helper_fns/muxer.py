import time
import re
import asyncio
from helper_fns.process import get_sub_process


progress_pattern = re.compile(
    r'(frame|fps|size|time|bitrate|speed)\s*\=\s*(\S+)'
)

def parse_progress(line):
    items = {
        key: value for key, value in progress_pattern.findall(line)
    }
    if not items:
        return None
    return items

async def check_task(tid):
    while True:
        asyncio.sleep(1)
        if tid not in get_sub_process():
            break
    print("🔶Task Cancelled")
    return
        

async def readlines(stream):
    pattern = re.compile(br'[\r\n]+')

    data = bytearray()
    while not stream.at_eof():
        lines = pattern.split(data)
        data[:] = lines.pop(-1)

        for line in lines:
            yield line
        data.extend(await stream.read(1024))


async def read_stderr(start, msg, process):
    async for line in readlines(process.stderr):
            line = line.decode('utf-8')
            print(line)
            progress = parse_progress(line)
            if progress:
                #Progress bar logic
                now = time.time()
                diff = start-now
                text = 'PROGRESS\n'
                text += 'Size : {}\n'.format(progress['size'])
                text += 'Time : {}\n'.format(progress['time'])
                text += 'Speed : {}\n'.format(progress['speed'])

                if round(diff % 5)==0:
                    try:
                        await msg.edit( text )
                    except:
                        pass

async def softmux_vid(vid_filename, sub_filename, msg):

    start = time.time()
    vid = vid_filename
    sub = sub_filename

    out_file = '.'.join(vid_filename.split('.')[:-1])
    output = out_file+'1.mkv'
    out_location = './'+output
    sub_ext = sub_filename.split('.').pop()
    command = [
            'ffmpeg','-hide_banner',
            '-i',vid,
            '-i',sub,
            '-map','1:0','-map','0',
            '-disposition:s:0','default',
            '-c:v','copy',
            '-c:a','copy',
            '-c:s',sub_ext,
            '-y',out_location
            ]

    process = await asyncio.create_subprocess_exec(
            *command,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            )

    # https://github.com/jonghwanhyeon/python-ffmpeg/blob/ccfbba93c46dc0d2cafc1e40ecb71ebf3b5587d2/ffmpeg/ffmpeg.py#L114
    
    await asyncio.wait([
            read_stderr(start,msg, process),
            process.wait(),
        ])
    
    if process.returncode == 0:
        await msg.edit('Muxing  Completed Successfully!\n\nTime taken : {} seconds'.format(round(start-time.time())))
    else:
        await msg.edit('An Error occured while Muxing!')
        return False
    time.sleep(2)
    return output


async def hardmux_vid(vid_filename, sub_filename, msg, subprocess_id, preset, duration, progress, datam):
    start = time.time()
    out_file = '.'.join(vid_filename.split('.')[:-1])
    output = out_file+'1.mp4'
    
    command = [
            'ffmpeg','-hide_banner',
            '-i',vid_filename,
            '-vf','subtitles='+sub_filename,
            '-c:v','h264',
            '-map','0:v:0',
            '-map','0:a:0?',
            '-preset', preset,
            '-y',output
            ]
    process = await asyncio.create_subprocess_exec(
            *command,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            )
    task = asyncio.create_task(check_task(subprocess_id))
    update_msg = asyncio.create_task(read_stderr(start,msg, process))
    done, pending = await asyncio.wait([task,
            update_msg,
            process.wait(),
        ], return_when=asyncio.FIRST_COMPLETED)
    print("🔷In task has cancelled")
    try:
      return_code = process.returncode
      process.terminate()
    except Exception as e:
      print(e)
    if update_msg in pending:
      update_msg.cancelled()
      await update_msg
      await msg.edit("update message cancelled")
    if task in pending:
      task.cancel()
      await task
    print(len(asyncio.Task.all_tasks()))
    print("wating....")
    if return_code == 0:
        await msg.edit('Muxing  Completed Successfully!\n\nTime taken : {} seconds'.format(round(start-time.time())))
    else:
        await msg.edit('An Error occured while Muxing!')
        return False
    
    time.sleep(2)
    return output



async def softremove_vid(vid_filename, sub_filename, msg):

    start = time.time()
    vid = './'+vid_filename
    sub = './'+sub_filename

    out_file = '.'.join(vid_filename.split('.')[:-1])
    output = out_file+'1.mkv'
    out_location = './'+output
    sub_ext = sub_filename.split('.').pop()

    #Removes all other fields and keep only
    #video and audio fields
    command = [
            'ffmpeg','-hide_banner',
            '-i',vid,
            '-i',sub,
            '-map','0:v:0',
            '-map','0:a?',
            '-map','1:0',
            '-disposition:s:0','default',
            '-c:v','copy',
            '-c:a','copy',
            '-c:s',sub_ext,
            '-y',out_location
            ]

    process = await asyncio.create_subprocess_exec(
            *command,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            )

    # https://github.com/jonghwanhyeon/python-ffmpeg/blob/ccfbba93c46dc0d2cafc1e40ecb71ebf3b5587d2/ffmpeg/ffmpeg.py#L114
    
    await asyncio.wait([
            read_stderr(start,msg, process),
            process.wait(),
        ])
    
    if process.returncode == 0:
        await msg.edit('Muxing  Completed Successfully!\n\nTime taken : {} seconds'.format(round(start-time.time())))
    else:
        await msg.edit('An Error occured while Muxing!')
        return False
    time.sleep(2)
    return output

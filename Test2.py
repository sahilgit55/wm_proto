import asyncio


stop  = False



async def func_1():
    global stop
    while True:
            print("func 1")
            await asyncio.sleep(2)
            stop = True
            print("🔶stop in fn1", stop)


async def func_2():
    while True:
        print(1)
        await asyncio.sleep(1)
        print("🔶stop in fn2", stop)
        if stop:
            break
    return


async def func_3():
    while True:
        print(1)
        await asyncio.sleep(1)
        print("🔶stop in fn3", stop)



async def competition():
    task2 = asyncio.create_task(func_1())
    task1 = asyncio.create_task(func_2())
    task3 = asyncio.create_task(func_3())
    done, pending = await asyncio.wait([task1, task2, task3], return_when=asyncio.FIRST_COMPLETED)
    print(dir(task3))
    
    
    
asyncio.run(competition())
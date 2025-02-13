#=========================================================================
    # THREADPOOL INIT
def INIT():
    from concurrent.futures import ThreadPoolExecutor
    import os
    threadcount = os.cpu_count()
    global executor
    executor = ThreadPoolExecutor(max_workers=threadcount)
#=========================================================================
    # WITH LOADBUFFER
def SUBMIT_WB(task):
    import math
    import shutil
    future = executor.submit(task)
    console_w = shutil.get_terminal_size().columns
    console_parts = math.floor((console_w // 2) - 1.5)
    while future.done() != True:
        print(" " * console_parts + "--/" + " " * console_parts,end="\r")
        print(" " * console_parts + "---" + " " * console_parts,end="\r")
        print(" " * console_parts + "--\\" + " " * console_parts,end="\r")
        print(" " * console_parts + "--|" + " " * console_parts,end="\r")
    else:
        print(future)
    return future.result()
def SUBMIT_WBNA(task):
    future = executor.submit(task)
    while future.done() != True:
        pass
    else:
        print(future)
    return future.result()
#=========================================================================
    # NO LOADBUFFER
def SUBMIT_NB(task):
    future = executor.submit(task)
    return future
#=========================================================================
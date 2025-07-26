##==================================================##
## IMPORTS
##==================================================##
from concurrent.futures import ThreadPoolExecutor
import os
##==================================================##
## FUNCTIONS
##==================================================##
def INIT():
    return ThreadPoolExecutor(max_workers=os.cpu_count())
def SHUTDOWN(ThreadPool:object):
    ThreadPool.shutdown(wait=True)
def SUBMIT(Task:callable,ThreadPool:object):
    return ThreadPool.submit(Task)
def SUBMIT_WITH_BUFFER(Task:callable,ThreadPool:object):
    ThreadFuture = ThreadPool.submit(Task)
    while ThreadFuture.done() != True:
        print("--/",end="\r")
        print("---",end="\r")
        print("--\\",end="\r")
        print("--|",end="\r")
    else:
        print(ThreadFuture)
    return ThreadFuture.result()
##==================================================##

"""
def SUBMIT_WB(task:callable,executor:object):
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
#=========================================================================
#=========================================================================
def INIT():
    from concurrent.futures import ThreadPoolExecutor
    import os
    threadcount = os.cpu_count()
    global executor
    executor = ThreadPoolExecutor(max_workers=threadcount)
    return executor
#=========================================================================
#=========================================================================
def SUBMIT_WBNA(task:callable,executor:object):
    future = executor.submit(task)
    while future.done() != True:
        pass
    else:
        print(future)
    return future.result()
#=========================================================================
#=========================================================================
def SUBMIT_NB(task:callable,executor:object):
    future = executor.submit(task)
    return future
#=========================================================================
"""
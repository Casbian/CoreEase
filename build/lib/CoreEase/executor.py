import os
import math
from concurrent.futures import ThreadPoolExecutor
import system
executor = ThreadPoolExecutor(max_workers=4)
def SubmitTasktoThreadWITHLoadBuffer(task):
    future = executor.submit(task)
    LoadBuffer(future)
    return future.result()
def SubmitTasktoThreadNOLoadBuffer(task):
    future = executor.submit(task)
    return future
def LoadBuffer(future):
    console_w = system.ConsoleWidth()
    console_parts = math.floor((console_w // 2) - 1.5)
    while future.done() != True:
        print(" " * console_parts + "--/" + " " * console_parts, end="\r")
        print(" " * console_parts + "---" + " " * console_parts, end="\r")
        print(" " * console_parts + "--\\" + " " * console_parts, end="\r")
        print(" " * console_parts + "--|" + " " * console_parts, end="\r")
    else:
        print(future)
def PassCommandtoConsole(command):
    os.system(command)
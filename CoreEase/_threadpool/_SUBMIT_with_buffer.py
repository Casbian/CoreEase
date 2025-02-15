#=========================================================================
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
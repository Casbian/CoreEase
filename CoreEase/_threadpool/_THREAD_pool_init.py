#=========================================================================
def INIT():
    from concurrent.futures import ThreadPoolExecutor
    import os
    threadcount = os.cpu_count()
    global executor
    executor = ThreadPoolExecutor(max_workers=threadcount)
    return executor
#=========================================================================
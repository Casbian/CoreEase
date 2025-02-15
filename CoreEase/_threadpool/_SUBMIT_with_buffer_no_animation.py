#=========================================================================
def SUBMIT_WBNA(task:callable,executor:object):
    future = executor.submit(task)
    while future.done() != True:
        pass
    else:
        print(future)
    return future.result()
#=========================================================================
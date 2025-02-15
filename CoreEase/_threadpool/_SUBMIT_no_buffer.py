#=========================================================================
def SUBMIT_NB(task:callable,executor:object):
    future = executor.submit(task)
    return future
#=========================================================================
#=========================================================================
def SUBMIT_NB(task:function,executor:object):
    future = executor.submit(task)
    return future
#=========================================================================
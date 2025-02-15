#=========================================================================
def TIME_WAIT(second:int):
    import time
    time.sleep(second)
def TIME_CURRENT():
    import time
    import datetime
    time = datetime.datetime.now()
    return time
def TIME_DIFFERENCE_WITHIN_24_HOUR(targettime:str):
    import datetime
    currenttime = TIME_CURRENT()
    try:
        targettime = datetime.datetime.combine(currenttime.date(),datetime.datetime.strptime(targettime,"%H:%M").time())
    except (ValueError,TypeError):
        return "Error try Format: str(%H:%M)"
    timedifference = targettime - currenttime
    return timedifference
#=========================================================================
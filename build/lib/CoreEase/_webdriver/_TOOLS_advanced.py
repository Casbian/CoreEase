#=========================================================================
def ATOOL_LOGINTRY_PORTAL(browser:object,usernameentryfield:object,passwordentryfield:object,submitbutton:object,username:str,password:str):
    check0 = browser.title
    usernameentryfield.send_keys(username)
    passwordentryfield.send_keys(password)
    submitbutton.click()
    check1 = browser.title
    if check1 == check0:
        return None
    else:
        return True
#=========================================================================
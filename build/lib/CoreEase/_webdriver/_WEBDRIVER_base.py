#=========================================================================
def BROWSER_CLOSE(browser:object):
    browser.quit()
def BROWSER_GOURL(browser:object,urlnewtarget:str):
    from selenium.common.exceptions import InvalidArgumentException
    try:
        browser.get(urlnewtarget)
        return True
    except InvalidArgumentException:
        return None 
#=========================================================================
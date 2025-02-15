#=========================================================================
def STOOL_BUTTONPRESS(browser:object,button:object):
    try:
        button.click()
    except Exception:
        pass
def STOOL_DOMCHANGE():
    domold = browser.page_source
    domnew = browser.page_source
    if domnew != domold:
        return False
    return True
#=========================================================================
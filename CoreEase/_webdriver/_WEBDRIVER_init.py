#=========================================================================
def BROWSER_START(hidden:bool):
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    global browser
    browserheadless = Options()
    browserheadless.add_argument("--headless")
    if hidden == True:
        browser=webdriver.Firefox(options=browserheadless)
    if hidden == False:
        browser=webdriver.Firefox()
    return browser
#=========================================================================
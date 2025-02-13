#=========================================================================
    # BROWSER
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
def BROWSER_CLOSE():
    browser.quit()
def BROWSER_GOURL(urlnewtarget:str):
    from selenium.common.exceptions import InvalidArgumentException
    try:
        browser.get(urlnewtarget)
        return True
    except InvalidArgumentException:
        return None 
#=========================================================================
    # SIMPLE TOOLS
def STOOL_BUTTONPRESS(button:object):
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
    # ADVANCED TOOLS
def ATOOL_LOGINTRY_PORTAL(usernameentryfield:object,passwordentryfield:object,submitbutton:object,username:str,password:str):
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
    # PARSER
def PARS_LOGIN_ENTRYS_AND_BUTTON():
    from selenium.webdriver.common.by import By
    strusernameforsearch = "username"
    strpasswordforsearch = "password"
    strbuttonforsearch = "submit"
    elementstocheck = ["a","button","div","span","form","li","area","svg a","input","img","details","summary","nav","section","article","header","footer","select","textarea","label","option","optgroup","output","progress","meter","input[type='file']","input[type='radio']","input[type='checkbox']","input[type='button']","input[type='submit']","input[type='reset']"]
    attributestocheck = ["href","onclick","action","method","id","class","name","type","placeholder","value","src","alt","title","disabled","checked","readonly","required","maxlength","min","max","step","pattern","role","aria-label","aria-hidden","style","data-*","target","rel","download","xlink:href"]
    for element in elementstocheck:
        x = browser.find_elements(By.CSS_SELECTOR,element)
        for y in x:
            for attribute in attributestocheck:
                z = y.get_attribute(attribute)
                if z != None:
                    if strusernameforsearch.lower() in z.lower():
                        usernameentryfield = y
                    if strpasswordforsearch.lower() in z.lower():
                        passwordentryfield = y
                    if strbuttonforsearch.lower() in z.lower():
                        submitbutton = y
    try:
        return usernameentryfield,passwordentryfield,submitbutton
    except UnboundLocalError:
        try:
            return None,passwordentryfield,submitbutton
        except UnboundLocalError:
            try:
                return None,None,submitbutton
            except UnboundLocalError:
                try:
                    return usernameentryfield,None,submitbutton
                except UnboundLocalError:
                    try:
                        return usernameentryfield,passwordentryfield,None
                    except UnboundLocalError:
                        try:
                            return None,passwordentryfield,None
                        except UnboundLocalError:
                            try:
                                return usernameentryfield,None,None
                            except UnboundLocalError:
                                return None,None,None
def PARS_LINKS():
    from selenium.webdriver.common.by import By
    httplinklist = []
    httpslinklist = []
    strhttpsearch = "http://"
    strhttpssearch = "https://"
    elementstocheck = ["a","button","div","span","form","li","area","svg a","input","img","details","summary","nav","section","article","header","footer","select","textarea","label","option","optgroup","output","progress","meter","input[type='file']","input[type='radio']","input[type='checkbox']","input[type='button']","input[type='submit']","input[type='reset']"]
    attributestocheck = ["href","onclick","action","method","id","class","name","type","placeholder","value","src","alt","title","disabled","checked","readonly","required","maxlength","min","max","step","pattern","role","aria-label","aria-hidden","style","data-*","target","rel","download","xlink:href"]
    for element in elementstocheck:
        x = browser.find_elements(By.CSS_SELECTOR,element)
        for y in x:
            for attribute in attributestocheck:
                z = y.get_attribute(attribute)
                if z != None:
                    if strhttpsearch.lower() in z.lower():
                        if z not in httplinklist:
                            httplinklist.append(y.text)
                            httplinklist.append(z)
                    if strhttpssearch.lower() in z.lower():
                        if z not in httpslinklist:
                            httpslinklist.append(y.text)
                            httpslinklist.append(z)
    return httplinklist,httpslinklist
def PARS_BUTTONS():
    from selenium.webdriver.common.by import By
    buttonlist = []
    elementstocheck = ["button","input[type='button']","input[type='submit']","input"]
    attributestocheck = ["id"]
    for element in elementstocheck:
        x = browser.find_elements(By.CSS_SELECTOR,element)
        for y in x:
            for attribute in attributestocheck:
                z = y.get_attribute(attribute)
                if z != None:
                    if z not in buttonlist:
                        buttonlist.append(z)
                    if y not in buttonlist:
                        buttonlist.append(y)
    return buttonlist
#=========================================================================
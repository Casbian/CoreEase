#=========================================================================
def CMD_HEIGHT():
    import shutil
    consoleheight = shutil.get_terminal_size().lines
    return consoleheight
def CMD_WIDTH():
    import shutil
    consolewidth = shutil.get_terminal_size().columns
    return consolewidth
#=========================================================================
import pyautogui
class Automation:
    def copy():
        Automation.control("c")
        
    def clickNCopy(x, y):
        pyautogui.click(x,y)
        Automation.copy()
    
    def pos():
        return pyautogui.position()
    
    def nClicksNCopy(positions):
        for x, y in positions:
            pyautogui.click(x,y)
        Automation.copy()
    
    def selectAll():
        Automation.control("a")
    
    def command(typ):
        pyautogui.hotkey("command", typ)
    
    def control(typ):
        pyautogui.hotkey("ctrl", typ)

    def click(x,y):
        pyautogui.click(x,y)
        
    def write(txt):
        pyautogui.typewrite(txt)
    
    def enter():
        pyautogui.typewrite(['enter'])
    
    def moveMouse(points, duration = 0.25, times = 3):
        for i in range(times):
            for x, y in points:
                pyautogui.moveTo(x, y, duration=duration)
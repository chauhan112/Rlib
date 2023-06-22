from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
import time
import os
import datetime
from threading import Timer

PLAY_GROUND98 = "http://192.168.144.90/playground/LCAPDevPortal/#"

previewBtnClass = './/button[@mattooltip="Preview"]'
loggingtime = 60*60 # 1 hour = 60*60 = 3600sec

class Log:
    def __init__(self):
        self._header = "name, date, time, status, pic\n"
    def set_filepath(self, name):
        self._name = name
        if not os.path.exists(self._name):
            with open(self._name, "w") as f:
                f.write(self._header)
    def run(self, name,status, img_path):
        n = datetime.datetime.now()
        date = f"{n.day}.{n.month}.{n.year}"
        time = f"{n.hour}:{n.minute}:{n.second}"
        with open(self._name, "a") as f:
            f.write(f"{name},{date},{time},{status},{img_path}\n")
class IStep:
    def run(self):
        pass
class IsRunning(IStep):
    def __init__(self, driver):
        self._driver = driver
    def run(self):
        wait = WebDriverWait(self._driver, 5*60)
        try:
            wait.until(expected_conditions.presence_of_element_located((By.XPATH, "(//button[@id='preview-get-started'])[1]")))
        except Exception as e:
            print(e)
            return False
        ele = self._driver.find_element(By.CSS_SELECTOR,"#preview-get-started")
        return ele.find_element(By.CSS_SELECTOR, ".mat-button-wrapper").text.lower() == "VIEW APPLICATION".lower()
class AppPlayGroundLogger(IStep):
    def __init__(self, username, password, driver=None):
        self._driver = driver
        self._username = username
        self._password = password
    def run(self):
        print("logging in")
        self._driver.find_element(By.ID, 'welcome_header_login_button').click()
        self._driver.find_element(By.ID, 'form_field_input_Your email_login').send_keys(self._username)
        self._driver.find_element(By.ID, 'form_field_input_Password_login').send_keys(self._password)
        self._driver.find_element(By.ID, 'login_login_button').click()
class SaveImage(IStep):
    def __init__(self, driver=None):
        self._driver = driver
    def run(self):
        print("saving image")
        n =datetime.datetime.now()
        image_name = f"{n.second}_{n.minute}_{n.hour}_{n.day}_{n.month}_{n.year}" + ".png"
        loc = os.sep.join([self._loc, image_name])
        self._driver.save_screenshot(loc)
        return loc
    def set_location(self, loc: str):
        if not os.path.exists(loc):
            os.makedirs(loc)
        self._loc = loc
    def set_name(self, name: str):
        self._name = name
class Waiter(IStep):
    def __init__(self, driver=None):
        self._driver = driver
    def set_wait_id(self, element_id):
        self._id= element_id
        self._condition = expected_conditions.presence_of_element_located((By.ID, element_id))
    def set_waiting_time(self, time_in_sec):
        self._time = time_in_sec
    def run(self):
        wait = WebDriverWait(self._driver, self._time)
        wait.until(self._condition)
    def set_element_path(self, path):
        self._condition = expected_conditions.presence_of_element_located((By.XPATH, path))
class PreviewApplication(IStep):
    def __init__(self, driver=None):
        self._driver = driver
    def set_name(self, name):
        self._name = name
    def run(self, onThread=False):
        if not onThread:
            self._run()
            return 
        from OpsDB import OpsDB
        OpsDB.runOnThread(self._run)
    def _run(self):
        start = time.time()
        print("previewing "+ self._name)
        w = Waiter(self._driver)
        self._driver.find_element(By.ID, 'text_input_search').clear_field()
        self._driver.find_element(By.ID, 'text_input_search').send_keys(self._name)
        actions = ActionChains(self._driver)
        actions.send_keys(Keys.ENTER)
        actions.perform()

        w.set_waiting_time(3*60)
        w.set_wait_id(f"card_title_label_{self._name}")
        w.run()
        time.sleep(1) # dont know why but it may have fixed the issue caused on the day: 19_34_14_15_2_2023.png
        a = ActionChains(self._driver)
        m = self._driver.find_element(By.ID, f"card_title_label_{self._name}")
        a.move_to_element(m).perform()

        w.set_waiting_time(60)
        w.set_wait_id(f"button_edit_in_lcap_{self._name}")
        w.run()
        time.sleep(.5)
        n = self._driver.find_element(By.ID, f"button_edit_in_lcap_{self._name}")
        a.move_to_element(n).click().perform()
        time.sleep(3)
        self._driver.switch_to.window(self._driver.window_handles[1])

        w.set_waiting_time(10)
        w.set_element_path(previewBtnClass)
        w.run()

        #Preview button
        self._driver.find_element(By.XPATH, previewBtnClass).click()
        self._driver.find_element(By.ID, "preview-get-started").click()
        ir = IsRunning(self._driver)
        if not ir.run():
            raise IOError("Could not preview")
        end = time.time()
        print("total time for compiling: "+ end)
class PreviewAutomater:
    def __init__(self):
        self._driver = None
        self._link = None
        self._steps = []
        self._options = None
    def set_link(self, link: str):
        self._link = link
    def set_steps(self, steps: list[IStep]):
        self._steps += steps
    def add_step(self, step: IStep):
        self._steps.append(step)
    def automate(self):
        self.get_driver()
        for s in self._steps:
            s.run()
    def close(self):
        self._driver.close()
    def make_head_less(self):
        self._options = Options()
        WINDOW_SIZE = "1920,1080"
        self._options.add_argument("--headless")
        self._options.add_argument("--window-size=%s" % WINDOW_SIZE)
    def get_driver(self):
        if self._driver is None:
            if self._options is not None:
                self._driver = webdriver.Chrome(options=self._options)
            else:
                self._driver = webdriver.Chrome()
            self._driver.get(self._link)
            self._driver.maximize_window()
            self._driver.implicitly_wait(5)
        return self._driver
class Main:
    def previewApplication(name, run_in_background= False, saveImage=False, preview_pic_location="preview", portal=PLAY_GROUND98,
            username="chauh-ra", password="chauh-ra"):
        pa = PreviewAutomater()
        if run_in_background:
            pa.make_head_less()
        pa.set_link(portal)
        pa.add_step(AppPlayGroundLogger(username, password, pa.get_driver()))
        paap = PreviewApplication(pa.get_driver())
        paap.set_name(name)
        pa.add_step(paap)
        if saveImage:
            imag = SaveImage(pa.get_driver())
            imag.set_location(preview_pic_location)
            pa.add_step(imag)
        pa.automate()
        return pa
    def checkPreviewNLog(name, run_in_background= False, saveImage=False, preview_pic_location="preview", portal=PLAY_GROUND98,
            username="chauh-ra", password="chauh-ra"):
        pa = PreviewAutomater()
        if run_in_background:
            pa.make_head_less()
        pa.set_link(portal)
        pa.add_step(AppPlayGroundLogger(username, password, pa.get_driver()))
        paap = PreviewApplication(pa.get_driver())
        paap.set_name(name)
        pa.add_step(paap)
        imag = SaveImage(pa.get_driver())
        imag.set_location(preview_pic_location)
        lg = Log()
        lg.set_filepath(os.sep.join([preview_pic_location, "log.csv"]))
        try:
            pa.automate()
            status = "running"
        except Exception as e:
            status = "no running"
            print(e)
        img_path = imag.run()
        lg.run(name, status, img_path)
        pa.close()
class CustomTimer:
    def __init__(self, time, func):
        # time in seconds
        self.time = time
        self.func = func
        self.t = Timer(time, self._threadInitialize)
        self.t.start()
        self._running = True

    def _threadInitialize(self):
        self.func()
        self.t.cancel()  #reset timer T
        if(self._running):
            self.t = Timer(self.time, self._threadInitialize)
            self.t.start()

    def cancel(self):
        self.t.cancel()
        self._running = False

    def changeTime(self, newTime):
        self.time = newTime
        self.t.cancel()
        self.t = Timer(self.time, self._threadInitialize)
        self.t.start()

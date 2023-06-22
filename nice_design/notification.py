class INotifier:
    def notify(self):
        pass
class Notifier:
    def playMusic(musicPath):
        from OpsDB import OpsDB
        OpsDB.cmd().onthread(f"cvlc \"{musicPath}\" --play-and-exit")
class BasicSetup:
    def __init__(self, title=None, msg=None, time_period: int = 0, time_out: int= 2):
        self.set_time_out(time_out)
        self.set_notification_time_period(time_period)
        if title is not None:
            self.set_title(title)
        if msg is not None:
            self.set_message(msg)
    def set_title(self, title: str):
        self._title = title
    def set_time_out(self, time_out):
        self._timeout = time_out
    def set_notification_time_period(self, time_period):
        self._time_period = time_period
    def set_message(self, msg):
        self._msg = msg
class WindowNotifier(INotifier, BasicSetup):
    def notify(self):
        from TimeDB import TimeDB
        TimeDB.setTimer().oneTimeTimer(self._time_period, self._notify)
    def _notify(self):
        from plyer import notification
        if(icon is None):
            icon = Path.joinPath(resourcePath(),r"assests\python_18894.ico")
        notification.notify(
            title = self._title,
            message = self._msg,
            timeout = self._timeout,
            app_icon = icon
        )
class LinuxNotifier(INotifier, BasicSetup):
    def notify(self):
        from TimeDB import TimeDB
        TimeDB.setTimer().oneTimeTimer(self._time_period, self._notify)
    def _notify(self):
        from OpsDB import OpsDB
        txt = f"notify-send \"{self._msg}\""
        try:
            txt = f"notify-send \"{self._title}\" \"{self._msg}\""
        except:
            pass
        OpsDB.cmd().onthread(txt, )
        if '_music_path' in self.__dict__:
            Notifier.playMusic(self._music_path)
    def set_music(self, musicPath):
        self._music_path = musicPath
class JupyterNotifier(INotifier):
    def set_message(self, message: str):
        self._msg = message
    def notify(self):
        from IPython.display import display, HTML
        if '_music_path' in self.__dict__:
            Notifier.playMusic(self._music_path)
        display(HTML("<script>alert('{}');</script>".format(self._msg)))
        
    def set_music_path(self, path):
        self._music_path = path
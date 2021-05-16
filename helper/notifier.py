import json
from os import path
from pynotifier import Notification
import pathlib, os
import playsound

try:
    from win10toast import ToastNotifier
except:
    pass

class Notifier:
    config_data = {}
    projectPath = ""
    soundPath = ""

    def __init__(self):
        self.projectPath = pathlib.Path(__file__).parent.parent.absolute()
        p = pathlib.PurePath("Resources/alert.wav")
        self.soundPath = os.path.join(self.projectPath, p)

        p = pathlib.PurePath("helper/config.json")
        with open(os.path.join(self.projectPath, p)) as fh:
            self.config_data = json.loads(fh.read())

    def notify(self, head, msg):
        if(self.config_data['linux_win'] == 'linux'):
            self.linux_notify(head, msg)
        else:
            self.win_notify(head, msg)

    def win_notify(self, head, msg):
        toast = ToastNotifier()
        p = pathlib.PurePath("Resources/syringe.ico")
        toast.show_toast(head, msg, duration=20, icon_path=os.path.join(self.projectPath, p))
        playsound.playsound(self.soundPath)
        playsound.playsound(self.soundPath)

    def linux_notify(self, head, msg):
        current = pathlib.Path(__file__).parent.absolute()

        p = pathlib.PurePath("Resources/syringe.png")

        Notification(
            title=head,
            description=msg,
            duration=5,  
            icon_path=os.path.join(self.projectPath, p),
            urgency='critical'
        ).send()

        playsound.playsound(self.soundPath)
        playsound.playsound(self.soundPath)

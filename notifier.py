from pynotifier import Notification
import pathlib, os
import playsound
import cfg
try:
    from win10toast import ToastNotifier
except:
    pass

class Notifier:
    def notify(self, head, msg):
        if(cfg.constants['linux_win'] == 'linux'):
            self.linux_notify(head, msg)
        else:
            self.win_notify(head, msg)

    def win_notify(self, head, msg):
        toast = ToastNotifier()
        toast.show_toast(head, msg, duration=20, icon_path="syringe.ico")
        playsound.playsound('alert.wav')
        playsound.playsound('alert.wav')

    def linux_notify(self, head, msg):
        current = pathlib.Path(__file__).parent.absolute()

        Notification(
            title=head,
            description=msg,
            duration=5,  
            icon_path=os.path.join(current, 'syringe.png'),
            urgency='critical'
        ).send()

        playsound.playsound('alert.wav')
        playsound.playsound('alert.wav')

import time
import tkinter as tk
from tkinter import ttk
from tkinter.constants import E, W
import json
import os, pathlib

# root

root = tk.Tk()
root.geometry('400x200')
root.resizable(0, 0)
root.title('CoWin Notification Alerts Configurator')

root.columnconfigure(0, weight = 1)

pin = tk.StringVar()
osVar = tk.StringVar()

form = ttk.Frame(root)
form.pack(padx=10, pady=10, fill='x', expand=True)

def buttonClicked():
    config = {
        'pin': pin.get(),
        'linux_win': osVar.get()
    }

    if(not pin.get() or not osVar.get()):
        if(not pin.get()):
            print("\033[0;31mPin Code not entered.\033[0m")
        if(not osVar.get()):
            print("\033[0;31mOS not entered.\033[0m")
        print("\033[1;31mConfiguration unsuccessful.\033[0m")
        exit()
    else:
        print("\033[1;32mConfiguration Successful.\033[0m")
        print("Your pincode is \033[1;33m",  pin.get(), "\033[0mand you are on a \033[1;33m", end="")
        if(config['linux_win'] == 'linux'):
            print("Linux-based System\033[0m")
        else:
            print("Windows\033[0m")

    projectPath = pathlib.Path(__file__).parent.parent.absolute()
    dumpPath = os.path.join(projectPath, "helper/config.json")

    jsonDump = json.dumps(config, indent=2)
    oh = open(dumpPath, 'w')
    oh.write(jsonDump)

    exit()


# Pin code
pinLabel = tk.Label(form, text='Your Pincode')
pinLabel.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)

pinEntry = tk.Entry(form, textvariable=pin)
pinEntry.grid(column=2, row=0, sticky=tk.E, padx=10, pady=5)
pinEntry.focus()

# OS
osLabel = tk.Label(form, text='OS')
osLabel.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)

r1 = ttk.Radiobutton(form, text='Linux-based OS', value='linux', variable=osVar)
r1.grid(column=2, row=1)
r1 = ttk.Radiobutton(form, text='Windows', value='win', variable=osVar)
r1.grid(column=3, row=1)

# Submit
submitButton = tk.Button(form, text="Submit", command=buttonClicked)
submitButton.grid(column=2, row=4, padx=5, pady=20)




root.mainloop()

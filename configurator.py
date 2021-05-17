import time
import tkinter as tk
from tkinter import Event, ttk
from tkinter.constants import E, W
import json
import os, pathlib

# root
#TODO: Add option for Age
class GUI:
    root = tk.Tk()
    # pin = tk.StringVar()
    # osVar = tk.StringVar()
    vars = []

    def __init__(self, title, size, resizable_x = 0, resizable_y = 0) -> None:
        self.root.geometry(size)
        self.root.resizable(0, 0)
        self.root.title(title)
        self.root.resizable(resizable_x, resizable_y)
        self.root.columnconfigure(0, weight = 1)

    def createFrane(self, name):
        newFrame = ttk.Frame(name)
        newFrame.pack(padx=10, pady=10, fill='x', expand=True)
        return newFrame

    def createEntryField(self, frame, label, x, y, variable):
        fieldLabel = tk.Label(frame, text=label)
        fieldLabel.grid(column=x, row=y, sticky=tk.W, padx=5, pady=5)

        fieldEntry = tk.Entry(frame, textvariable=variable)
        fieldEntry.grid(column=x + 1, row=y, sticky=tk.E, padx=10, pady=5)
        
        self.vars.append(variable)

        return (fieldLabel, fieldEntry)

    def createLabel(self, frame, label, x, y):
        fieldLabel = tk.Label(frame, text=label)
        fieldLabel.grid(column=x, row=y, sticky=(tk.E, tk.W), padx=10, pady=5)

        return fieldLabel

    def createRadioField(self, frame, label, options, x, y, variable):
        fieldLabel = tk.Label(frame, text=label)
        fieldLabel.grid(column=x, row=y, sticky=tk.W, padx=5, pady=5)

        radioButtons = []
        posDelta = 0
        for option in options:
            posDelta += 1
            r = tk.Radiobutton(frame, text=option[0], value=option[1], variable=variable)
            r.grid(column=x + posDelta, row=y)
            radioButtons.append(r)

        self.vars.append(variable)

        return (fieldLabel, radioButtons)

    def createButton(self, frame, label, x, y, function):
        bton = tk.Button(frame, text=label, command=lambda: function(frame))
        bton.grid(column= x, row=y, padx=5, pady=20)
        return bton

    def submitButtonClicked(self, frame):
        config = {
            'pin': self.vars[0].get(),
            'linux_win': self.vars[1].get()
        }

        if(not config['pin'] or not config['linux_win']):
            if(not config['pin'] and not config['linux_win']):
                self.createLabel(frame, "Pin not entered and OS not selected", 2, 2)
            elif(not config['pin']):
                self.createLabel(frame, "Pin not entered", 2, 2)
            else:
                self.createLabel(frame, "OS not selected", 2, 2)
        elif(len(config['pin']) != 6):
            self.createLabel(frame, "Mind checking the pincode once again?", 2, 2)
        else:
            self.createLabel(frame, "Thank you for configuring me. Exiting..", 2, 2)
            self.root.after(1000, lambda: exit())

        dumpPath = pathlib.PurePath("helper/config.json")

        jsonDump = json.dumps(config)
        with open(dumpPath, 'w') as oh:
            oh.write(jsonDump)



if __name__ == '__main__':
    window = GUI("CoWin Notifier Configurator", '500x200', 0, 0)
    form = window.createFrane(window.root)
    responseVar = []

    # Pin Field
    pin = tk.StringVar()
    (pinLabel, pinEntry) = window.createEntryField(form, "Pincode", 1, 0, pin)
    pinEntry.focus()
    
    # OS Field
    osVar = tk.StringVar()
    osOptions = [("Linux-Based OS", "linux"), ("Windows", "win")]
    (osLabel, osRadio) = window.createRadioField(form, "OS", osOptions, 1, 1, osVar)

    # Submit Button
    submitButton = window.createButton(form, "Submit", 2, 3, window.submitButtonClicked)

    window.root.mainloop()

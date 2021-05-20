import time
import tkinter as tk
from tkinter import Event, ttk
from tkinter.constants import E, RADIOBUTTON, W
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
    
    def pins_validity(self, pins_list):
        for pin in pins_list:
            if(len(pin) != 6):
                return False
        
        return True

    def createCheckboxField(self, frame, label, options, x, y):
        fieldLabel = tk.Label(frame, text=label)
        fieldLabel.grid(column=x, row=y, sticky=tk.W, padx=5, pady=5)

        chkVar = []
        chkBoxes = []
        posDelta = 0
        for option in options:
            var = tk.IntVar()
            posDelta += 1
            ch = tk.Checkbutton(frame, text=option, variable=var)
            ch.grid(column=x + posDelta, row=y)
            chkBoxes.append(ch)
            chkVar.append(var)
        
        self.vars.append(chkVar)

        return (fieldLabel, chkBoxes)

    def createButton(self, frame, label, x, y, function):
        bton = tk.Button(frame, text=label, command=lambda: function(frame, x, y))
        bton.grid(column= x, row=y, padx=5, pady=20)
        return bton

    def submitButtonClicked(self, frame, x, y):
        config = {
            'pin': self.vars[0].get(),
            'linux_win': self.vars[1].get(),
            '18+': self.vars[2][0].get(),
            '45+': self.vars[2][1].get()
        }

        pins_list = []
        for pin in config['pin'].split(","):
            pins_list.append(pin.strip())
        config['pin'] = pins_list

        if(not config['pin'] or not config['linux_win'] or not (config['18+'] or config['45+'])):
            if(not config['pin'] and not config['linux_win'] and not (config['18+'] and config['45+'])):
                self.createLabel(frame, "Pin, OS, Age group missing", x, y - 1)
            elif(not config['pin']):
                self.createLabel(frame, "Pin not entered", x, y - 1)
            elif(not config['linux_win']):
                self.createLabel(frame, "OS not selected", x, y - 1)
            else:
                self.createLabel(frame, "Age group not specified", x, y - 1)
        elif(not self.pins_validity(config['pin'])):
            self.createLabel(frame, "Mind checking pin-code once again?", x, y - 1)
        else:
            self.createLabel(frame, "Thank you for configuring me. Exiting..", x, y - 1)
            self.root.after(1000, lambda: exit())

        dumpPath = pathlib.PurePath("helper/config.json")

        jsonDump = json.dumps(config)
        # print(jsonDump)
        with open(dumpPath, 'w') as oh:
            oh.write(jsonDump)



if __name__ == '__main__':
    window = GUI("CoWin Notifier Configurator", '600x200', 1, 1)
    form = window.createFrane(window.root)
    responseVar = []

    # Pin Field
    pin = tk.StringVar()
    (pinLabel, pinEntry) = window.createEntryField(form, "Pincodes (Separated by comma)", 1, 0, pin)
    pinEntry.focus()
    
    # OS Field
    osVar = tk.StringVar()
    osOptions = [("Linux-Based OS", "linux"), ("Windows", "win")]
    (osLabel, osRadio) = window.createRadioField(form, "OS", osOptions, 1, 1, osVar)

    # Age Field
    ageVars = [tk.IntVar(), tk.IntVar()]
    ageOptions = ["18 - 44", "45+"]
    (ageLabel, ageBoxes) = window.createCheckboxField(form, "Age Group", ageOptions, 1, 2)

    # Submit Button
    submitButton = window.createButton(form, "Submit", 2, 4, window.submitButtonClicked)

    window.root.mainloop()

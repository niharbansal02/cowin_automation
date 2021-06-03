import time
import tkinter as tk
from tkinter import DoubleVar, Event, Variable, ttk
from tkinter.constants import E, RADIOBUTTON, W
import json
import os, pathlib
import requests

# root
#TODO: Add option for Age
class GUI:
    root = tk.Tk()
    # pin = tk.StringVar()
    # osVar = tk.StringVar()
    vars = {}

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

    def createEntryField(self, frame, label, x, y, variable, alias = None):
        fieldLabel = tk.Label(frame, text=label)
        fieldLabel.grid(column=x, row=y, sticky=tk.W, padx=5, pady=5)

        fieldEntry = tk.Entry(frame, textvariable=variable)
        fieldEntry.grid(column=x + 1, row=y, sticky=tk.E, padx=10, pady=5)
        
        self.vars[alias] = variable

        return (fieldLabel, fieldEntry)

    def createLabel(self, frame, label, x, y, alias = None):
        fieldLabel = tk.Label(frame, text=label)
        fieldLabel.grid(column=x, row=y, sticky=(tk.E, tk.W), padx=10, pady=5)

        return fieldLabel

    def createRadioField(self, frame, label, options, x, y, variable, func = None, alias = None):
        fieldLabel = tk.Label(frame, text=label)
        fieldLabel.grid(column=x, row=y, sticky=tk.W, padx=5, pady=5)

        radioButtons = []
        posDelta = 0
        for option in options:
            posDelta += 1
            r = tk.Radiobutton(frame, text=option[0], value=option[1], variable=variable, command=func)
            r.grid(column=x + posDelta, row=y)
            radioButtons.append(r)
        
        self.vars[alias] = variable

        return (fieldLabel, radioButtons)
    
    def pins_validity(self, pins_list):
        for pin in pins_list:
            if(len(pin) != 6):
                return False
        
        return True

    def createCheckboxField(self, frame, label, options, x, y, alias = None):
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
        
        self.vars[alias] = chkVar

        return (fieldLabel, chkBoxes)

    def createDropDown(self, frame, label, var, values, x, y, alias = None):
        fieldLabel = tk.Label(frame, text=label)
        fieldLabel.grid(column=x, row=y, sticky=tk.W, padx=5, pady=5)

        dropDown = ttk.Combobox(frame, textvariable=var, values=values)
        dropDown.grid(column=x + 1, row=y, sticky=tk.W, padx=5, pady=5)
        dropDown.current(1)

        self.vars[alias] = vars

        return var, dropDown

    def createButton(self, frame, label, x, y, function):
        bton = tk.Button(frame, text=label, command=lambda: function(frame, x, y))
        bton.grid(column= x, row=y, padx=5, pady=20)
        return bton

    def submitButtonClicked(self, frame, x, y):
        config = {
            'pin': self.vars["pin"].get(),
            'linux_win': self.vars["os"].get(),
            '18+': self.vars["ageListBool"][0].get(),
            '45+': self.vars["ageListBool"][1].get(),
            'dose': self.vars["dose"].get()
        }

        # print(json.dumps(config, indent=4))

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

def decider(pin_dist, window, el1, el2):
    if(pin_dist == "pin"):
        byPin(window)
    else:
        byDist(window)
        pass

def byPin(window):
    # Pin Field
    pin = tk.StringVar()
    (pinLabel, pinEntry) = window.createEntryField(form, "Pincodes (Separated by comma)", 1, 4, pin, "pin")
    pinEntry.focus()
    
    # Submit Button
    submitButton = window.createButton(form, "Submit", 2, 6, window.submitButtonClicked)

def byDist(window):
    states_URL = "https://cdn-api.co-vin.in/api/v2/admin/location/states"

    hdr = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'accept': 'application/json',
            'Accept-Language': 'en_US'
    }

    response = requests.get(states_URL, headers=hdr)
    jsonDump = response.text
    JSON = json.loads(jsonDump)
    stateList = []
    stateNameList = []
    stateDict = {}
    for state in JSON["states"]:
        stateList.append((state["state_id"], state["state_name"]))
        stateNameList.append(state["state_name"])
        stateDict[state["state_name"]] = state["state_id"]

    # DropDown
    state = tk.StringVar()
    state, drpDown = window.createDropDown(form, "State", state, stateNameList, 1, 3)

    drpDown.bind("<<ComboboxSelected>>", lambda event: disctrict(event, stateDict[state.get()], window))

def disctrict(event, stateID, frame):
    print(stateID)

    disctrictURL = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/" + str(stateID)

    hdr = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'accept': 'application/json',
            'Accept-Language': 'en_US'
    }

    response = requests.get(disctrictURL, headers=hdr)
    jsonDump = response.text
    JSON = json.loads(jsonDump)
    distList = []
    distNameList = []
    distDict = {}
    for state in JSON["districts"]:
        distList.append((state["district_id"], state["district_name"]))
        distNameList.append(state["district_name"])
        distDict[state["district_name"]] = state["district_id"]

    # District DropDown
    dist = tk.StringVar()
    dist, drpDown = frame.createDropDown(form, "District", dist, distNameList, 1, 4)

    drpDown.bind("<<ComboboxSelected>>", lambda event: dist(event, print(dist)))


#TODO: Alias in byDist(), and restructure it

if __name__ == '__main__':
    window = GUI("CoWin Notifier Configurator", '600x400', 1, 1)
    form = window.createFrane(window.root)
    responseVar = []

    # OS Field
    osVar = tk.StringVar()
    osOptions = [("Linux-Based OS", "linux"), ("Windows", "win")]
    (osLabel, osRadio) = window.createRadioField(form, "OS", osOptions, 1, 0, osVar, None, "os")

    # Dose Field
    doseVar = tk.StringVar()
    doseOptions = [("Dose 1", "d1"), ("Dose 2", "d2")]
    (doseLabel, doseRadio) = window.createRadioField(form, "Dose", doseOptions, 1, 1, doseVar, None, "dose")


    # Age Field
    ageVars = [tk.IntVar(), tk.IntVar()]
    ageOptions = ["18 - 44", "45+"]
    (ageLabel, ageBoxes) = window.createCheckboxField(form, "Age Group", ageOptions, 1, 2, "ageListBool")


    # Radio for Pincode/Disctrict
    loc = tk.StringVar()
    locOptions = [("Pincode", "pin"), ("Discrict", "district")]
    (locLabel, locEntry) = window.createRadioField(form, "Search by", locOptions, 1, 3, loc, lambda: decider(loc.get(), window, locLabel, locEntry), "pin_dist")

    print(window.vars)
    window.root.mainloop()

import tkinter as tk
from tkinter import ttk
from tkinter.constants import E, W
import json

# root

root = tk.Tk()
root.geometry('400x200')
root.resizable(0, 0)
root.title('CoWin Notification Alerts Configurator')

root.columnconfigure(0, weight = 1)

pin = tk.StringVar()
os = tk.StringVar()

def buttonClicked():
    print("Thank you!")
    config = {
        'pin': pin.get(),
        'linux_win': os.get()
    }

    jsonDump = json.dumps(config, indent=2)
    oh = open('config.json', 'w')
    oh.write(jsonDump)

    exit()

form = ttk.Frame(root)
form.pack(padx=10, pady=10, fill='x', expand=True)



# Pin code
pinLabel = tk.Label(form, text='Your Pincode')
pinLabel.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)

pinEntry = tk.Entry(form, textvariable=pin)
pinEntry.grid(column=2, row=0, sticky=tk.E, padx=10, pady=5)
pinEntry.focus()

# OS
osLabel = tk.Label(form, text='OS?')
osLabel.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)

r1 = ttk.Radiobutton(form, text='Linux-based OS', value='linux', variable=os)
r1.grid(column=2, row=1)
r1 = ttk.Radiobutton(form, text='Windows', value='win', variable=os)
r1.grid(column=3, row=1)

print(os)
# Submit
submitButton = tk.Button(form, text="Submit", command=buttonClicked)
submitButton.grid(column=2, row=3, padx=5, pady=20)




root.mainloop()

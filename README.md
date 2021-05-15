# CoWin Notification Automater

Sends you a notification on your desktop if slots are available near you.

## Installation
-   Install ```py-notifier``` using ```pip```
    `$ pip install py-notifier`

-   Install ```playsound``` using ```pip```
    `$ pip install playsound`

#### Linux-bases systems
This script uses ```urllib```, ```amixer```, ```notify-send```, and ```aplay```.
Install them if you don't have them with you.

#### Windows
-   Install ```win10toast``` using ```pip```
    `$ pip install win10toast`

## Requirements
-   A stable internet connection
-   Linux-based OS (Tested on Ubuntu 20.10), 
-   or Windows 10

## Configuration
Confguration file: ```config.json```
-   Change ```pin``` to your desired pincode.
-   Change ```linux_win``` to ```linux``` if you are using linux, else write ```win``` if you are on Windows.

## Running
Open your terminal window. Type the following:-
`$ python3 script.py`

Keep an eye on future developments, as some more features shall be incorporated.

import os
import json

curl_command = "curl -o json.json -X GET  -H \"User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36\"  \"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=457001&date=15-05-2021\""

os.system(curl_command)

fh = open('json.json')
json_data = json.loads(fh.read())
oh = open('data.txt', 'w')
oh_aux = open('aux.json', 'w')



for center in json_data['centers']:
    name = center['name']
    city = center['district_name']
    pin = center['pincode']
    fee_type = center['fee_type']
    min_age = center['sessions'][0]['min_age_limit']
    date = center['sessions'][0]['date']
    availability = center['sessions'][0]['available_capacity']
    vaccine = center['sessions'][0]['vaccine']

    if(availability == 0):
        os.system('notify-send "Slot Available!!" -i "/home/death0hole/Desktop/CoWin/syringe.jpg" -u critical')
        os.system("aplay /home/death0hole/Desktop/CoWin/alert.wav -q")


    oh.write("Center Name")
    oh.write("\t")
    oh.write(name)
    oh.write("\n")

    oh.write("Availability")
    oh.write("\t")
    oh.write(str(availability))
    oh.write("\n")
    
    oh.write("Date")
    oh.write("\t")
    oh.write(date)
    oh.write("\n")
    
    oh.write("Vaccine")
    oh.write("\t")
    oh.write(vaccine)
    oh.write("\n")
    
    oh.write("Min Age")
    oh.write("\t")
    oh.write(str(min_age))
    oh.write("\n")
    oh.write("\n")

    
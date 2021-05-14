import os
import json
import datetime

# service_curl_command = "curl -o json.json -X GET  -H \"User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36\"  \"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=457001&date="

oh = open('data.txt', 'w')
# oh_aux = open('aux.json', 'w')

date_1 = datetime.datetime.now().strftime("%d-%m-%Y")
date_2 = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d-%m-%Y")
date_3 = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%d-%m-%Y")

test_dates = [date_1, date_2, date_3]

while True:
    cont = input("Continue?")
    if(not cont):break


    for test_date in test_dates:
        print(test_date)
        curl_command = "curl -o jsonHolder.json -X GET  -H \"User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36\"  \"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=457001&date=" + test_date + "\""
        os.system(curl_command)

        fhAux = open('jsonHolder.json')
        jsonAux_data = json.loads(fhAux.read())
        
        try:
            aux_var = (jsonAux_data['centers'][0])
        except:
            continue

        os.system("cp jsonHolder.json json.json")

        fh = open('json.json')
        json_data = json.loads(fh.read())

        for center in json_data['centers']:
            name = center['name']
            city = center['district_name']
            pin = center['pincode']
            fee_type = center['fee_type']
            min_age = center['sessions'][0]['min_age_limit']
            date = center['sessions'][0]['date']
            availability = center['sessions'][0]['available_capacity']
            vaccine = center['sessions'][0]['vaccine']


            if(availability == 0):      # Just for testing
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
import os, time
import json
import datetime
import cfg

date_1 = datetime.datetime.now().strftime("%d-%m-%Y")
date_2 = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d-%m-%Y")
date_3 = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%d-%m-%Y")

test_dates = [date_1, date_2, date_3]

def work():
    while True:
        # cont = input("Continue?")
        # if(not cont):break
        time.sleep(5)


        for test_date in test_dates:
            print(test_date)
            curl_command = "curl -o jsonHolder.json -X GET  -H \"User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36\"  \"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=" + str(cfg.constants['pin']) + "&date=" + test_date + "\""
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

            oh = open('data.txt', 'w')

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
                # if(availability > 0):
                    notify(name)

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

            oh.close()


def notify(center_name):
    sysStr = 'notify-send' + ' "' + center_name + ' || Slot Available!!" -i "/home/death0hole/Desktop/CoWin/syringe.jpg" -u critical'
    os.system('amixer -D pulse sset Master 100%')
    os.system(sysStr)
    os.system("aplay /home/death0hole/Desktop/CoWin/alert.wav -q")
    os.system("aplay /home/death0hole/Desktop/CoWin/alert.wav -q")


if __name__ == '__main__':
    work()
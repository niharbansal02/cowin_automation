import urllib.request, urllib.parse, urllib.request
import os, time
import json
import datetime
import cfg
from notifier import Notifier

date_1 = datetime.datetime.now().strftime("%d-%m-%Y")
date_2 = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d-%m-%Y")
date_3 = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%d-%m-%Y")

test_dates = [date_1, date_2, date_3]


def request_data(date):
    service_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?"
    params = {
        'pincode': cfg.constants['pin'],
        'date': date
    }

    hdr = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'accept': 'application/json',
        'Accept-Language': 'en_US'
    }

    URL = service_url + urllib.parse.urlencode(params)
    req = urllib.request.Request(URL, headers=hdr)
    jsonResp = urllib.request.urlopen(req).read()
    return jsonResp.decode()

def work():
    while True:
        # cont = input("Continue?")
        # if(not cont):break
        # time.sleep(5)


        for test_date in test_dates:
            print(test_date)
            jsonStr = request_data(test_date)
            json_data = json.loads(jsonStr)

            try:
                aux_var = (json_data['centers'][0])
            except:
                continue

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


                # if(availability == 0):      # Just for testing
                if(availability > 0):
                    notifObj = Notifier()
                    notifObj.notify("!! Slot Available !!", name)

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

        time.sleep(60)



if __name__ == '__main__':
    # work()
    # print(request_data('15-05-2021'))
    # notify("Nihar")
    # from pynotifier import Notification
    # notify("Vaccine Slot Available", "Yaayy")
    # win_notify("hi Mudit")
    n = Notifier()
    n.notify("Slot", "Hi")
    pass
    

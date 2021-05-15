import urllib.request, urllib.parse, urllib.request
import os, time
import json
import datetime
from notifier import Notifier

class CoWin_alerts:
    test_dates = []
    config_data = {}

    def __init__(self):
        date_1 = datetime.datetime.now().strftime("%d-%m-%Y")
        date_2 = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d-%m-%Y")
        date_3 = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%d-%m-%Y")
        self.test_dates = [date_1, date_2, date_3]
        with open('config.json') as fh:
            self.config_data = json.loads(fh.read())
        # print(self.config_data)

    def request_data(self, date):
        service_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?"
        params = {
            'pincode': self.config_data['pin'],
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

    def work(self):
        while True:
            # cont = input("Continue?")
            # if(not cont):break
            # time.sleep(5)

            for test_date in self.test_dates:
                # print(test_date)
                jsonStr = self.request_data(test_date)
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

                    self.write_in_file(oh, "Center Name", name)
                    self.write_in_file(oh, "Availability", availability)
                    self.write_in_file(oh, "Date", date)
                    self.write_in_file(oh, "Vaccine", vaccine)
                    self.write_in_file(oh, "Min Age", min_age)

                oh.close()

            time.sleep(60)

    def write_in_file(self, fout, head, msg):
        fout.write(head)
        fout.write("\t")
        fout.write(msg)
        fout.write("\n")



if __name__ == '__main__':
    obj = CoWin_alerts()
    obj.work()

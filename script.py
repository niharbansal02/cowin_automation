import urllib.request, urllib.parse, urllib.request
import os, time, pathlib
import json
import datetime
from helper.notifier import Notifier

class CoWin_alerts:
    test_dates = []
    config_data = {}
    projectPath = ""

    def __init__(self):
        date_1 = datetime.datetime.now().strftime("%d-%m-%Y")
        date_2 = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d-%m-%Y")
        date_3 = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%d-%m-%Y")
        self.test_dates = [date_1, date_2, date_3]

        self.projectPath = pathlib.Path(__file__).parent.absolute()
        p = pathlib.PurePath("helper/config.json")
        with open(os.path.join(self.projectPath, p)) as fh:
            self.config_data = json.loads(fh.read())

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

            #TODO: Verify request for age criteria
            for test_date in self.test_dates:
                # print(test_date)
                try:
                    jsonStr = self.request_data(test_date)
                    json_data = json.loads(jsonStr)
                except:
                    print("\033[0;31mHTTP 403 Error\033[0m:", datetime.datetime.now().strftime("%H:%M"), "It's not me, it's the Government. Please be patient.")
                    continue

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
                    notifyAge = False
                    if(self.config_data['18+'] == 1 and min_age == 18):
                        notifyAge = True
                    if(self.config_data['45+'] == 1 and min_age == 45):
                        notifyAge = True

                    # if(availability == 0):      # Just for testing
                    if(availability > 1 and notifyAge):
                        notifObj = Notifier()
                        notifObj.notify("!! Slot Available !!", name)
                        with open("timelogs.txt", 'a+') as th:
                        	th.write(self.test_dates[0])
                        	th.write("\t")
                        	th.write(datetime.datetime.now().strftime("%H:%M"))
                        	th.write("\t")
                        	th.write(name)
                        	th.write("\n")

                    self.write_in_file(oh, "Center Name", name)
                    self.write_in_file(oh, "Availability", str(availability))
                    self.write_in_file(oh, "Date", date)
                    self.write_in_file(oh, "Vaccine", vaccine)
                    self.write_in_file(oh, "Min Age", str(min_age))

                oh.close()

            time.sleep(30)

    def write_in_file(self, fout, head, msg):
        fout.write(head)
        fout.write("\t")
        fout.write(msg)
        fout.write("\n")



if __name__ == '__main__':
    obj = CoWin_alerts()
    obj.work()

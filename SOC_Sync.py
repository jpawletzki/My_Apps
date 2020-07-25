"""
Scenario

*Missing AbuseIPDB API Key - Add for it to run. 

Lets set the scene:

You are a SOAR engineer for a Client A.

Client A has two SOCs and each have a SOAR platform :
One site is in the EST time zone in the United States.
and another site that is in the CET time zone in the Netherlands.

Both SOCs have requested the same app.

The app's purpose is to provide the local time,
and the counterpart SOC's site's time. This will help the analyst by giving a quick dashboard to reference the time
of the other SOC for quality of life instead of having to remember the time difference or look it up constantly.

This will be displayed on the SOAR's dashboard that has the ability to display
outputs of Python scripts.

Instead of creating two separate scripts to maintain, you decide to do it in one that dynamically changes based off
of IP location.

The code:

The current time is based off of the SOAR platform's location via IP address. Ths time zone is determined by
checking the country code the IP is registered in and setting the appropriate timezone needed through
datetime and pytz. The date and time is also parsed out for both timezones of the datetime object and displayed,
and is outputted with the appropriate labels.

ASCII art from "https://www.asciiart.eu/electronics/clocks"
"""

import requests
import re
import json
import time
from datetime import datetime
from pytz import timezone
import sys


class SOCSync:

    def get_system_public_ip(self):
        self.systemPublicIP = requests.get('https://api.ipify.org').text

    def get_system_public_ip_test_input(self, systemPublicIP):
        #Manually input the IP to test program functionality during runtime.
        self.systemPublicIP = systemPublicIP

    def get_system_public_ip_country_code(self):
        while True:
            try:
                #AbuseIPDB API Parameters
                url = 'https://api.abuseipdb.com/api/v2/check'
                querystring = {
                    'ipAddress': self.systemPublicIP,
                    'maxAgeInDays': '90'
                }
                headers = {
                    'Accept': 'application/json',
                    'Key': ''
                }
                self.response = requests.request(method='GET', url=url, headers=headers, params=querystring)
                # Formatted output
                self.decodedResponse = json.loads(self.response.text)
                #Nested JSON. Loading the data section and then grabbing the country code from that section.
                self.data = (self.decodedResponse['data'])
                self.countryCode = self.data['countryCode']
                break
            except:
                print("Error receiving response from AbuseIPDB API, exiting program")
                sys.exit()

    def country_code_test_input(self, countryCode):
        #Manually input the country code to test program functionality during runtime.
        self.countryCode = countryCode

    def parse_country_code(self):
        #We can hard code the country codes and time zone values to match
        #since in a typical production environment NATs are static for these type of systems, and we should get
        #consistant IP results and do not have to worry about it changing. In case of change, modify script.
            if self.countryCode == "US":
                self.timeZone = "EST"
            elif self.countryCode == "NL":
                self.timeZone = "CET"
            else:
                print("Invalid country code, exiting program")
                time.sleep(10)
                sys.exit()

    def return_current_time(self):
        #Parses date and time from datetime in the appropriate time zone
        #No try/except because the expected input is hard coded and if that method fails the program will
        #not make it here
        dateRe = re.compile("....-..-..")
        timeRe = re.compile("[0-9][0-9]:[0-9][0-9]:[0-9][0-9]")

        self.dateEST = (re.search(dateRe, str(datetime.now(timezone("EST")))))[0]
        self.timeEST = (re.search(timeRe, str(datetime.now(timezone("EST")))))[0]
        self.dateCET = (re.search(dateRe, str(datetime.now(timezone("CET")))))[0]
        self.timeCET = (re.search(timeRe, str(datetime.now(timezone("CET")))))[0]
        #Big downfall of this is that it does not account for Daylight Savings with this method so at the time of creation
        #it is less 1 hour, note is added in output
        if self.timeZone == "EST":
            return f"\nThe current time in your time zone ({self.timeZone}) is {self.timeEST} (Add 1 hour for Daylight Savings)\n" \
                   f"The current date in your time zone ({self.timeZone}) is {self.dateEST} (yyyy-mm-dd)\n\n" \
                   f"In the other SOC the time is {self.timeCET}, and the date is {self.dateCET} (yyyy-mm-dd)\n\n"
        else:
            return f"\nThe current time in your time zone ({self.timeZone}) is {self.timeCET}\n" \
                   f"The current date in your time zone ({self.timeZone}) is {self.dateCET} (yyyy-mm-dd)\n\n" \
                   f"In the other SOC, the time is {self.timeEST} (Add 1 hour for Daylight Savings), and the date is {self.dateEST} (yyyy-mm-dd)\n\n"


def run_application():
    Sync = SOCSync()
    Sync.get_system_public_ip()
    Sync.get_system_public_ip_country_code()
    Sync.parse_country_code()
    while True:
        time.sleep(60)
        print(Sync.return_current_time())


def debug_application():
    #Initilizes debug menu and sanitizes input
    Sync = SOCSync()
    testMenuOptions = {"Test IP": "1", "Test Country Code": "2", "Both": "3"}
    for key, value in testMenuOptions.items():
        print(f"\t{key}: {value}")
    selection = input("What would you like to do? ")
    while selection != "1" and selection != "2" and selection != "3":
        print("\n\nEnter a valid menu option\n")
        for key, value in testMenuOptions.items():
            print(f"\t{key}: {value}")
        selection = input("What would you like to do? ")

    if selection == "1":
        debugIP = input("What IP would you like to test ")
        Sync.get_system_public_ip_test_input(debugIP)
        Sync.get_system_public_ip_country_code()
        Sync.parse_country_code()
        print(Sync.return_current_time())

    elif selection == "2":
        debugCountryCode = input("What Country Code would you like to test ")
        Sync.get_system_public_ip()
        Sync.country_code_test_input(debugCountryCode)
        Sync.parse_country_code()
        print(Sync.return_current_time())

    else:
        debugCountryCode = input("What Country Code would you like to test ")
        debugIP = input("What IP would you like to test ")
        Sync.get_system_public_ip_test_input(debugIP)
        Sync.country_code_test_input(debugCountryCode)
        Sync.parse_country_code()
        print(Sync.return_current_time())

    #Deletes object to avoid issues since function reinstates it.
    del Sync

    selection = input("\nEnter 1 to keep debugging\n Enter 2 to return to the main menu\nWhat would you like to do? ")
    while selection != "1" and selection != "2":
        print("\n\nEnter a valid menu option\n")
        for key, value in testMenuOptions.items():
            print(f"{key}: {value}")
        selection = input("\nEnter 1 to keep debugging\nEnter 2 to return to the main menu\nWhat would you like to do? ")
    if selection == "1":
        debug_application()
    else:
        show_main_menu()


# Initializes Main Menu and Object and sanitizes input
def show_main_menu():
    menuOptions = {"Run Application": "1", "Test Application": "2", "Exit": "3"}
    print("        Welcome to\n\n" 
          "        SOC  SYNC")
    print("""
    .'`~~~~~~~~~~~`'.\n
    (  .'11 12 1'.  )\n
    |  :10 \    2:  |\n
    |  :9   @-> 3:  |\n
    |  :8       4;  |\n
    '. '..7 6 5..' .'\n
     ~-------------~ """)
    for key, value in menuOptions.items():
        print(f"\t{key}: {value}")
    print("Warning - This GitHub version will not function if you do not add your AbuseIPDB key to the code")
    selection = input("What would you like to do? ")
    while selection != "1" and selection != "2" and selection != "3":
        print("\n\nEnter a valid menu option\n")
        for key, value in menuOptions.items():
            print(f"\t{key}: {value}")
        selection = input("\nEnter 1 to keep debugging\n Enter 2 to return"
                          " to the main menu\nWhat would you like to do? ")
    if selection == "1":
        run_application()
    elif selection == "2":
        debug_application()
    else:
        sys.exit()

show_main_menu()



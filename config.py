import os
import inspect


PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))+"\\"



num_crackers = 10 #The number of crackers in this folder

passwd_dict = PATH+"words.txt" #Password dictionary

manglers = PATH+"manglers.txt" #Suffixes to be added to the passwords

targets = PATH+"targets.txt"

logs = PATH+"logs.txt"

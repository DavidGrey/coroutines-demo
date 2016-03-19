import os
import inspect


PATH = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))+"\\"

passwd_dict = PATH+"passwds.txt" #Password dictionary

targets = PATH+"targets.txt"

logs = PATH+"logs.txt"

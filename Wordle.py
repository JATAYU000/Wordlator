import mysql.connector as sq
import pickle
global dictionary

def InitializeDB():
    
    f = open('pw_list.dat','rb')
    try:
        while True:
            dictionary = pickle.load(f)
    except:
        f.close()
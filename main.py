from selenium import webdriver
import time,sys
from selenium.webdriver.common.by import By
from pyautogui import press, typewrite, hotkey
import mysql.connector as sq
import pickle
from PIL import Image
from io import BytesIO

# pixel position of each word
position = {"00":[800,390],"01":[865,390],"02":[931,390],"03":[1000,390],"04":[1065,390],
            "10":[800,456],"11":[865,456],"12":[931,456],"13":[1000,456],"14":[1065,456],
            "20":[800,527],"21":[865,527],"22":[931,527],"23":[1000,527],"24":[1065,527],
            "30":[800,593],"31":[865,593],"32":[931,593],"33":[1000,593],"34":[1065,593],
            "40":[800,662],"41":[865,662],"42":[931,662],"43":[1000,662],"44":[1065,662],
            "50":[800,731],"51":[865,731],"52":[931,731],"53":[1000,731],"54":[1065,731]}

# rgb values of green, yellow and grey
rgb = {"green":(83,141,78,255),"yellow":(181, 159, 59, 255),"grey":(58, 58, 60, 255)}


def is_database_empty(con):
    c1 = con.cursor()
    c1.execute('select count(*) from word_list')
    test = c1.fetchall()
    for l in test:
        for k in l:
            return k

def no_letters(con,s):
    k = is_database_empty(con)
    if k == 0:
        o = ''
        p = 0
        while p < len(s)-1:
            o = o + "'"+s[p]+"'"+' not in i and '
            p = p +1
        o = o +"'"+s[len(s)- 1]+"'"+' not in i'
        try:
            for i in dictionary:
                exec('if '+o+':'+"""\n\tqry = 'insert into word_list values (%s)'\n\tc2 = con.cursor()\n\tc2.execute(qry,(i,))\n\tcon.commit()""")
        except:
            pass
    else:
        qry2 = 'delete from word_list where words like %s'+' or words like %s'+' or words like %s'
        c3 = con.cursor()
        for y in s:
            j = '%'+y+'%'
            k = y+'%'
            l = '%'+y
            m = (j,k,l)
            c3.execute(qry2,m)

    free_dict()

def yes_letters(t,con):
    k = is_database_empty(con)
    if k == 0:
        o = ''
        p = 0
        while p < len(t)-1:
            o = o + "'"+t[p]+"'"+' in i and '
            p = p +1
        o = o +"'"+t[len(t)- 1]+"'"+' in i'
        try:
            for i in dictionary:
                exec('if '+o+':'+"""\n\tqry = 'insert into word_list values (%s)'\n\tc6 = con.cursor()\n\tc6.execute(qry,(i,))\n\tcon.commit()""")
        except:
            pass
    else:
        qry2 = 'delete from word_list where words not like %s'+' and words not like %s'+' and words not like %s'+' and words not like %s'+' and words not like %s'
        c3 = con.cursor()
        for y in t:
            j = y+'____'
            k = '_'+y+'___'
            l = '__'+y+'__'
            a = '___'+y+'_'
            b = '____'+y
            m = (j,k,l,a,b)
            c3.execute(qry2,m)

    free_dict()


def free_dict():
    try:
        del dictionary
    except:
        pass

def out_pos_letter(con,s):
    if s == "_____": return
    d = {}
    t = []
    for i in range(len(s)):
        d[i] = s[i]
        if s[i] != '_':
            t.append(s[i])      
    yes_letters(t,con)

    for x in d:
        if d[x] == '_':
            continue
        else:
            if x == 0:
                c = d[0]+'____'
                y_d(c,con)
            elif x == 1:
                c = '_'+d[1]+'___'
                y_d(c,con)
            elif x == 2:
                c = '__'+d[2]+'__'
                y_d(c,con)
            elif x == 3:
                c = '___'+d[3]+'_'
                y_d(c,con)
            else:
                c = '____'+d[4]
                y_d(c,con)

def y_d(c,con):
    qry78 = 'delete from word_list where words like %s'
    c700 = con.cursor()
    c700.execute(qry78,(c,))

def pos_letters(con,s):
    k = is_database_empty(con)
    if k == 0:
        pass
    else:
        qry3 = 'delete from word_list where words not like %s'
        c8 = con.cursor()
        c8.execute(qry3,(s,))


def suggest_word(con):
    k = is_database_empty(con)
    if k == 0:
        return [('rates',0)]
    else:
        return s_l_w(con)

def s_l_w(con):
    global wer
    qry4 = 'select * from word_list'
    c10 = con.cursor()
    c10.execute(qry4)
    lol = c10.fetchall()
    wer = []
    if len(lol) == 1:
        return [lol[0]]
        # quit_p()
    for e in range(len(lol)):
        wer.append((lol[e][0]))
    del lol
    return ind_count(wer)

def quit_p(con):
    k = is_database_empty(con) 
    if k != 0:
        clear_data(con)
        print('\nTHANK YOU FOR USING THE PROGRAM')
        exit()
    else:
        print('\nTHANK YOU FOR USING THE PROGRAM')
        exit()

def clear_data(con):
    c20 = con.cursor()
    c20.execute('delete from word_list')
    con.commit()
    print('\nDATABASE CLEARED SUCESSFULLY')

def ind_count(wer):
    global pos_d
    pos_d = {}
    for d in wer: 
        for i , j in enumerate(d):
            if j in pos_d:
                pos_d[j][i] += 1
            else:
                pos_d[j] = [0,0,0,0,0]
                pos_d[j][i] += 1

    return get_word_by_pos(pos_d)

def get_word_by_pos(pos_d):
    pars_d = ()
    for y in range(5):
        top = len(pos_d)
        l = []
        for i in pos_d:
            w = pos_d[i][y]
            if l == []:
                l.append((i,w))
            else:
                if w > l[0][1]:
                    l.append((i,w))
                    l.pop(0)
            top = top - 1
            if top == 0:
                pars_d = pars_d + (l[0][0],)
                
    return make_word(pars_d)

def make_word(q):
    disp = []
    max_index = []
    for g in wer:
        count = 0
        if g[0] == q[0]:
            count += 1
        if g[1] == q[1]:
            count += 1
        if g[2] == q[2]:
            count += 1
        if g[3] == q[3]:
            count += 1
        if g[4] == q[4]:
            count += 1
        if count > 2:
            disp.append((g,count))
            if count not in max_index:
                max_index.append(count)
    out = []
    for w in disp:
        if w[1] == 5 or w[1] == 4 or w[1] == max(max_index):
            out.append(w)
    return out


def check_if_database_is_empty(con):
    k = is_database_empty(con)
    if k != 0:
        c = con.cursor()
        c.execute('delete from word_list')
        con.commit()

def launchBrowser():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    time.sleep(1)
    driver.get("https://www.nytimes.com/games/wordle/index.html")
    return driver


def CloseInitialWindow(driver):
    button = driver.find_element(By.CSS_SELECTOR,"button[data-testid='Play']")
    button.click()
    time.sleep(1)
    button = driver.find_element(By.CSS_SELECTOR,"button[class='Modal-module_closeIcon__TcEKb']")
    button.click()
    time.sleep(1)

def EnterWord(word,driver):
    press(word[0])
    press(word[1])
    press(word[2])
    press(word[3])
    press(word[4])
    hotkey('enter')
    time.sleep(2)
    return

def AnalyzeEntry(driver,con,row,word):
    word = word.upper()
    green = ""
    yellow = ""
    grey = ""
    img = driver.get_screenshot_as_png()
    img = Image.open(BytesIO(img)) 
    for i in range(0,5):
        px = img.getpixel(position[str(row)+str(i)])
        if px == rgb['green']:
            green += word[i]
            yellow +="_"
        elif px == rgb['yellow']:
            yellow += word[i]
            green+="_"
        elif px == rgb['grey']:
            grey = grey + word[i]
            green+='_'
            yellow+="_"
    if "_" not in green:
        return "completed"
    no_letters(con,grey)
    pos_letters(con,green)
    out_pos_letter(con,yellow)
    words = suggest_word(con)
    ind=0
    for i in range(len(words)):
        if word[ind]>word[i]:ind = i
    return words[i][0]

def Login(driver,username,pasword):
    return

def main():
    global position,dictionary

    print("""\n\n

    __      _____  _ __ __| |    ___ _ __ __ _  ___| | __   |___ \        ___
    \ \ /\ / / _ \| '__/ _` |   / __| '__/ _` |/ __| |/ /     __) |      / _ \ 
     \ V  V / (_) | | | (_| |  | (__| | | (_| | (__|   <     / __/   _  | (_) |
      \_/\_/ \___/|_|  \__,_|   \___|_|  \__,_|\___|_|\_\   |_____| |_|  \___/

    \n""")

    # Initialisation
    psswrd = input("Enter mysql password: ")
    choice = input("Do you want to login or play anonymous? (y/n):")
    con = sq.connect(host = 'localhost', user = 'jatayu', password = psswrd, database = 'wordle_crack' )
    
    print("Dont minimise the browser be afk and enjoy!")
    time.sleep(1)

    # Updating dictionary with wordlist
    f = open('./pw_list.dat','rb')
    try:
        while True:
            dictionary = pickle.load(f)
    except:
        f.close()

    # Initialising Browseer
    driver = launchBrowser()
    if(choice.lower() in ["y","yes"]):
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        Login(driver,username,password)
    elif(choice.lower() in ["n","no"]):
        CloseInitialWindow(driver=driver)
    w = driver.get_window_size()['width']/2
    position = {"00":[w-160,390],"01":[w-95,390],"02":[w-29,390],"03":[w+40,390],"04":[w+105,390],
            "10":[w-160,456],"11":[w-95,456],"12":[w-29,456],"13":[w+40,456],"14":[w+105,456],
            "20":[w-160,527],"21":[w-95,527],"22":[w-29,527],"23":[w+40,527],"24":[w+105,527],
            "30":[w-160,593],"31":[w-95,593],"32":[w-29,593],"33":[w+40,593],"34":[w+105,593],
            "40":[w-160,662],"41":[w-95,662],"42":[w-29,662],"43":[w+40,662],"44":[w+105,662],
            "50":[w-160,731],"51":[w-95,731],"52":[w-29,731],"53":[w+40,731],"54":[w+105,731]}
    
    newWord = 'rates'
    for i in range(6):
        EnterWord(newWord,driver)
        newWord = AnalyzeEntry(driver,con,i,newWord)
        if(newWord == "completed"):
            print("Thank you for using Wordlator :D")
            break
    return
    
if __name__ == '__main__':
    main()
from selenium import webdriver
import time 
from selenium.webdriver.common.by import By
from pyautogui import press, typewrite, hotkey
import mysql.connector as sq
import pickle
global con,dictionary

def Initialize():
    psswrd = input("Enter password: ")
    con = sq.connect(host = 'localhost', user = 'jatayu', password = psswrd, database = 'wordle_crack' )
    print(con)
    f = open('pw_list.dat','rb')
    try:
        while True:
            dictionary = pickle.load(f)
    except:
        f.close()

def is_database_empty():
    c1 = con.cursor()
    c1.execute('select count(*) from word_list')
    test = c1.fetchall()
    for l in test:
        for k in l:
            return k

def no_letters():
    s = input('Enter the letter(s) not present in the word : ')
    k = is_database_empty()
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

def yes_letters(t):
    k = is_database_empty()
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

def out_pos_letter():
    d = {}
    t = []
    s = input('Enter the letter(s) where they are out of positions ( _ where letter not known) : ')
    for i in range(len(s)):
        d[i] = s[i]
        if s[i] != '_':
            t.append(s[i])      
    yes_letters(t)

    for x in d:
        if d[x] == '_':
            continue
        else:
            if x == 0:
                c = d[0]+'____'
                y_d(c)
            elif x == 1:
                c = '_'+d[1]+'___'
                y_d(c)
            elif x == 2:
                c = '__'+d[2]+'__'
                y_d(c)
            elif x == 3:
                c = '___'+d[3]+'_'
                y_d(c)
            else:
                c = '____'+d[4]
                y_d(c)

def y_d(c):
    qry78 = 'delete from word_list where words like %s'
    c700 = con.cursor()
    c700.execute(qry78,(c,))

def pos_letters():
    k = is_database_empty()
    if k == 0:
        print('\nPlease complete either option 1 or 2')
    else:
        s = input('Enter the letter(s) with their correct positions ( _ where letter not known) : ')
        qry3 = 'delete from word_list where words not like %s'
        c8 = con.cursor()
        c8.execute(qry3,(s,))


def suggest_word():
    k = is_database_empty()
    if k == 0:
        print('RATES or SALET')
    else:
        s_l_w()

def s_l_w():
    global wer
    qry4 = 'select * from word_list'
    c10 = con.cursor()
    c10.execute(qry4)
    lol = c10.fetchall()
    wer = []
    if len(lol) == 1:
        return lol[0]
        quit_p()
    for e in range(len(lol)):
        wer.append((lol[e][0]))
    del lol
    ind_count(wer)

def quit_p():
    k = is_database_empty() 
    if k != 0:
        clear_data()
        print('\nTHANK YOU FOR USING THE PROGRAM')
        exit()
    else:
        print('\nTHANK YOU FOR USING THE PROGRAM')
        exit()

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

    get_word_by_pos(pos_d)

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
                
    make_word(pars_d)

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

    display_sugg_words(disp,max_index)

def display_sugg_words(disp,max_index):
    for w in disp:
        if w[1] == 5 or w[1] == 4 or w[1] == max(max_index):
            print(w)

def check_if_database_is_empty():
    k = is_database_empty()
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

def EnterWord(driver):
    press('c')
    press('r')
    press('u')
    press('s')
    press('h')
    time.sleep(1)
    return

def main():
    # entry point
    # driver = launchBrowser()
    # CloseInitialWindow(driver=driver)
    Initialize()

    return
    
if __name__ == '__main__':
    main()
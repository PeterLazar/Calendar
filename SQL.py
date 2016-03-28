import sqlite3 as lite

# TODO pr save event... ce ni subjecta, vrni neko napako al neki


# prejsnja verzija:
#(ID,d,m,y,subj,desc,h:m,notify,weekday,repeat,repDays,repUntil,show)
# se mi zdi
################################################################
def create_events():
    # Options.db file must not exist!
    con = lite.connect('Events.db')
    with con:
        cur = con.cursor()
        # dateChanged    - "YYYY-MM-DD HH:MM:SS"  datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # repeat         - one of [none,daily, weekly, monthly, anualy, custom]
        # repeatWeekdays - tuple containing weekday numbers eg. "(1,3,4)"
        # repeatUntil    - tuple "(yyyy,mm,dd)"
        # show           - boolean
        # notify         - boolean
        cur.execute('''CREATE TABLE Events(Id INTEGER PRIMARY KEY,
                       dateChanged TEXT,
                       subject TEXT,
                       description TEXT,
                       year INTEGER,
                       month INTEGER,
                       day INTEGER,
                       h_m TEXT,
                       repeat TEXT,
                       repeatWeekdays TEXT,
                       repeatUntil TEXT,
                       show INTEGER,
                       notify INTEGER)''')

def save_event(dateChanged,subject,description,year,month,day,h_m,repeat='None',repeatWeekdays='()',repeatUntil='(,,)',show=1,notify=0):
##    print dateChanged,subject,year,month,day,h_m
    if subject == '':
        print('No subject!')
        return 0
    con = lite.connect('Events.db')
    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM Events WHERE year='+str(year)+' AND month='+str(month)+' AND day= '+str(day)+' AND h_m="'+str(h_m)+'" AND subject="'+subject+'"')
        test = cur.fetchall()
        if test: return 0 # event ze obstaja, zato ne shranimo nic
        cur.execute('INSERT INTO Events(dateChanged,subject,description,year,month,day,h_m,repeat,repeatWeekdays,repeatUntil,show,notify) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (dateChanged,subject,description,year,month,day,h_m,repeat,repeatWeekdays,repeatUntil,show,notify))

def change_event_id(id, names, values):
    # id - id of event
    # name - tuple of names of values to change
    # value - new values for corresponding names
    if len(names) != len(values): return 0
    if len(names) == 0: return 0
    changes = ''
    for i in range(len(names)):
        if type(values[i]) == type(''):
            changes = changes + str(names[i])+'="'+str(values[i])+'", '
        else:
            changes = changes + str(names[i])+'='+str(values[i])+', '
    changes = changes[:-2]+' '
    print('UPDATE Events set '+changes+'WHERE Id = '+str(id))
    con = lite.connect('Events.db')
    with con:
        cur = con.cursor()
        cur.execute('UPDATE Events set '+changes+'WHERE Id = '+str(id))

def delete_event_id(id):
    print(id)
    con = lite.connect('Events.db')
    with con:
        cur = con.cursor()
        cur.execute('DELETE FROM Events WHERE Id = '+str(id))

def get_events_day(year,month,day):
    # TODO check everything
    con = lite.connect('Events.db')
    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM Events WHERE year='+str(year)+' AND month='+str(month)+' AND day='+str(day))
        out = cur.fetchall()
    out2 = dict()
    for i in out:
        if out2.get(int(i[7][:2])): out2[int(i[7][:2])].append(i)
        else: out2[int(i[7][:2])] = [i]
    return out2

def get_events_month(year,month,day_first,day_last):
    # TODO repeating events not implemented yet i think

    # for display on main window
    # day_first - month day of the first day of the previous month, that is displayed
    # day_last - month day of the last day of the next month, that is displayed
    con = lite.connect('Events.db')
    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM Events WHERE year='+str(year if month!=1 else year-1)+' AND month='+str(month-1 if month!=1 else 12)+' AND day>='+str(day_first))
        out = cur.fetchall()
        cur.execute('SELECT * FROM Events WHERE year='+str(year)+' AND month='+str(month))
        out += cur.fetchall()
        cur.execute('SELECT * FROM Events WHERE year='+str(year if month!=12 else year+1)+' AND month='+str(month+1 if month!=12 else 1)+' AND day<='+str(day_last))
        out += cur.fetchall()

    out2 = dict()
    for i in out:
        try:
            # (year, month, day)
            out2[(i[4],i[5],i[6])] += [i]
##            out2[(int(i[4]),int(i[5]),int(i[6]))] += [i]
        except:
            out2[(i[4],i[5],i[6])] = [i]
##            out2[(int(i[4]),int(i[5]),int(i[6]))] = [i]
            
    return out2
    




################################################################
################################################################
def create_options():
    # Options.db file must not exist!
    con = lite.connect('Options.db')
    with con:
        cur = con.cursor()
        cur.execute('''CREATE TABLE Colors(Id INTEGER PRIMARY KEY,
                       color1 TEXT,
                       color2 TEXT,
                       color3 TEXT,
                       color4 TEXT,
                       color5 TEXT,
                       color6 TEXT)''')
        cur.execute('INSERT INTO Colors(color1,color2,color3,color4,color5,color6)VALUES (?,?,?,?,?,?)', ('#808080', '#cfcfcf', '#ffffff', '#808080', '#ffffff', '#ffffff'))

        cur.execute('''CREATE TABLE ColorScheme(Id INTEGER PRIMARY KEY,
                       name TEXT,
                       color1 TEXT,
                       color2 TEXT,
                       color3 TEXT,
                       color4 TEXT,
                       color5 TEXT,
                       color6 TEXT)''')
        cur.execute('INSERT INTO ColorScheme(name,color1,color2,color3,color4,color5,color6)VALUES (?,?,?,?,?,?,?)', ('The Grey','#808080', '#cfcfcf', '#ffffff', '#808080', '#ffffff', '#ffffff'))

        cur.execute('''CREATE TABLE Misc(Id INTEGER PRIMARY KEY,
                       width INTEGER,
                       height INTEGER,
                       title INTEGER,
                       x INTEGER,
                       y INTEGER,
                       alpha INTEGER,
                       mouse INTEGER,
                       del INTEGER)''')
        cur.execute('INSERT INTO Misc(width,height,title,x,y,alpha,mouse,del) VALUES (?,?,?,?,?,?,?,?)', (80,60,20,10,10,80,1,0))

################################################################
def get_misc():
    con = lite.connect('Options.db')
    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM Misc')
        misc = cur.fetchall()[0][1:]
    return misc

def save_misc(width,height,title,x,y,alpha,mouse,delete):
    con = lite.connect('Options.db')
    with con:
        cur = con.cursor()

        cur.execute('DELETE FROM Misc WHERE Id = 1')
        cur.execute('INSERT INTO Misc(width,height,title,x,y,alpha,mouse,del) VALUES (?,?,?,?,?,?,?,?)', (width,height,title,x,y,alpha,mouse,delete))


################################################################
def change_colors_sql(colors):
    con = lite.connect('Options.db')
    with con:
        cur = con.cursor()

        cur.execute('DELETE FROM Colors WHERE Id = 1')
        cur.execute('INSERT INTO Colors(color1,color2,color3,color4,color5,color6)VALUES (?,?,?,?,?,?)', colors)

def get_colors():
    con = lite.connect('Options.db')
    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM Colors')
        colors = cur.fetchall()[0][1:]
    return colors

def save_color_scheme(name,colors):
    con = lite.connect('Options.db')
    with con:
        cur = con.cursor()
        cur.execute('INSERT INTO ColorScheme(name,color1,color2,color3,color4,color5,color6)VALUES (?,?,?,?,?,?,?)', [name]+colors)

def delete_color_scheme(id):
    con = lite.connect('Options.db')
    with con:
        cur = con.cursor()
        cur.execute('DELETE FROM ColorScheme WHERE Id = '+str(id))

def get_colors_schemes():
    con = lite.connect('Options.db')
    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM ColorScheme')
        schemes = cur.fetchall()

    return schemes

##def get_colors_scheme(id):
##    con = lite.connect('Options.db')
##    with con:
##        cur = con.cursor()
##        cur.execute('SELECT * FROM ColorScheme WHERE Id = '+str(id))
##        colors = cur.fetchall()[0]
##
##        cur.execute('DELETE FROM Colors WHERE Id = 1')
##        cur.execute('INSERT INTO Colors(color1,color2,color3,color4,color5,color6)VALUES (?,?,?,?,?,?)', colors[2:])
##    return colors


def get():
    con = lite.connect('Events.db')
    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM Events')
        out = cur.fetchall()
    for i in out:print(i)
##    return out

if __name__ == '__main__':
    try:
        create_options()
    except:
        pass
    try:
        create_events()
    except:
        pass
##    get()
    



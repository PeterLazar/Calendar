from Tkinter import *
import tkFont as font
from math import cos, sin, pi
from datetime import datetime, date, timedelta
import os
import win32gui

from SQL import *
from EMClass import EventManagerWindow
from tooltip import ToolTip
from options import options_window

# add a timeout timer to change back to current month (when not on it)- 5 min
# TODO:

root = Tk()
root.overrideredirect(True)
root.title('II')

def dummy_draw_month(month,year,today):
    #place holder function to be passed to Event manager window,
    #so we can redraw main window.
    #We use it to avoid wierd code order of definitions
    draw_month(month,year,today)
    

event_manager_window = EventManagerWindow(root, dummy_draw_month)
opt_window = False

month_names = ['January','February','March','April','May','June','July','August','September','October','November','December']

(box_width, box_height, title_height,x,y,alpha,mouse,delete) = get_misc()
x_pos,y_pos = StringVar(), StringVar()
x_pos.set(str(x));y_pos.set(str(y))
root.attributes('-alpha', alpha/100.0)
root.geometry('+%s+%s' % (x, y))
(color1,color2,color3,color4,color5,color6) = get_colors()

today = datetime.now()
(day, month, year) = (today.day, today.month, today.year)
disp_month, disp_year = month, year
weekday = today.isoweekday()-1


## update calendar at midnight ###########################################
## hopefully... didnt want to check every second if new day
def new_day():
    global today, day, month, year, disp_month, disp_year, weekday
    today = datetime.now()
    (day, month, year) = (today.day, today.month, today.year)
    disp_month, disp_year = month, year
    weekday = today.isoweekday()-1

    draw_month(month,year,today)

    root.after(24 * 60 * 60 * 1000, new_day)

seconds_to_next_day = ((23 - today.hour)*60 + (59 - today.minute))*60 + 60 - today.second
root.after(seconds_to_next_day *1000, new_day)
###############################################################################







canvas = Canvas(root, width = box_width*7+1, height = box_height*6+2*title_height+1, highlightthickness=0)
canvas.pack()
tt = ToolTip(canvas,[],[], root.winfo_screenwidth(), root.winfo_screenheight())

## header #########################################
header1 = [
canvas.create_rectangle(0,0,box_width*7,title_height, fill = color1),
canvas.create_rectangle(0,title_height,box_width*7,2*title_height, fill = color1)]

header2 = [
canvas.create_line(title_height*2/10,title_height*2/10,title_height*8/10,title_height*8/10, width = title_height//10+1, fill = color6),
canvas.create_line(title_height*2/10,title_height*8/10,title_height*8/10,title_height*2/10, width = title_height//10+1, fill = color6),

canvas.create_polygon(5*box_width+title_height/3*cos(0),title_height/2+title_height/3*sin(0),5*box_width+title_height/3*cos(pi*2/3),title_height/2+title_height/3*sin(pi*2/3),5*box_width+title_height/3*cos(2*pi*2/3),title_height/2+title_height/3*sin(2*pi*2/3), fill = color6),
canvas.create_polygon(2*box_width-title_height/3*cos(0),title_height/2-title_height/3*sin(0),2*box_width-title_height/3*cos(pi*2/3),title_height/2-title_height/3*sin(pi*2/3),2*box_width-title_height/3*cos(2*pi*2/3),title_height/2-title_height/3*sin(2*pi*2/3), fill = color6),
canvas.create_rectangle(box_width*7-title_height*83/100,title_height*4/7,box_width*7-title_height*4/10,title_height*8/10, fill = color6, outline = color6),
canvas.create_polygon(box_width*7-title_height,title_height*4/7,box_width*7-title_height*2/10,title_height*4/7,box_width*7-title_height*6/10,title_height*1/8, fill = color6)]

month_year_title = canvas.create_text(7/2.0*box_width,title_height/2.0, text = 'Month, Year',font=('TkDefaultFont',min(-9,-title_height+2),'bold'), fill = color6)

for i,j in enumerate(['Mo','Tu','We','Th','Fr','Sa','Su']):
    header2.append(canvas.create_text(box_width*(i+.5),title_height*3/2.0, font=('TkDefaultFont',min(-title_height+4,-9),'bold'), text = j, fill = color6))


def change_header_colors():
    for i in header1:
        canvas.itemconfigure(i, fill = color1)
    for i in header2:
        canvas.itemconfigure(i, fill = color6)
        try:
            canvas.itemconfigure(i, outline = color6)
        except: continue
## body ###############################################
# initialize, add correct values later

rectangles = []
day_numbers = []
for i in range(6*7):
    rectangles.append(canvas.create_rectangle((i%7)*box_width,2*title_height+(i//7)*box_height,(i%7 +1)*box_width,2*title_height+(i//7 +1)*box_height, fill='brown'))
    day_numbers.append(canvas.create_text((i%7)*box_width+5,5+2*title_height+(i//7)*box_height,text=str(i), font=('TkDefaultFont',10), anchor=NW))
day_marker = 0 # holder for the outline marking current day

#####################################################

def make_tooltip_text(events):
    l = len(events)
    if l == 1:
        out = events[0][2]+' '
    else:
        out = ''
        for i in range(l):
            out = out+str(i+1)+'/'+str(l)+' '+events[i][2]+'\n'
    return out[:-1]
        

def make_text(d,events, weight1):
    out = ' '+str(d) + '\n'

    font1 = font.Font(family='TkDefaultFont', size=10, weight=weight1)
    h = font1.metrics("linespace")
    max_lines = int(box_height/h)
    
    if events:
        l = len(events)
        if l == 1:
            line = ''
            for j in events[0][2]:
                line += j
                if font1.measure(line) > box_width:
                    line = line[:-2]+'..'
                    break
            out = out + line + '\n'
        else:
            for i in range(min(l,max_lines-1)):
                line = str(i+1)+'/'+str(l)+' '
                for j in events[i][2]:
                    line += j
                    if font1.measure(line) > box_width:
                        line = line[:-2]+'..'
                        break
                out = out+line+'\n'
    return out[:-1]

timeout_timer = None

def draw_month(month,year,today):
    global disp_month, disp_year, day_marker, tt, timeout_timer
    tt.child, tt.text = [], [] # zbisemo prejsnje tooltipe
    disp_month, disp_year = month, year
    canvas.delete(day_marker)

    first_of_month = datetime(year,month,1).isoweekday()-1
    days_in_month = (date(year if month != 12 else year+1, month+1 if month != 12 else 1,1) - timedelta(days=1)).day

    ldlm = (date(year, month,1) - timedelta(days=1)).day # last day of last month
    canvas.itemconfigure(month_year_title, text = month_names[month-1]+', '+str(year), fill = color6)

    events = get_events_month(disp_year, disp_month, ldlm-(first_of_month)+1,6*7-(first_of_month + days_in_month-1))

    font1 = font.Font(family='TkDefaultFont', size=8, weight='normal')
    font2 = font.Font(family='TkDefaultFont', size=8, weight='bold')
    for i in range(6*7):
        if i < first_of_month:
            d = ldlm-(first_of_month-i)+1
            ev = events.get((year-1, 12, d) if month == 1 else (year, month-1, d))
            if ev: tt.child.append(rectangles[i]); tt.text.append(make_tooltip_text(ev))

            canvas.itemconfigure(rectangles[i], fill=color2)
            canvas.itemconfigure(day_numbers[i], text=make_text(d,ev,'normal'), font=font1, fill=color4)
        elif i > first_of_month + days_in_month-1:
            d = i-(first_of_month + days_in_month-1)
            ev = events.get((year+1, 1, d) if month == 12 else (year, month+1, d))
            if ev: tt.child.append(rectangles[i]); tt.text.append(make_tooltip_text(ev))

            canvas.itemconfigure(rectangles[i], fill=color2)
            canvas.itemconfigure(day_numbers[i], text=make_text(d,ev,'normal'), font=font1, fill=color4)
        else:
            d = i-first_of_month+1
            ev = events.get((year, month, d))
            if ev: tt.child.append(rectangles[i]); tt.text.append(make_tooltip_text(ev))

            canvas.itemconfigure(rectangles[i], fill=color1)
            canvas.itemconfigure(day_numbers[i], text=make_text(d,ev,'bold'), font=font2, fill=color3)
    if (today.month, today.year) == (month, year):
        i = first_of_month + today.day - 1
        day_marker = canvas.create_rectangle((i%7)*box_width,2*title_height+(i//7)*box_height,(i%7 +1)*box_width,2*title_height+(i//7 +1)*box_height, width=3, outline='red')
    else:
        # go back to current month after some time
        if timeout_timer:
            timeout_timer.active = False
            del timeout_timer
        timeout_timer = Timeout(root)
        

class Timeout():
    def __init__(self, root):
        self.active = True
        root.after(5 * 60 * 1000, self.redraw)

    def redraw(self):
        if self.active:
            print 1
            today = datetime.now()
            draw_month(today.month, today.year, today)

draw_month(month,year,today)


def StartMove(event):
    global win_x, win_y
    win_x = event.x
    win_y = event.y

def StopMove(event):
    global win_x, win_y
    win_x, win_y = None, None

def OnMotion(event):
    global win_x, win_y
    deltax = event.x - win_x
    deltay = event.y - win_y
    x = root.winfo_x() + deltax
    y = root.winfo_y() + deltay
    x_pos.set(str(x))
    y_pos.set(str(y))
    root.geometry('+%s+%s' % (x, y))

def move_fnc(move):
##    print(move)
    if move:
        root.bind('<ButtonPress-1>', StartMove)
        root.bind('<ButtonRelease-1>', StopMove)
        root.bind('<B1-Motion>', OnMotion)
    else:
        try:
            root.unbind('<ButtonPress-1>')
            root.unbind('<ButtonRelease-1>')
            root.unbind('<B1-Motion>')
        except:
            pass

def bye(x):
    root.destroy()

def month_up(*args):
    if disp_month == 12: draw_month(1, disp_year+1,today)
    else: draw_month(disp_month+1, disp_year,today)
    
def month_down(*args):
    if disp_month == 1: draw_month(12, disp_year-1,today)
    else: draw_month(disp_month-1, disp_year,today)

def mouse_wheel(event):
    if event.delta == -120:
        month_up()
    if event.delta == 120:
        month_down()

def click(event):
    x,y = event.x, event.y
    if y <= title_height:
        if x < title_height:
            bye(1)
        elif x > 1.8*box_width and x < 2.2*box_width:
            month_down()
        elif x > 4.8*box_width and x < 5.2*box_width:
            month_up()

def double_click(event):
##    global event_manager_window
    x,y = event.x, event.y
    if y <= title_height:
        if x > 7*box_width - title_height:
            draw_month(today.month, today.year, today)
        return 0 #end function

    if y > 2*title_height:

        y = y - 2*title_height
        num = y//box_height *7 + x//box_width

        first_of_month = datetime(disp_year,disp_month,1).isoweekday()-1
        days_in_month = (date(disp_year if disp_month != 12 else disp_year+1, disp_month+1 if disp_month != 12 else 1,1) - timedelta(days=1)).day
##        event_manager_window = True

        if num < first_of_month:
            ldlm = (date(disp_year, disp_month,1) - timedelta(days=1)).day # last day of last month
            day = ldlm-(first_of_month-num)+1
            month = disp_month-1 if disp_month != 1 else 12
            year = disp_year if disp_month != 1 else disp_year-1
            event_manager_window.change_day(year, month, day, True)
##            event_manager(event_manager_window, day, month, year, event_manager_close)
        elif num > first_of_month + days_in_month-1:
            day = num-(first_of_month + days_in_month-1)
            month = disp_month+1 if disp_month != 12 else 1
            year = disp_year if disp_month != 12 else disp_year+1
            event_manager_window.change_day(year, month, day, True)
##            event_manager(event_manager_window, day, month, year, event_manager_close)
        else:
            day = num-first_of_month+1
            event_manager_window.change_day(disp_year, disp_month, day, True)
##            event_manager(event_manager_window, day, disp_month, disp_year, event_manager_close)
##        print(event_manager_window)

def event_manager_close(month, year, today, save = False):
    global event_manager_window
    event_manager_window.root.withdraw()
    if save:
        draw_month(month, year, today)

def opt_win_close():
    global opt_window
    opt_window = False

def change_colors(colors):
    global color1,color2,color3,color4,color5,color6
    (color1,color2,color3,color4,color5,color6) = colors
    change_header_colors()
    draw_month(disp_month,disp_year,today)



def open_options(event):
    global opt_window
    if opt_window: return 0
    opt_window = True
    options_window(root, change_colors, move_fnc, opt_win_close, x_pos,y_pos)

   



######################################################################
hwnds = []
self = 0
screen_size = (0,0,root.winfo_screenwidth(), root.winfo_screenheight())
hwnd1 = 0
flag = 0

def on_top():
    global flag
    root.attributes('-topmost',1)
    root.attributes('-topmost',0)
    flag = 1

def bottom():
    # win32con.SWP_SHOWWINDOW|win32con.SWP_NOMOVE | win32con.SWP_NOSIZE = 67
    # win32con.HWND_BOTTOM = 1
    global self
    win32gui.SetWindowPos(self, 1,0,0,0,0, 67)

def enumHandler(hwnd, lParam):
    global hwnds
    if win32gui.IsWindowVisible(hwnd):
        hwnds.append(hwnd)

def gen_name(*args):
    global hwnds,hwnd1, flag
    hwnds = []
    win32gui.EnumWindows(enumHandler, None)

    for i in range(2,hwnds.index(self)):
        try:
            if win32gui.GetWindowRect(hwnds[i]) == screen_size and win32gui.GetWindowText(hwnds[i])=='':
                hwnd1 = hwnds[2]
                on_top()
        except:
            # okno obstaja, ko uporabiš EnumWindows, a je že uniceno, ko kliceš GetWindowRect
            continue

    if flag and hwnd1 not in hwnds:
        bottom()
        flag = 0

    root.after(150, gen_name)


def enumHandler2(hwnd, lParam):
    global self, hwnd1
    if win32gui.IsWindowVisible(hwnd):
        if win32gui.GetWindowText(hwnd) == 'II':
            self = hwnd
            hwnd1 = hwnd

def get_self(*args):
    win32gui.EnumWindows(enumHandler2, None)


def dummy_name():
    root.after(500, get_self)
    root.after(1000, gen_name)
##    root.after(1500, bottom)


dummy_name()
######################################################################

canvas.bind('<Button-1>', click)
canvas.bind('<Double-Button-1>', double_click)
canvas.bind('<Button-3>', open_options)

move_fnc(mouse)

root.bind('<MouseWheel>', mouse_wheel)
root.mainloop()

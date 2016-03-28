from Tkinter import *
import ttk
from datetime import datetime, date, timedelta
from SQL import *

# update main window after adding/deleting/changing events
# dont keep comboboxes when you dont need them (deletion, change of day)
# update EMW after change (add, delete, change)
# TODO: add scrolling to calendars (canvas) redrawing everything going to first of month

class SelectedBefore():
    def __init__(self, canvas, rectangle):
        self.canvas = canvas
        self.rect = rectangle

class CalendarCanvas():
    def __init__(self, emw, size):

        self.emw = emw
        self.size = size
        self.canvas = Canvas(emw.calendars_frame, width = size*7+1, height = size*7, bg = 'white', highlightthickness=0)
        self.first_of_month = 0 # init var
        self.days_in_month = 0 # init var
        self.month = 0 # init var
        self.year = 0 # init var

        self.canvas.bind('<Button-1>', self.click)

    def change_month(self, year, month, selected_date=(0,0,0)):

        self.canvas.delete(ALL)

        events = [i[2] for i in get_events_month(year,month,32,0)]
        self.first_of_month = datetime(year,month,1).isoweekday()-1
        self.days_in_month = (date(year if month != 12 else year+1, month+1 if month != 12 else 1,1) - timedelta(days=1)).day
        self.month = month
        self.year = year

        # create text "month, year" on top of calendar
        self.canvas.create_text(self.size*7/2.0, self.size/2.0, text = ['January','February','March','April','May','June','July','August','September','October','November','December'][month-1]+', '+str(year), font = ('TkDefaultFont',9,'bold'))

        # create numbers in month (red if event on the day, black otherwise)
        for i in range(6*7):
            if i >= self.first_of_month and i < self.days_in_month + self.first_of_month:
                self.canvas.create_text((i%7+.5)*self.size, (i/7+1.5)*self.size, text = str(i-self.first_of_month+1), fill='red' if i-self.first_of_month+1 in events else 'black')

        # create rect around current day
        if month == self.emw.today.month and year == self.emw.today.year:
            i = self.emw.today.day+self.first_of_month-1
            self.canvas.create_rectangle(i%7*self.size, (i/7+1)*self.size, (i%7+1)*self.size, (i/7+2)*self.size, outline='red')

        # create rect around selected day
        if month == selected_date[1] and year == selected_date[0]:
            i = selected_date[2]+self.first_of_month-1
            self.emw.selected_before.canvas = self.canvas
            self.emw.selected_before.rect = self.canvas.create_rectangle(i%7*self.size+1, (i/7+1)*self.size+1, (i%7+1)*self.size-1, (i/7+2)*self.size-1)

    def click(self, event):

        # determine which day was clicked and if it was valid
        i = event.x/self.size + event.y/self.size *7 - 7
        if i < self.first_of_month: return 0
        if i >= self.first_of_month + self.days_in_month: return 0


        # delete previous rect and create new one around selected day
        try: self.emw.selected_before.canvas.delete(self.emw.selected_before.rect)
        except AttributeError: pass
        
        self.emw.selected_before.canvas = self.canvas
        self.emw.selected_before.rect = self.canvas.create_rectangle(i%7*self.size+1, (i/7+1)*self.size+1, (i%7+1)*self.size-1, (i/7+2)*self.size-1)

        self.emw.change_day(self.year, self.month, i-self.first_of_month+1, False)




class EntriesDay():
    def __init__(self, emw):

        self.emw = emw
        self.year_string = StringVar()
        self.month_string = StringVar()
        self.day_string = StringVar()
        self.entry_vars = []
        self.entries = []
        self.full = []

        # go to day comboboxes and button ################################
        gtd = Frame(emw.day_frame)
        gtd.grid(row=0, column=0, columnspan=4)
        
        Label(gtd, text='Day: ').grid(row=0,column=0)
        ttk.Combobox(gtd, textvariable=self.day_string, width = 5, values=list(range(1,[0,31,28,31,30,31,30,31,31,30,31,30,31][self.emw.month] + 1))).grid(row=0, column=1)

        Label(gtd, text='Month: ').grid(row=0,column=2)
        ttk.Combobox(gtd, textvariable=self.month_string, width = 5, values=list(range(1,13))).grid(row=0, column=3)

        Label(gtd, text='Year: ').grid(row=0,column=4)
        ttk.Combobox(gtd, textvariable=self.year_string, width = 5, values=list(range(1980, 2031))).grid(row=0, column=5)

        Button(gtd, text= 'Go to day', command=self.go_to_day2).grid(row=0, column=6)


        # create day grid #################################################
        for i in range(24):
            self.entry_vars.append(StringVar())
            self.entries.append(Entry(emw.day_frame, width = 23, textvariable = self.entry_vars[i]))
            self.entries[i].grid(row = 10+i%12, column = (i/12)*2+1)
            # maybe save labels somewhere, so you can change bg if there is an event there or not
            Label(emw.day_frame, text = ('0'+str(i) if i < 10 else str(i))+':00').grid(row = 10+i%12, column = (i/12)*2)

        self.entry_class = self.entries[0].winfo_class() # bomo rabli pole za preverjat class

        Button(emw.day_frame, text='Save', command = self.shrani).grid(row=30, column=2)
        Button(emw.day_frame, text='Save and Quit', command = lambda x=True: self.shrani(x)).grid(row=30, column=3)


    def shrani(self, close=False):
        flag = False
        for i in range(24):
            if i in self.full: continue
            a = self.entry_vars[i].get()
            
            if a:
                flag = True
                save_event(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),a,'',self.emw.year,self.emw.month,self.emw.day,('0'+str(i) if i < 10 else str(i))+':00')
        if flag:
            self.emw.draw_month(int(self.emw.month),int(self.emw.year),datetime.now())
        if close:
            self.emw._delete_window()
        else:
            self.emw.change_day(int(self.year_string.get()), int(self.month_string.get()), int(self.day_string.get()), True)



    def go_to_day2(self):        
        self.emw.change_day(int(self.year_string.get()), int(self.month_string.get()), int(self.day_string.get()), True)


    def go_to_day(self):

        # change comboboxes
        self.year_string.set(str(self.emw.year))
        self.month_string.set(str(self.emw.month))
        self.day_string.set(str(self.emw.day))

        # reset string variables
        for i in self.entry_vars: i.set("")
        
        def dummy(click, i, event):
            if event == False: self.emw.event_detail.change(False, i)
            else: self.emw.event_detail.change(event)

        # if its combobox, delete it and make an Entry
        for i in range(24):
            self.entries[i].unbind('<Button-1>')
            self.entries[i].bind('<Button-1>',lambda x, i1=i,e=False: dummy(x, i1, e))
            if self.entries[i].winfo_class() != self.entry_class:
                self.entries[i].destroy()
                self.entries[i] = Entry(self.emw.day_frame, width = 23, textvariable = self.entry_vars[i])
                self.entries[i].grid(row=10+i%12, column=(i/12)*2+1)

        # get events
        events = get_events_day(self.emw.year, self.emw.month, self.emw.day)

        def dummy_combo(click, widget, events):
            self.emw.event_detail.change(events[widget.current()])
            
        # if more than one event, delete entry and make a combobox
        j = False # init value to be returned if no events exist
        for i,j in events.items():
            self.full.append(i)
            if len(j) == 1:
                self.entry_vars[i].set(j[0][2])
                self.entries[i].bind('<Button-1>', lambda x, i1=i,e=j[0]: dummy(x, i1, e))
##                self.entries[i].bind('<Button-1>', lambda x: self.emw.event_detail.change(j[0]))
            else:
                self.entries[i].destroy()
                self.entries[i] = ttk.Combobox(self.emw.day_frame, textvariable=self.entry_vars[i], values = [k[2] for k in j])
                self.entries[i].current(0)
                self.entries[i].grid(row=10+i%12, column=(i/12)*2+1)
                self.entries[i].bind('<<ComboboxSelected>>', lambda x, w=self.entries[i], e=j: dummy_combo(x,w,e))

        # return events, so we can display details of first event
        return j


class EventDetail:
    def __init__(self, emw):
        
        self.emw = emw

        self.event = [0]
        
        self.year_string = StringVar()
        self.month_string = StringVar()
        self.day_string = StringVar()

        self.end_year_string = StringVar()
        self.end_month_string = StringVar()
        self.end_day_string = StringVar()

        self.subject = StringVar()

        self.notification = IntVar()
        self.show = IntVar()
        self.time = StringVar()

        self.repeat = StringVar()
        self.day_checkbox = [IntVar() for i in range(7)]

        # date comboboxes #################################################
        gtd = Frame(emw.event_frame)
        gtd.grid(row=0, column=0, columnspan=4)
        
        Label(gtd, text='Day: ').grid(row=0,column=0)
        # need to have it, so i can change number of days in "values" list
        self.day_combobox = ttk.Combobox(gtd, textvariable=self.day_string, width = 5, values=list(range(1,[0,31,28,31,30,31,30,31,31,30,31,30,31][self.emw.month] + 1)))
        self.day_combobox.grid(row=0, column=1)

        Label(gtd, text='Month: ').grid(row=0,column=2)
        ttk.Combobox(gtd, textvariable=self.month_string, width = 5, values=list(range(1,13))).grid(row=0, column=3)

        Label(gtd, text='Year: ').grid(row=0,column=4)
        ttk.Combobox(gtd, textvariable=self.year_string, width = 5, values=list(range(1980, 2031))).grid(row=0, column=5)


        # misc ############################################################
        misc = Frame(emw.event_frame)
        misc.grid(row= 1, column=0)

        Label(misc, text='Time: ').grid(row=0,column=0)
        Entry(misc, textvariable=self.time, width=5).grid(row=0,column=1)

        Checkbutton(misc, text = "Notification", variable = self.notification).grid(row=0,column=2)
        Checkbutton(misc, text = "Show event", variable = self.show).grid(row=0,column=3)
        
        # repeating #############################################
        repeat_frame = LabelFrame(emw.event_frame, text = 'Repeating', relief = 'groove') #, width = 450, height = 50)
        repeat_frame.grid(row=2,column=0)

        # more bit definirano to prej, da lhko uporabim u fn disable
        check_frame = Frame(repeat_frame)
        check_frame.grid(row=2, column=0, columnspan=4)
        check_buttons = []
        for i,d in enumerate(['Mo','Tu','We','Th','Fr','Sa','Su']):
            check_buttons.append(Checkbutton(check_frame, text = d, variable = self.day_checkbox[i]))
            check_buttons[i].grid(row=0,column=i)

        def disable(x):
            if self.rep.get() == 'Custom':
                for i in check_buttons: i['state'] = NORMAL
            else:
                for i in check_buttons: i['state'] = DISABLED

        Label(repeat_frame, text='Repeat event: ').grid(row=0,column=0)
        self.rep = ttk.Combobox(repeat_frame, textvariable=self.repeat, width = 8, values=['None','Daily','Weekly','Monthly','Anualy','Custom'])
        self.rep.grid(row=0, column=1)

        self.rep.bind('<<ComboboxSelected>>', lambda x: disable(x))


        end_date = Frame(repeat_frame)
        end_date.grid(row=3, column=0, columnspan=4)
        
        Label(end_date, text='Day: ').grid(row=0,column=0)
        # always have 31 day... so could have non valid dates, but doesent matter
        ttk.Combobox(end_date, textvariable=self.end_day_string, width = 5, values=list(range(1,32))).grid(row=0, column=1)

        Label(end_date, text='Month: ').grid(row=0,column=2)
        ttk.Combobox(end_date, textvariable=self.end_month_string, width = 5, values=list(range(1,13))).grid(row=0, column=3)

        Label(end_date, text='Year: ').grid(row=0,column=4)
        ttk.Combobox(end_date, textvariable=self.end_year_string, width = 5, values=list(range(1980, 2031))).grid(row=0, column=5)

   
        # subject + description ###########################################
        Label(emw.event_frame, text='Subject:').grid(row = 20, column=0)
        Entry(emw.event_frame, textvariable=self.subject, width=48).grid(row=25, column=0)
        

        Label(emw.event_frame, text='Description:').grid(row = 30, column=0)
        self.text = Text(emw.event_frame, width=48, height=5, font='TkDefaultFont')
        self.text.grid(row=35, column=0)


        # buttons
        buttons = Frame(emw.event_frame)
        buttons. grid(row=40, column=0)

        Button(buttons, text='Clear', command=self.change).grid(row=0,column=0)
        Button(buttons, text='Delete', command=self.delete_event).grid(row=0,column=1)
        self.save_button = Button(buttons, text='Save', command=self.save_change)
        self.save_button.grid(row=0,column=2)

    def delete_event(self):
        month = int(self.month_string.get())
        year = int(self.year_string.get())
        delete_event_id(self.event[0])
        self.emw.draw_month(month, year, datetime.now())
        self.emw.change_day(year, month, int(self.day_string.get()), True)

    def save_change(self):
        # TODO: change self.event as well... just pass event to "change" function
        if self.save_button['text'] == 'Change':
            names2 = ['id','dateChanged','subject','description','year','month','day','h_m','repeat','repeatWeekdays','repeatUntil','show','notify']

            repUnt = '('+self.end_year_string.get()+','+self.end_month_string.get()+','+self.end_day_string.get()+')'
            repWeek ='('
            for i in range(7):
                if self.day_checkbox[i]: repWeek = repWeek +str(i)+','
            repWeek = repWeek[:-1]+')'
            new_vals = (0,0,self.subject.get(),self.text.get(1.0,END)[:-1],int(self.year_string.get()),int(self.month_string.get()),int(self.day_string.get()),self.time.get(),self.repeat.get(),repWeek,repUnt,self.show.get(),self.notification.get())
            names = []
            values = []
            for i in range(2, 13):
                if self.event[i] != new_vals[i]:
                    names.append(names2[i])
                    values.append(new_vals[i])
            if names:
                change_event_id(self.event[0], names+['dateChanged'], values+[datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
                self.change()
        else:
            repUnt = '('+self.end_year_string.get()+','+self.end_month_string.get()+','+self.end_day_string.get()+')'
            repWeek ='('
            for i in range(7):
                if self.day_checkbox[i]: repWeek = repWeek +str(i)+','
            repWeek = repWeek[:-1]+')'        
            save_event(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                       self.subject.get(),
                       self.text.get(1.0,END),
                       self.year_string.get(),
                       self.month_string.get(),
                       self.day_string.get(),
                       self.time.get(),
                       repeat=self.repeat.get(),
                       repeatWeekdays=repWeek,
                       repeatUntil=repUnt,
                       show=self.show.get(),
                       notify=self.notification.get())
            self.change()

        self.emw.draw_month(int(self.month_string.get()),int(self.year_string.get()),datetime.now())
        self.emw.change_day(int(self.year_string.get()), int(self.month_string.get()), int(self.day_string.get()), True)



    def change(self, event = False, just_time= False):
            
        if not event:
            event = (0,0,'','',self.emw.year,self.emw.month,self.emw.day,'08:00','None','()','(,,)',1,0)
            self.save_button['text']='Save'
        else:
            self.save_button['text']='Change'

        self.event = event

        self.year_string.set(str(event[4]))
        self.month_string.set(str(event[5]))
        self.day_string.set(str(event[6]))

        self.day_combobox['values']=list(range(1,[0,31,28,31,30,31,30,31,31,30,31,30,31][self.emw.month] + 1))
        [a,b,c] = event[10][1:-1].split(',')
        self.end_year_string.set(a)
        self.end_month_string.set(b)
        self.end_day_string.set(c)

        self.subject.set(event[2])
        self.text.delete(1.0, END)
        self.text.insert(END, event[3])

        self.notification.set(event[12])
        self.show.set(event[11])
        self.time.set(event[7])

        self.repeat.set(event[8])
        for i in range(7): self.day_checkbox[i].set(0)
        for i in eval(event[9]): self.day_checkbox[i].set(1)

        if type(just_time) == type(1):
            self.time.set(('0'+str(just_time) if just_time < 10 else str(just_time))+':00')




class EventManagerWindow:
    def __init__(self, calendar, draw_month):
        self.draw_month = draw_month
        self.root = Toplevel(calendar)
        self.root.title('Manage Events')

        self.year = 0 # init variable
        self.month = 0 # init variable
        self.day = 0 # init variable
        self.today = datetime.now()

        self.selected_before = SelectedBefore(0,0) # to be used in canvases

        # make base frames
        self.calendars_frame = Frame(self.root)
        self.day_frame = Frame(self.root)
        self.event_frame = Frame(self.root)

        self.calendars_frame.grid(row=0,column=0)
        self.day_frame.grid(row=0, column=1)
        self.event_frame.grid(row=0, column=2)

        # make calendars
        size = 18
        self.canvases = [CalendarCanvas(self, size) for i in range(3)]
        for i in range(3): self.canvases[i].canvas.grid(row=i, column=0)

        # make entries grid
        self.entries_day = EntriesDay(self)

        # make event details area
        self.event_detail = EventDetail(self)

        self.root.withdraw()

        self.root.protocol('WM_DELETE_WINDOW', self._delete_window)

    def _delete_window(self):
        self.root.withdraw()
        

    def change_day(self, year, month, day, update_calendars):
        # if day is changed by clicking on a calendar, the calendars should not
        # update

        self.root.state('normal')
        self.root.focus()

        self.year = year
        self.month = month
        self.day = day

        if update_calendars:
            for i in range(3): self.canvases[i].change_month(year+(month+i)/13, month+i if month+i < 13 else month+i-12, (year, month, day))
        event = self.entries_day.go_to_day()

        if event: self.event_detail.change(event[0])
        else: self.event_detail.change()
        return 0

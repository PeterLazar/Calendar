# coding: utf-8
from Tkinter import *
import tkColorChooser as colorchooser
import ttk
from SQL import *
import FixTk

change_colors = None
colors = None
schemes = None
curr_id = 1000


def get_color(color, label):
    global colors
    new = colorchooser.askcolor()[1]
    if new:
        colors[color] = new
        label.config(bg = new)
        change_colors(colors)
        change_colors_sql(colors)

def colors_tab(frame):
    [color1,color2,color3,color4,color5,color6] = colors
    Label(frame, text='Primary color: ').grid(row = 0, column=3, sticky=W)
    l1 = Label(frame, text = '     ', bg = color1)
    l1.grid(row = 0, column = 5, padx=(5,20))
    Button(frame, text = 'Color', command = lambda c=0, l=l1:get_color(c,l)).grid(row  = 0, column = 4)

    Label(frame, text='Secondary color: ').grid(row = 1, column=3, sticky=W)
    l2 = Label(frame, text = '     ', bg = color2)
    l2.grid(row = 1, column = 5, padx=(5,20))
    Button(frame, text = 'Color', command = lambda c=1, l=l2:get_color(c,l)).grid(row  = 1, column = 4)

    Label(frame, text='Month days: ').grid(row = 2, column=3, sticky=W)
    l3 = Label(frame, text = '     ', bg = color3)
    l3.grid(row = 2, column = 5, padx=(5,20))
    Button(frame, text = 'Color', command = lambda c=2, l=l3:get_color(c,l)).grid(row  = 2, column = 4)

    Label(frame, text='Other days: ').grid(row = 3, column=3, sticky=W)
    l4 = Label(frame, text = '     ', bg = color4)
    l4.grid(row = 3, column = 5, padx=(5,20))
    Button(frame, text = 'Color', command = lambda c=3, l=l4:get_color(c,l)).grid(row  = 3, column = 4)

    Label(frame, text='Event text: ').grid(row = 4, column=3, sticky=W)
    l5 = Label(frame, text = '     ', bg = color5)
    l5.grid(row = 4, column = 5, padx=(5,20))
    Button(frame, text = 'Color', command = lambda c=4, l=l5:get_color(c,l)).grid(row  = 4, column = 4)

    Label(frame, text='Weekday names: ').grid(row = 5, column=3, sticky=W)
    l6 = Label(frame, text = '     ', bg = color6)
    l6.grid(row = 5, column = 5, padx=(5,20))
    Button(frame, text = 'Color', command = lambda c=5, l=l6:get_color(c,l)).grid(row  = 5, column = 4)

    #save scheme
    nameVar = StringVar()
    Entry(frame, textvariable = nameVar).grid(row = 3, column=7)
    def save_colors_check():
        global schemes
        n = nameVar.get()
        if not n:
            # ni imena, vrži opozorilo, da ga rabiš
            return 0
        save_color_scheme(n, colors)
        schemes = get_colors_schemes()
        values = [i[1] for i in schemes]
        cb.config(values = values)

    Button(frame, text='Save color scheme', command = save_colors_check).grid(row = 4, column= 7)
    ###
    def select_color_theme(event):
        global colors, curr_id
        id = cb.current()
        curr_id = schemes[id][0]
        colors = list(schemes[id][2:])
        for i,j in enumerate([l1,l2,l3,l4,l5,l6]):
            j.config(bg = colors[i])
            change_colors(colors)
            change_colors_sql(colors)

    values = [i[1] for i in schemes]
    cb = ttk.Combobox(frame, values = values)
    cb.grid(row = 3, column= 1)
    cb.bind("<<ComboboxSelected>>", select_color_theme)

    def dummy_delete_color_scheme():
        global schemes, curr_id
        delete_color_scheme(curr_id)
        for i in schemes:
            if i[0] == curr_id:
                schemes.remove(i)
                break
        curr_id = 1000
        values = [i[1] for i in schemes]
        cb.config(values = values)

    Button(frame, text='Delete current scheme', command = dummy_delete_color_scheme).grid(row = 4, column= 1)

######################################################################
def miscelaneous_tab(parent, root, move_fnc, x_pos,y_pos):
    (box_width, box_height, title_height,x,y,alpha,mouse,delete) = get_misc()
    b_h,b_w,t_h,Del,alpha1,move1 = StringVar(), StringVar(), StringVar(), IntVar(), IntVar(), IntVar()
    b_h.set(str(box_height));b_w.set(str(box_width));t_h.set(str(title_height))
    alpha1.set(alpha);move1.set(mouse)

    ######################################################################
    pos = LabelFrame(parent, text = 'Position', relief = 'groove', width = 250, height = 50)
    pos.grid(row=1, column=1)
    Label(pos, text = 'x: ').grid(row=0,column=0)
    Entry(pos, textvariable = x_pos).grid(row=0,column=1)
    Label(pos, text = 'y: ').grid(row=0,column=2)
    Entry(pos, textvariable = y_pos).grid(row=0,column=3)

    ######################################################################
    size = LabelFrame(parent, text = 'Size', relief = 'groove', width = 250, height = 50)
    size.grid(row=2,column=1)
    Label(size, text = 'Box height: ').grid(row=0,column=0)
    Entry(size, textvariable = b_h, width = 4).grid(row=0,column=1)
    Label(size, text = 'Box width: ').grid(row=0,column=2)
    Entry(size, textvariable = b_w, width = 4).grid(row=0,column=3)
    Label(size, text = 'Title bar height: ').grid(row=0,column=4)
    Entry(size, textvariable = t_h, width = 4).grid(row=0,column=5)

    ######################################################################
    othr = LabelFrame(parent, text = 'Misc', relief = 'groove', width = 250, height = 50)
    othr.grid(row=3, column=1)
    Label(othr, text = 'Alpha: ').grid(row=0,column=0)
    Entry(othr, textvariable = alpha1, width = 4).grid(row=0,column=1)
    def move_fnc2(): move_fnc(move1.get())
    Checkbutton(othr, text='Mouse movement', variable = move1, command = move_fnc2).grid(row = 0, column = 2)

    ######################################################################
    deletion = LabelFrame(parent, text = 'Confirm deletion', relief = 'groove', width = 250, height = 50)
    deletion.grid(row=4, column=1)
    def sth(): # rabim, ka mi noce delat cene
        print(Del.get())
    r1 = Radiobutton(deletion, text=' Always ',variable=Del, value=0, command = sth)
    r1.grid(row=0, column=1)
    r2 = Radiobutton(deletion, text=' Never ',variable=Del, value=1, command = sth)
    r2.grid(row=0, column=2)
    r3 = Radiobutton(deletion, text=' Repeating events ',variable=Del, value=2, command = sth)
    r3.grid(row=0, column=3)
    Del.set(delete)

    ######################################################################
    buttons = Frame(parent, width = 250, height = 50)
    buttons.grid(row=5, column=2)
    def save():
        #save everything from misc tab
        save_misc(int(b_w.get()),int(b_h.get()),int(t_h.get()),x_pos.get(),y_pos.get(),alpha1.get(),move1.get(),Del.get())
        return 0
    Button(buttons, text = 'Save', command = save).grid(row  = 0, column = 0)







######################################################################

def options_window(root, change_colors1, move_fnc, opt_win_close, x_pos,y_pos):
    global change_colors, colors, schemes
    colors = list(get_colors())
    schemes = get_colors_schemes()
    change_colors = change_colors1


    opt_win = Toplevel(root)
    opt_win.title('Options')
    opt_win.focus_set()

    nb = ttk.Notebook(opt_win)
    nb.pack()

    color_tab = Frame(nb)
    nb.add(color_tab, text = 'Colors')
    colors_tab(color_tab)

    misc_tab = Frame(nb)
    nb.add(misc_tab, text = 'Misc')
    miscelaneous_tab(misc_tab,root,move_fnc, x_pos,y_pos)




    def _delete_window():
        opt_win.destroy()
        opt_win_close()

    opt_win.protocol('WM_DELETE_WINDOW', _delete_window)
    opt_win.mainloop()






##if __name__ == '__main__':
##    a = Tk()
##    options_window(a)

# Standard ToolTip from Python remade, to work with canvas and
# its children instead of widgets

# one ToolTip should be used for everything on a canvas
# "child" is a list of tags, belonging to stuff, where we want tooltips
# "text" is a list of corresponding texts
# !!!!! child and text MUST be lists
from Tkinter import *



class ToolTip():

    def __init__(self, canvas, child, text, screen_width, screen_height):
        self.canvas = canvas
        self.child = child
        self.text = text
        self.x = 0
        self.y = 0
        self.sw = int(screen_width)
        self.sh = int(screen_height)
        self.tipwindow = None
        self.id = None
        self.child_id = None
        self.canvas.focus_set()
        self.canvas.bind('<Motion>', self.motion)
        self.canvas.bind('<MouseWheel>', self.leave)

    def motion(self, event=None):
        x,y = event.x, event.y
        self.x, self.y = x,y
        a = self.canvas.find_overlapping(x,y,x,y)
        for i,j in enumerate(self.child):
            if j in a:
                if i != self.child_id:
                    self.leave()
                self.child_id = i
                self.enter()
                return 0
        self.leave()


    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.canvas.after(500, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.canvas.after_cancel(id)

    def showtip(self):
        if self.tipwindow:
            return
        
        self.tipwindow = tw = Toplevel(self.canvas)
        tw.wm_overrideredirect(1)
        self.showcontents(self.text[self.child_id])
        tw.update()

        # fix, so that it doesnt go offscreen
        x = self.canvas.winfo_rootx() + self.x + 10
        y = self.canvas.winfo_rooty() + self.y + 10

        w,h = tw.geometry().split('+')[0].split('x')
        x = min(x, self.sw - int(w)-1)
        y = min(y, self.sh - int(h)-1)

        tw.wm_geometry('+%d+%d' % (x, y))


    def showcontents(self, text='Your text here'):
        label = Label(self.tipwindow, text=text, justify=LEFT,
                      background='#ffffe0', relief=SOLID, borderwidth=1)
        label.pack()

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()



def main():
    # Test code
    root = Tk()
    c = Canvas(root, width=600, height = 300)
    c.pack()
    b = c.create_rectangle(10,10,200,130, fill='red')
    d = c.create_rectangle(200,10,400,130, fill='blue')
    e = c.create_rectangle(10,130,200,250, fill='yellow')
    tip = ToolTip(c,[d,b], ['Fuck you!','Hello world'], 500,500)
    tip.child += [e]
    tip.text += ['Nice!']

    root.mainloop()

if __name__ == '__main__':
    main()

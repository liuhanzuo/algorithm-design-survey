from tkinter import *
from Board import *
from evaluation import *
import time
class Game:
    def black_init(self):
        pass
    def white_init(self):
        self.AI_player=1
        self.human_player=-1
    def __init__(self):
        self.tk=Tk()
        self.current_player=1
        self.human_player=1
        self.AI_player=-1
        self.chosen=0
        self.tk.title("Gobang")
        self.tk.resizable(0,0)
        self.tk.update()
        self.bg=PhotoImage(file="board.png")
        w=self.bg.width()
        h=self.bg.height()
        self.canvas=Canvas(self.tk,width=w,height=h,highlightthickness=0)
        self.canvas.create_image(0,0,image=self.bg,anchor='nw')
        # choose black/white
        self.recid1=self.canvas.create_rectangle(20,20,220,100,fill="black")
        self.recid2=self.canvas.create_text(90, 60, text="Black", font=("Arial", 22),fill="white")
        self.recid3=self.canvas.create_rectangle(320,20,520,100,fill="white")
        self.recid4=self.canvas.create_text(390, 60, text="White", font=("Arial", 22),fill="black")
        self.canvas.bind_all('<Button-1>',self.choose)
        self.bd=Board()
        self.ev=evaluator()
        self.canvas.pack()
    def choose(self,evt):
        if evt.x>=20 and evt.x<=220 and evt.y>=20 and evt.y<=100: #black
            self.black_init()
            self.chosen=1
        if evt.x>=320 and evt.x<=520 and evt.y>=20 and evt.y<=100:
            self.white_init()
            self.chosen=1
        if self.chosen==0:
            return 0
        self.canvas.delete(self.recid1)
        self.canvas.delete(self.recid2)
        self.canvas.delete(self.recid3)
        self.canvas.delete(self.recid4)
        self.canvas.unbind('<Button-1>')    
        self.canvas.bind_all('<Button-1>',self.user_click)
        return 1
    def user_click(self,evt):
        if self.current_player != self.human_player:
            return False
        x=(int)((evt.x-41.5)/(42.8)+0.5)
        y=(int)((evt.y-41.5)/(42.8)+0.5)
        if self.bd.move(self.canvas,self.human_player,x,y):
            self.current_player=-self.current_player
            return True
        return False
    def component_move(self):
        if self.current_player!=self.AI_player:
            return False
        ls=self.ev.Getpos(self.bd,-1,4)[0]
        if(self.bd.move(self.canvas,self.AI_player,ls[0],ls[1])):
            self.current_player=-self.current_player
            time.sleep(0.2)
            return True
        return False
    def mainloop(self):
        ENDG=0
        while 1:
            if self.current_player==self.AI_player:
                self.component_move()
            time.sleep(0.1)
            if(self.bd.EndGame()):
                self.tk.update()
                ENDG=self.bd.EndGame()
                time.sleep(3)
                break
            self.tk.update()
        self.canvas.delete(ALL)
        if ENDG==1:
            self.canvas.create_text(300,400,text="BLACK WINS!",font="Helvetica 40", fill="blue")
        else:
            self.canvas.create_text(300,400,text="WHITE WINS!",font="Helvetica 40", fill="blue")
        self.tk.update()
        time.sleep(20)
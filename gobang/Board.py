from tkinter import *
class Board:
    def __init__(self):
        self.status=[]
        for i in range(0,15):
                self.status.append([0]*15)
    def Available(self,x,y):
        return x>=0 and x<=14 and y>=0 and y<=14
    def EndGame(self):
        for i in range(0,15):
            for j in range(0,15):
                for k in [[0,1],[1,0],[1,1],[1,-1]]:
                    tot,x,y=0,i,j
                    for r in range(0,6):
                        if(self.Available(x,y)):
                            tot+=self.status[x][y]
                            x+=k[0]
                            y+=k[1]
                    if abs(tot)==5:
                        if tot==5:
                            return 1
                        else:
                            return -1
        return 0
    def move(self, canvas, player_id, x, y):
        if not self.Available(x,y):
            return False
        if self.status[x][y]!=0:
            return False
        self.status[x][y]=player_id
        d=43.2
        e=35
        color=''
        if player_id==1:
            color='black'
        else:
            color='white'
        canvas.create_oval(25+x*d,25+y*d,25+x*d+e,25+y*d+e,fill=color)
        return True
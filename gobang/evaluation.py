import random
from Board import *
class recorder:
    def __init__(self):
        #BLACK(1) WHITE(-1)
        self.FIVE=[0,0] #number of SSSSS
        self.ALIVE_FOUR=[0,0] #number of OSSSSO
        self.DEAD_FOUR=[0,0] 
        self.ALIVE_THREE=[0,0] #number of OSSSO/OSSOSO/OSOSSO
        self.DEAD_THREE=[0,0] #number of ESSSOO/ESSOSO/ESOSSO/conv
        self.ALIVE_TWO=[0,0] #number of OOSSOO
        self.JMP_TWO=[0,0] #number of OSOSO
        self.ALIVE_ONE=[0,0] #number of OOSOO
    def decode_string(self,s):
        Len=len(s)
        ans=[0,0,0,0,0,0,0,0]
        s_cnt=s.count('S')
        if s_cnt==0:
            return ans
        if s_cnt==1:
            for i in range(0,Len-5):
                sub=s[i:(i+5)]
                if sub=="OOSOO":
                    ans[7]=ans[7]+1
                elif sub=="OOSOE" or sub=="EOSOO":
                    ans[7]=ans[7]+0.4
            return ans
        if s_cnt==2:
            for i in range(0,Len-5):
                sub=s[i:(i+5)]
                if sub=="OSOSO":
                    ans[6]=ans[6]+1
                elif sub=="OOSOO":
                    ans[7]=ans[7]+1                
                elif sub=="OOSOE" or sub=="EOSOO":
                    ans[7]=ans[7]+0.4
            for i in range(0,Len-6):
                sub=s[i:(i+6)]
                if sub=="OOSSOO":
                    ans[5]=ans[5]+1
            return ans
        if s_cnt>=3:
            for i in range(0,Len-5):
                sub=s[i:(i+5)]
                if sub=="SSSSS":
                    ans[0]=ans[0]+1
                elif sub=="OSSSO":
                    ans[3]=ans[3]+1
                elif sub=="OSOSO":
                    ans[6]=ans[6]+1
                elif sub=="OOSOO":
                    ans[7]=ans[7]+1
                elif sub=="OOSOE" or sub=="EOSOO":
                    ans[7]=ans[7]+0.4
        for i in range(0,Len-6):
            sub=s[i:(i+6)]
            if sub=="OSSSSO":
                ans[1]=ans[1]+1
            elif sub=="OSOSSO" or sub=="OSSOSO":
                ans[3]=ans[3]+1
            elif sub=="ESSSOO" or sub=="ESSOSO" or sub=="ESOSSO":
                ans[4]=ans[4]+1
            elif sub=="OOSSSE" or sub=="OSOSSE" or sub=="OSSOSE":
                ans[4]=ans[4]+1
            elif sub=="OOSSOO":
                ans[5]=ans[5]+1
        for i in range(1,Len-1):
            if s[i]!='O':
                continue
            j=i-1
            CNT=0
            CNT2=0
            while s[j]=='S':
                j=j-1
                CNT=CNT+1
            if s[j]=='E' and j<i-1:
                CNT2=1
            j=i+1
            while s[j]=='S':
                j=j+1
                CNT=CNT+1
            if s[j]=='E' and j>i+1:
                CNT2=CNT2+1
            if CNT2<2 and CNT>=4:
                ans[2]=ans[2]+1
        return ans
    def Available(self,x,y):
        return x>=0 and x<=14 and y>=0 and y<=14
    def upd(self,lst1,id):
        if id==0:
            self.FIVE[0]+=lst1[0]
            self.ALIVE_FOUR[0]+=lst1[1]
            self.DEAD_FOUR[0]+=lst1[2]
            self.ALIVE_THREE[0]+=lst1[3]
            self.DEAD_THREE[0]+=lst1[4]
            self.ALIVE_TWO[0]+=lst1[5]
            self.JMP_TWO[0]+=lst1[6]
            self.ALIVE_ONE[0]+=lst1[7]
        else:
            self.FIVE[1]+=lst1[0]
            self.ALIVE_FOUR[1]+=lst1[1]
            self.DEAD_FOUR[1]+=lst1[2]
            self.ALIVE_THREE[1]+=lst1[3]
            self.DEAD_THREE[1]+=lst1[4]
            self.ALIVE_TWO[1]+=lst1[5]
            self.JMP_TWO[1]+=lst1[6]
            self.ALIVE_ONE[1]+=lst1[7]
    def count(self,board):
        self.__init__()
        s=""
        for i in range(0,14):
            s="E"
            for j in range(0,14):
                if board.status[i][j]==1:
                    s=s+"S"
                elif board.status[i][j]==0:
                    s=s+"O"
                else:
                    s=s+"E"
            s=s+"E"
            lst1=self.decode_string(s)
            self.upd(lst1,0)
            s="E"
            for j in range(0,14):
                if board.status[i][j]==-1:
                    s=s+"S"
                elif board.status[i][j]==0:
                    s=s+"O"
                else:
                    s=s+"E"
            s=s+"E"
            lst1=self.decode_string(s)
            self.upd(lst1,1)
        for i in range(0,14):
            s="E"
            for j in range(0,14):
                if board.status[j][i]==1:
                    s=s+"S"
                elif board.status[j][i]==0:
                    s=s+"O"
                else:
                    s=s+"E"
            s=s+"E"
            lst1=self.decode_string(s)
            self.upd(lst1,0)
            s="E"
            for j in range(0,14):
                if board.status[j][i]==-1:
                    s=s+"S"
                elif board.status[j][i]==0:
                    s=s+"O"
                else:
                    s=s+"E"
            s=s+"E"
            lst1=self.decode_string(s)
            self.upd(lst1,1)
            
        lst=[]
        for i in range(0,15):
            lst.append([i,0])
            lst.append([0,i])
        for j in lst:
            x,y=j[0],j[1]
            s="E"
            for k in range(0,15):
                if not self.Available(x+k,y+k):
                    break
                if board.status[x+k][y+k]==1:
                    s=s+"S"
                elif board.status[x+k][y+k]==0:
                    s=s+"O"
                else:
                    s=s+"E"
            s=s+"E"
            lst1=self.decode_string(s)
            self.upd(lst1,0)
            s="E"
            for k in range(0,15):
                if not self.Available(x+k,y+k):
                    break
                if board.status[x+k][y+k]==-1:
                    s=s+"S"
                elif board.status[x+k][y+k]==0:
                    s=s+"O"
                else:
                    s=s+"E"
            s=s+"E"
            lst1=self.decode_string(s)
            self.upd(lst1,1)
                   
        lst=[]
        for i in range(0,15):
            lst.append([i,14])
            lst.append([0,i])
        for j in lst:
            x,y=j[0],j[1]
            s="E"
            for k in range(0,15):
                if not self.Available(x+k,y-k):
                    break
                if board.status[x+k][y-k]==1:
                    s=s+"S"
                elif board.status[x+k][y-k]==0:
                    s=s+"O"
                else:
                    s=s+"E"
            s=s+"E"
            lst1=self.decode_string(s)
            self.upd(lst1,0)
            s="E"
            for k in range(0,15):
                if not self.Available(x+k,y-k):
                    break
                if board.status[x+k][y-k]==-1:
                    s=s+"S"
                elif board.status[x+k][y-k]==0:
                    s=s+"O"
                else:
                    s=s+"E"
            s=s+"E"
            lst1=self.decode_string(s)
            self.upd(lst1,1)
            

class evaluator:
    def __init__(self):
        pass
    def Getpos(self,board,playerid,nodenum):
        Empty=[]
        for i in range(0,15):
            for j in range(0,15):
                if board.status[i][j]==0:
                    Empty.append([i,j])
        Size=len(Empty)
        if Size==225:
            return [[7,7],0]
        new_board=Board()
        for i in range(0,15):
            for j in range(0,15):
                new_board.status[i][j]=board.status[i][j]
        MAX=[]
        lst=[]
        for i in range(nodenum):
            MAX.append(-100000000)
            lst.append([0,0])
        for [i,j] in Empty:
            new_board.status[i][j]=playerid
            score=self.Evaluation(new_board,playerid)
            score+=random.randint(-10,10)
            for d in range(0,nodenum):
                if score>MAX[d]:
                    for x in range(nodenum-1,d,-1):
                        MAX[x]=MAX[x-1]
                        lst[x][1]=lst[x-1][1]
                        lst[x][0]=lst[x-1][0]
                    MAX[d]=score
                    lst[d]=[i,j]
            new_board.status[i][j]=0
        if nodenum==1:
            return [lst[0],MAX[0]]
        else:
            MAXSCORE=-1000000000
            pos=[0,0]
            d=0
            for [i,j] in lst:
                new_board.status[i][j]=playerid
                cur=self.Getpos(new_board,-playerid,1)[1]
                if(MAX[d]-cur>MAXSCORE):
                    MAXSCORE=MAX[d]-cur
                    pos=[i,j]
                new_board.status[i][j]=0
                d=d+1
            return [pos,MAXSCORE]
    def getpos2(self,board,playerid):
        pass
    def Available(self,x,y):
        return x>=0 and x<=14 and y>=0 and y<=14
    def Winning(self,board,playerid):
        for i in range(0,15):
            cnt=0
            for j in range(0,15):
                if(board.status[i][j]==playerid):
                    cnt=cnt+1
                    if cnt==5:
                        return True
                else:
                    cnt=0
            if cnt==5:
                return True
        for i in range(0,15):
            cnt=0
            for j in range(0,15):
                if(board.status[j][i]==playerid):
                    cnt=cnt+1
                    if cnt==5:
                        return True
                else:
                    cnt=0
        lst=[]
        for i in range(1,12):
            lst.append([i,0])
            lst.append([0,i])
        lst.append([0,0])
        for j in lst:
            x,y,cnt=j[0],j[1],0
            for k in range(0,15):
                if not self.Available(x+k,y+k):
                    break
                if board.status[x+k][y+k]==playerid:
                    cnt=cnt+1
                    if cnt==5:
                        return True
                else:
                    cnt=0        
        lst=[]
        for i in range(1,15):
            lst.append([i,14])
            lst.append([0,i])
        for j in lst:
            x,y,cnt=j[0],j[1],0
            for k in range(0,15):
                if not self.Available(x+k,y-k):
                    break
                if board.status[x+k][y-k]==playerid:
                    cnt=cnt+1
                    if cnt==5:
                        return True
                else:
                    cnt=0
    def Evaluation(self,board,playerid):
        #current move: enemy
        #my score count
        tot_score=0
        #check if winning
        if self.Winning(board,playerid):
            return 10000000
        
        #count my killing points/alive threes, and the enemie's to get an evaluation
        re=recorder()
        re.count(board)
        MY,EN=0,0
        if playerid==1:
            EN=1
        else:
            MY=1
        score=0
        if re.FIVE[MY]:
            return 10000000
        if re.FIVE[EN] or re.ALIVE_FOUR[EN] or re.DEAD_FOUR[EN]:
            return -10000000
        
        score=score+re.FIVE[MY]*1000000+re.ALIVE_FOUR[MY]*100000+re.ALIVE_THREE[MY]*400
        score=score+re.DEAD_THREE[MY]*100+re.JMP_TWO[MY]*35
        score=score+re.DEAD_FOUR[MY]*250+re.ALIVE_TWO[MY]*50+re.ALIVE_ONE[MY]*10
        if re.ALIVE_THREE[MY]+re.DEAD_FOUR[MY]>=2:
            score=score+5000
        score-=(re.ALIVE_FOUR[EN]*1000000+re.ALIVE_THREE[EN]*12000)
        score-=(re.DEAD_FOUR[EN]*1000000+re.DEAD_THREE[EN]*800)
        score-=(re.JMP_TWO[EN]*65+re.ALIVE_TWO[EN]*105+re.ALIVE_ONE[EN]*20)
        return score
        
                   
        
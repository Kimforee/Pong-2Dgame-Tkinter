from cProfile import label
from email.mime import image
from tkinter import *
from tkinter import font
from turtle import color, title 
import random
from PIL import ImageTk
import mysql.connector
from tkinter import messagebox

root = Tk()
width = 1024
height = 576
score = 0
highscore = 0
b2 = 0
b3 = 0
speedcount = 0
speedlimit=[2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]

# ball moving speed
global xspeed, yspeed
xspeed = random.randint(2,8)
yspeed = random.randint(2,8)
xspeed = 4
yspeed = 4
img1= ImageTk.PhotoImage(file='./bg.png')
img2= ImageTk.PhotoImage(file='./mainbg.jpg')


def Game():
    global canvas

    # creating canvas 
    canvas = Canvas(root, bg='cyan', width=width, height=height)
    canvas.create_image(0,0,image=img1,anchor=NW)
    canvas.place(x=120,y=80)

    # creating a ball using oval
    ball = canvas.create_oval(430, 10, 470, 50, fill='black',outline='cyan')

    platform_y = height - 10
    platform = canvas.create_rectangle(width//2-100, platform_y, width//2+100, platform_y+10, fill='white')


    canvas.create_text(32, 20, text="Score :", font=('Arial Bold', 12), fill='black')
    canvas.create_text(200, 20, text="Highest Score :", font=('Arial Bold', 12), fill='black')
    canvas.create_text(270, 20, text=highscore, font=('Arial Bold', 12), fill='black',tag="high")


    def move_ball():

        global xspeed, yspeed
        global speedcount
        global score
        global highscore

        #to keep a track of speed
        print("x equals :  ",xspeed)
        print("y equals :  ",yspeed)

        # to get the co-ordinates of the ball
        x1, y1, x2, y2 = canvas.coords(ball)

        # this increases the speed of the ball by 2 after every 2 hits on platform
        if speedcount in speedlimit :
            speedcount = 0
            if xspeed > 0:
                xspeed = xspeed + 2
            if yspeed > 0:
                yspeed = yspeed + 2 
            if xspeed < 0:
                xspeed = xspeed - 2  
            if yspeed < 0:
                yspeed = yspeed - 2     

            print("inside speed change to x =" +str(xspeed) + "y =" +str(yspeed))
        if x1 <= 0 or x2 >= width:
            # hit wall, reverse x speed
            xspeed = -xspeed
            print("inside hit wall reverse change to " +str(xspeed) + " " )

        if y1 <= 0:
            # hit top wall 
            yspeed = abs(yspeed)
            print("inside top wal hit change to " +str(yspeed) + "top ball hit " )

        elif y2 >= platform_y:

            # calculate center x of the ball
            cx = (x1 + x2) // 2

            # check whether platform is hit
            px1, _, px2, _ = canvas.coords(platform)
            print("inside platform hit change to " +str(yspeed) + "top speedcount is one"+str(speedcount) )
            # if px1 <= cx <= px2:
            if px1 <= cx <= px2:
              yspeed = -yspeed
              speedcount = speedcount + 1
              score = score + 1
              print("inside platform hit change to " +str(yspeed) + "top speedcount is"+str(speedcount) )
              if score > highscore:
                 canvas.delete("high")
                 highscore = score
 
              canvas.delete("tag")
              canvas.create_text(71, 20, text=score, font=('Arial Bold', 12), fill='black',tag="tag")
              canvas.create_text(270, 20, text=highscore, font=('Arial Bold', 12), fill='black',tag="high")
              
            else:
              canvas.create_text(width//2, height//2, text='Game Over \n  You Lost', font=('Arial Bold', 32), fill='red',)
              databaseofpong(score)
              return
            
        canvas.move(ball, xspeed, yspeed)
        canvas.after(20, move_ball)

    def board_right(event):
        x1, y1, x2, y2 = canvas.coords(platform)
        # make sure the platform is not moved beyond right wall
        if x2 < width:
            dx = min(width-x2, 20)
            canvas.move(platform, dx, 0)

    def board_left(event):
        x1, y1, x2, y2 = canvas.coords(platform)
        # make sure the platform is not moved beyond left wall
        if x1 > 0:
            dx = min(x1, 20)
            canvas.move(platform, -dx, 0)

    def board_up(event):
            x1, y1, x2, y2 = canvas.coords(platform)
            if y1 > 0:
              dx = min(y1, 20)
              canvas.move(platform, -dx, 0)

    def board_down(event):
            x1, y1, x2, y2 = canvas.coords(platform) 
            if y2 < height:
              dx = min(height-y2, 20)
              canvas.move(platform, -dx, 0)

    canvas.bind_all('<Right>', board_right)
    canvas.bind_all('<Left>', board_left)
    canvas.bind_all('<Up>', board_up)
    canvas.bind_all('<Down>', board_down)

    move_ball()   

def opennew():
    
    # global canvas
    global b1
    global b2
    global b3
    global b4
    global mb1
    global mb2
    global pong
    pong.after(20,pong .destroy)
    b4  .after(20,b4   .destroy)
    mb1 .after(20,mb1  .destroy)
    mb2 .after(20,mb2  .destroy)
    b1  .after(20,b1   .destroy)
    rec=int(2)
    backbutton(rec)

    b3=Button(root,text=" Restart ",
              activeforeground='#C47AFF',
              font=('Arial Bold', 16),
              bd=5,
              width=17,
              height=1,
              command=restart)                
    b3.place(x=600,y=20)
    Game()

def close():
    ans=messagebox.askokcancel("Title","Do you really want to exit Pong  ?")
    if(ans==True):
       root.destroy()

def retrieve_highscore():
    connection = mysql.connector.connect(host="localhost", user="root", password="12345")
    cursor = connection.cursor()
    try:
        cursor.execute("USE PongStorage2")
    except mysql.connector.Error as err:
        # Create the database and table if they don't exist
        if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            cursor.execute("CREATE DATABASE PongStorage2")
            cursor.execute("USE PongStorage2")
            cursor.execute("CREATE TABLE playerscore1 (id INT PRIMARY KEY AUTO_INCREMENT, score INT)")
        else:
            raise
    
    cursor.execute("SELECT MAX(score) FROM playerscore1")
    result = cursor.fetchone()

    # Fetch and discard any pending result sets
    while cursor.nextset():
        pass

    cursor.close()
    connection.close()

    if result and result[0]:
        return result[0]
    else:
        return 0

def highsscore():

    global score
    global b1
    global b2
    global b3
    global b4
    global mb1
    global mb2
    global pong
    global highscore
    global highb
    global scoret

    pong.after(20,pong .destroy)
    b4  .after(20,b4   .destroy)
    mb1 .after(20,mb1  .destroy)
    mb2 .after(20,mb2  .destroy)
    b1  .after(20,b1   .destroy)
    rec=int(1)
    backbutton(rec)
    highestscore = retrieve_highscore()
    print("Highest Score in hieghtcisre function->:", highestscore)
    
    scoret=Label (root, text=highestscore,
                  font=('Arial Bold', 16), 
                  fg='black',bg='#B9E0FF',
                  bd=20,height=2,width=10,
                  highlightbackground='#CDFCF6',
                  relief=RAISED,)
    scoret.place(x=690,y=290)

    highb= Label (root,text="  Highest Score : ",
                  fg='black',bg='#B9E0FF',
                  activeforeground='#C47AFF',
                  font=('Arial Bold', 16),
                  bd=20,width=15,height=2,
                  highlightbackground='#CDFCF6',
                  relief=RAISED,)
    highb.place(x=420,y=290)

def backtomainmenu():
    global canvas
    global b1
    global b2
    global b3
    global b4
    global mb1
    global mb2
    global pong
    global highb
    global scoret

    pong  .after (20,pong .destroy)
    mb1   .after (20,mb1  .destroy)
    mb2   .after (20,mb2  .destroy)
    b1    .after (20,b1   .destroy)
    b3    .after (20,b3   .destroy)
    b2    .after (20,b2   .destroy)
    b4    .after (20,b4   .destroy)
    canvas.after (20,canvas.destroy)
    pong =  Label(root, text= "          PONG          ",
                  font= ('Helvetica 18 bold'),
                  highlightbackground='#CDFCF6',
                  relief=RAISED,
                  activeforeground='#C47AFF',
                  fg='black',bg='#8D72E1',
                  bd=20,
                  width=18,
                  height=3)
    pong.pack(padx= 30,pady= 30)
        
    b1=  Button(  root,text=" Start ",
                  fg='black',bg='#B9E0FF',
                  activeforeground='#C47AFF',
                  font=('Arial Bold', 16),
                  bd=5,width=16,height=1,
                  command= opennew) 
    b1.place   (  x=520,y=210)

    mb1= Button(  root,text=" Options ",
                  fg='black',bg='#B9E0FF',
                  activeforeground='#C47AFF',
                  font=('Arial Bold', 16),
                  bd=5,width=16,height=1,
                  command=root.destroy)
    mb1.place  (  x=520,y=310)

    mb2= Button(  root,text=" Highest Score ",
                  fg='black',bg='#B9E0FF',
                  activeforeground='#C47AFF',
                  font=('Arial Bold', 16),
                  bd=5,width=16,height=1,
                  command=highsscore)
    mb2.place  (  x=520,y=410)

    b4=  Button(  root,text=" Quit ",fg='black',
                  bg='#B9E0FF',
                  activeforeground='#C47AFF',
                  font=('Arial Bold', 16),
                  bd=5,width=16,height=1,
                  command=close)
    b4.place   (  x=520,y=510)

def menu():
    global xspeed
    global yspeed
    global opt
    optlist=[" Easy "," Medium "," Hard "]
    var = StringVar(root)
    var.set("Easy")

    opt=OptionMenu(root,var,*optlist)
    opt.place(x=790,y=320)
    if    (opt==" Easy "):
          xspeed = 4
          yspeed = 4
        
    elif  (opt==" Medium "):
          xspeed = 8
          yspeed = 8
    
    elif  (opt==" Hard "):
          xspeed = 15
          yspeed = 15
     

def backtomainmenu1():
    global canvas
    global b1
    global b2
    global b3
    global b4
    global mb1
    global mb2
    global pong
    global highb
    global scoret
    
    scoret.after (20,scoret.destroy)
    highb .after (20,highb.destroy)
    b2    .after (20,b2   .destroy)

    pong =  Label(root, text= "          PONG          ",
                  font= ('Helvetica 18 bold'),
                  highlightbackground='#CDFCF6',
                  relief=RAISED,
                  activeforeground='#C47AFF',
                  fg='black',bg='#8D72E1',
                  bd=20,
                  width=18,
                  height=3)
    pong.pack(padx= 30,pady= 30)
        
    b1=  Button(  root,text=" Start ",
                  fg='black',bg='#B9E0FF',
                  activeforeground='#C47AFF',
                  font=('Arial Bold', 16),
                  bd=5,width=16,height=1,
                  command= opennew) 
    b1.place   (  x=520,y=210)
    mb1= Button(  root,text=" Options ",
                  fg='black',bg='#B9E0FF',
                  activeforeground='#C47AFF',
                  font=('Arial Bold', 16),
                  bd=5,width=16,height=1,
                  command=menu)
    mb1.place  (  x=520,y=310)
    mb2= Button(  root,text=" Highest Score ",
                  fg='black',bg='#B9E0FF',
                  activeforeground='#C47AFF',
                  font=('Arial Bold', 16),
                  bd=5,width=16,height=1,
                  command=highsscore)
    mb2.place  (  x=520,y=410)
    b4=  Button(  root,text=" Quit ",fg='black',
                  bg='#B9E0FF',
                  activeforeground='#C47AFF',
                  font=('Arial Bold', 16),
                  bd=5,width=16,height=1,
                  command=close)
    b4.place   (  x=520,y=510)

def backbutton(rec):
    global b2
    # highb.after(20,highb.destroy)
    if(rec == 1):
        b2=Button(root,text=" Back ",
              activeforeground='#C47AFF',
              font=('Arial Bold', 16),
              bd=5,width=17,
              height=1,
              command=backtomainmenu1)
        b2.place(x=140,y=20)
    elif(rec == 2):
        b2=Button(root,text=" Back ",
              activeforeground='#C47AFF',
              font=('Arial Bold', 16),
              bd=5,width=17,
              height=1,
              command=backtomainmenu)
        b2.place(x=140,y=20)

def restart():
    global canvas
    global b2
    global b3
    global b4
    global score
    global xspeed
    global yspeed
    score = 0
    xspeed = 4
    yspeed = 4
    xspeed = random.randint(-4,4)
    yspeed = random.randint(-4,4)
    canvas.after(20, canvas.destroy)
    b2.after(20,b2.destroy)
    b3.after(20,b3.destroy)
    opennew ()

def databaseofpong(got):
    highs = 0
    connection = mysql.connector.connect(host="localhost", user="root", password="12345")
    con = connection.cursor(buffered=True)
    
    try:
        con.execute("use PongStorage2")
    except:
        con.execute("create database PongStorage2")
        con.execute("use PongStorage2")
    
    try:
        con.execute("describe playerscore1")
    except:   
        con.execute("create table playerscore1( id int primary key auto_increment, score int)")

    def storage():
        print("inside ready push data in storage scoreboard")
        con.execute(f"INSERT INTO playerscore1 (score) VALUES ({highs})")
        connection.commit()

    highs = retrieve_highscore()

    if got > highs:
        highs = got
        print("calling storage")
        storage()
    else:
        print("Failed to score high. You Asian.")

root.overrideredirect(False)
root.geometry     ("1280x720")
root.title        ("Main Menu")
title_bar = Frame (root,bg='#8D72E1',relief=SUNKEN,bd=2)
root.configure    (bg='#6C4AB6')

line1 = Label(root, text= "",
             highlightbackground='#CDFCF6',
             relief=RAISED,
             activeforeground='#C47AFF',
             fg='black',bg='#8D72E1',
             bd=20,
             width=1,
             height=100)
line1.place(x= 1,y= 1)

line2 = Label(root, text= "",
             highlightbackground='#CDFCF6',
             relief=RAISED,
             activeforeground='#C47AFF',
             fg='black',bg='#8D72E1',
             bd=20,
             width=1,
             height=100)
line2.place(x= 1230,y=1)

pong = Label(root, text= "          PONG          ",
             font= ('Helvetica 18 bold'),
             highlightbackground='#CDFCF6',
             relief=RAISED,
             activeforeground='#C47AFF',
             fg='black',bg='#8D72E1',
             bd=20,
             width=18,
             height=3)
pong.pack(padx= 30,pady= 30)

b1=  Button(root,text=" Start ",
            fg='black',bg='#B9E0FF',
            activeforeground='#C47AFF',
            font=('Arial Bold', 16),
            bd=5,width=16,height=1,
            command= opennew) 
b1.place   (x=520,y=210)
mb1= Button(root,text=" Options ",
            fg='black',bg='#B9E0FF',
            activeforeground='#C47AFF',
            font=('Arial Bold', 16),
            bd=5,width=16,height=1,
            command=menu)
mb1.place  (x=520,y=310)
mb2= Button(root,text=" Highest Score ",
            fg='black',bg='#B9E0FF',
            activeforeground='#C47AFF',
            font=('Arial Bold', 16),
            bd=5,width=16,height=1,
            command= highsscore)
mb2.place  (x=520,y=410)
b4=  Button(root,text=" Quit ",
            fg='black',bg='#B9E0FF',
            activeforeground='#C47AFF',
            font=('Arial Bold', 16),
            bd=5,width=16,height=1,
            command=close)
b4.place   (x=520,y=510)


root.mainloop()
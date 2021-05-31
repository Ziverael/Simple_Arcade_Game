#!/usr/bin/env python

import tkinter as tk
from PIL import ImageTk,Image
import os
root=tk.Tk()
root.title("Arcade Game")
root.geometry("1000x800")
root.iconbitmap(".\Images\ico.ico")

im=tk.PhotoImage(file=r".\Images\button.png")    
bg=tk.PhotoImage(file=r".\Images\menu_bg.png")

#----------------------------------
#Buttons Actions
#----------------------------------
def run():
    os.system("python platformgame.py")
def rules():
    os.system("python rules.py")
def scores():
    os.system("python score.py")
def about():
    os.system("python abouts.py")    
#Canvas
#----------------------------------
background=tk.Canvas(root,width=1000,height=800)
background.pack(fill="both",expand=True)
background.create_image(0,0,image=bg,anchor="nw")
background.create_text(500,100,text="Platform Game",font=("Arial",50),fill="white")
#----------------------------------
#Menu
#----------------------------------
buttfont=("Helvetica",20)
butt=[]
pad=0
butt.append(tk.Button(root,image=im,text="Start",command=run,compound="center",font=buttfont,bg="purple",fg="purple"))
butt.append(tk.Button(root,image=im,command=rules,text="Rules",compound="center",font=buttfont,bg="purple",fg="purple"))
butt.append(tk.Button(root,image=im,command=scores,text="Scores",compound="center",font=buttfont,bg="purple",fg="purple"))
butt.append(tk.Button(root,image=im,text="About me",command=about,compound="center",font=buttfont,bg="purple",fg="purple"))
butt.append(tk.Button(root,image=im,text="Exit",command=root.quit,compound="center",font=buttfont,bg="purple",fg="purple"))
for i in butt:
    background.create_window(400,200+pad,anchor="nw",window=i)
    pad+=100    
background.create_text(180,780,text="Platformgame by Krzysztof Jankowski. All rights reserved")
#----------------------------------
root.mainloop()
import tkinter as tk
from PIL import ImageTk,Image

root=tk.Tk()
root.title("Results")
root.geometry("500x400")
root.iconbitmap(".\Images\ico.ico")
otherbg=tk.PhotoImage(file=r".\Images\menu_bg2.png")



scorebg=tk.Canvas(root,width=500,height=400)
scorebg.pack(fill="both",expand=True)
scorebg.create_image(0,0,image=otherbg,anchor="nw")
scorebg.create_text(250,30,text="Best Results",font=("Arial",30),fill="white")
    
f=open("scores.txt","r")
table=[i for i  in f]
it=1
out=""
for i in table:
    i=i.split(" ")
    move=10-len(i[1])
    expand=" "*move
    i[1]+=expand
    
    move=8-len(i[0])
    expand=" "*move
    i[0]=expand+i[0]
    
    buff=str(it)+". "+i[1]+" "+i[0]
    #print(buff)
    out+=buff+"\n"
    it+=1

scorebg.create_text(250,250,text=out,font=("Arial",20),fill="white",justify="left")

f.close()
root.mainloop()    
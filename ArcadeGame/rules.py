import tkinter as tk
from PIL import ImageTk,Image
root=tk.Tk()
root.title("About me")
root.geometry("500x400")
root.iconbitmap(".\Images\ico.ico")

otherbg=tk.PhotoImage(file=r".\Images\menu_bg2.png")


others=tk.Canvas(root,width=500,height=400)
others.pack(fill="both",expand=True)
others.create_image(0,0,image=otherbg,anchor="nw")
others.create_text(250,30,text="Rules",font=("Arial",30),fill="white")


text="The goal is to survive as long as you can. In orded to achieve this goal\n you have to jump on sliding platforms, collect hearts and avoid\nblack blocks\nKeys:\nLeft Right arrows - move left right\nSpace - jump (while jumping - double jump)\nEsc-Quit"
others.create_text(250,150,text=text,font=("Arial",10),fill="white")
root.mainloop()

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
others.create_text(250,30,text="About me",font=("Arial",30),fill="white")

text="""Krzysztof Jankowski 1st yaer student of Applied Mathematics.\nAssets in that project was made by myself, except sounds and music.\nSounds and music sources:\n Our Nights
by Eugenio Mininni\n\n
Extra bonus in a video game
Boxer getting hit
Player jumping in a video game
From the site https://mixkit.co/free-sound-effects/game/
"""

others.create_text(250,200,text=text,font=("Arial",10),fill="white",justify="center")


root.mainloop()

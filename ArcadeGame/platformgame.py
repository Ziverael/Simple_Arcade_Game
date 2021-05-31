#Modules section
import pygame as pg
from pygame.locals import *
import sys
import random

#-----------------------------------------------
#Fundamental variables and initialization
pg.init()
vec=pg.math.Vector2#Create a vector object
HEIGHT=800
WIDTH=1000
ACC=3#Acceleration
FRIC=-0.4#Friction of objects
FPS=60
FPS_CLOCK=pg.time.Clock()
Running=True

#Screen and display
icon=pg.image.load("./Images/ico.png")
screen=pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption("Platform game")
pg.display.set_icon(icon)
#-----------------------------------------------
#Classes
class Background(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.bgim=pg.image.load("./Images/bg.jpg")#Unpreapared
        self.bgX=0
        self.bgY=0
    def render(self):
        screen.blit(self.bgim,(self.bgX,self.bgY))

class Platform(pg.sprite.Sprite):
    def __init__(self,pos):#pos=(x,y)
        super().__init__()
        self.image=pg.image.load("./Images/Block_Cobelstone.png")
        self.rect=self.image.get_rect(center=(pos[0],pos[1]-50))
        self.pos=vec(pos)
    
    

    def update(self):
        self.pos.y+=1+Timer.dific
        self.rect.midbottom=self.pos
        if self.rect.top==HEIGHT:
            self.kill()

class Health(pg.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image=pg.image.load("./Images/Heart.png")
        self.rect=self.image.get_rect(center=(pos[0],pos[1]-50))
        self.pos=vec(pos)
    
    def update(self):
        self.pos.y+=1+Timer.dific
        self.rect.midbottom=self.pos
        if self.rect.top==HEIGHT:
            self.kill()

class Timer(pg.sprite.Sprite):
    start=pg.time.get_ticks()
    last_s=-1
    last_platx=360
    dific=0.0
    dific2=0
    def __init__(self):
        super().__init__()
        self.rect=pg.Rect(0,0,200,30)
        
        self.disp="{}:{}:{}".format(0,0,0)
        self.font=pg.font.SysFont('Consolas',30)
        self.image=self.font.render(self.disp,True,(255,255,255))
        self.rect=self.image.get_rect()


    def update(self):
        buff=pg.time.get_ticks()-Timer.start
        mi=buff//60000
        s=(buff-mi*60000)//1000
        ms=buff%1000
        self.disp="{}:{}:{}".format(mi,s,ms)
        self.image=self.font.render(self.disp,True,(255,255,255)) 
        if s!=Timer.last_s:
            if not s%3:
                Timer.last_platx=generate(True)
                Timer.dific+=0.05
                Timer.dific2+=1
            if not s%7:
                generate(False)
            if s!= 0 and not s%(15+Timer.dific2):
                generateHp()
            if s>36 and not s%4:
                generate(False)
        Timer.last_s=s
        
class Enemy(pg.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image=pg.image.load("./Images/Enemy.png")
        self.rect=self.image.get_rect(center=(pos[0],pos[1]-50))
        self.pos=vec(pos)
    
    def update(self):
        self.pos.y+=1+Timer.dific
        self.rect.midbottom=self.pos
        if self.rect.top==HEIGHT:
            self.kill()


        
class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pg.image.load("./Images/Hero.png")
        self.faceL=pg.image.load("./Images/HeroL.png")
        self.faceR=pg.image.load("./Images/Hero.png")
        self.rect=self.image.get_rect()
        self.pos=vec((600,100))
        self.vel=vec(0,0)
        self.acc=vec(0,0.3)#Set speed of changing movement
        self.jump_=1
        self.stand=False
        self.hp=3

    def gravity(self):
        hits=pg.sprite.spritecollide(self,platSprite,0,0)#Returns list of interacted sprites
        if self.vel.y>0:
            if hits:
                lowest=hits[0]
                if self.vel.y>14:
                    eps=-10
                else:
                    eps=-50
                if self.pos.y<lowest.rect.bottom+eps:#Decrease value to interact only with top of the sprite
                    self.jump_=2
                    self.stand=True
                
                    self.pos.y=lowest.rect.top+3+2*Timer.dific
                    self.vel.y=0
            else:
                self.stand=False

    def collect(self):
        hit=pg.sprite.spritecollide(self,hpSprite,1,0)
        if hit:
            self.hp+=1
            collectFX.play()
            stat.update()
    
    def damage(self):
        hit=pg.sprite.spritecollide(self,enemySprite,0,0)
        if hit:
            return True

    def update(self):
        self.gravity()
        self.collect()    
        keys=pg.key.get_pressed() 
        if keys[K_LEFT]:
            self.acc.x=-ACC
            self.image=self.faceL
        if keys[K_RIGHT]:
            self.acc.x=ACC
            self.image=self.faceR
        #Kinemathic formulas with no discrete time (1t=1period)
        
        if  not self.stand:
            if self.jump_==2:
                self.jump_-=1
            self.vel.y+=self.acc.y
        
        buff=self.acc.x
        self.acc.x+=self.vel.x*FRIC
        if buff*self.acc.x<0:
            self.acc.x=0
            self.vel.x=0
        self.vel+=self.acc
        self.pos+=self.vel+0.5*self.acc

        #Sliding from screen edges and lose condition
        if self.pos.y-100>HEIGHT or self.damage():
            self.hp-=1
            damageFX.play()
            stat.update()
            pg.event.clear()
            if self.hp<1:
                pg.event.post(pg.event.Event(pg.QUIT))
            else:
                self.pos.x=Timer.last_platx
                self.pos.y=0
                self.vel.y=0
        if self.pos.x >WIDTH:
            self.pos.x=0
        if self.pos.x<0:
            self.pos.x=WIDTH
        
        self.rect.midbottom=self.pos
        
    def jump(self):
        if self.jump_:
            self.jump_-=1
            self.vel.y=-10-Timer.dific
            jumpFX.play()


class Stats(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.text="Hp:{}".format(hero.hp)
        self.font=pg.font.SysFont(None,30)
        self.image=self.font.render(self.text,1,(255,255,255))
        self.rect=self.image.get_rect(center=(950,10))
    
    def update(self):
        self.text="Hp:{}".format(hero.hp)
        self.image=self.font.render(self.text,1,(255,255,255))
        self.rect=self.image.get_rect(center=(950,0))
    



class Textbackground(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pg.image.load("./Images/Results.png")
        self.X=350
        self.Y=300

    def render(self):
        screen.blit(self.image,(self.X,self.Y))

class Textinput(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.text="name"
        self.font=pg.font.SysFont("Consolas",40)
        self.image=self.font.render(self.text,True,(255,255,255))
        self.rect=self.image.get_rect(center=(350+80,300+100))
    
    def update(self):
        self.image=self.font.render(self.text,True,(255,255,255))

#-----------------------------------------------
#Functions
def generate(type_):#True-Platform; False-Enemy
    number=random.randrange(1,5)
    last=random.randrange(0,937)
    if  not type_:
        if abs(Timer.last_platx-last)<64:
            last+=64
    pos=(last,0)
    for i in range(0,number):
        if type_:
            platSprite.add(Platform(pos))
        else:
            enemySprite.add(Enemy(pos))
        pos=(pos[0]+64,pos[1])
    return last

def generateHp():
    hpSprite.add(Health((random.randrange(0,937),0)))

def gen():
    table=[]
    for i in range(0,10):
        table.append(["0:00:00","Name",0])
    return table
def ms2dp(n):
    mi=n//60000
    s=(n-mi*60000)//1000
    ms=n%1000
    output="{}:{}:{}".format(mi,s,ms)
    return output
        
def loadSounds(file):
    return "./Sounds/{}".format(file)

#-----------------------------------------------
#Sounds
pg.mixer.music.load(loadSounds("mixkit-our-nights-627.mp3"))
pg.mixer.music.play(-1)
jumpFX=pg.mixer.Sound(loadSounds("mixkit-player-jumping-in-a-video-game-2043.wav"))
collectFX=pg.mixer.Sound(loadSounds("mixkit-extra-bonus-in-a-video-game-2045.wav"))
damageFX=pg.mixer.Sound(loadSounds("mixkit-boxer-getting-hit-2055.wav"))
#-----------------------------------------------
#Create objects
timer=Timer()
timerSprite=pg.sprite.RenderClear()
timerSprite.add(timer)


background=Background()
background.render()

hero=Player()
heroSprite=pg.sprite.RenderClear()
heroSprite.add(hero)

stat=Stats()
statSprite=pg.sprite.RenderClear()
statSprite.add(stat)

hpSprite=pg.sprite.RenderClear()

platSprite=pg.sprite.RenderClear()
platSprite.add(Platform((600,200)))
platSprite.add(Platform((600+64,200)))
platSprite.add(Platform((600-64,200)))

enemySprite=pg.sprite.RenderClear()
#-----------------------------------------------
#Event loop
while Running:
    for event in pg.event.get():
        
        #Quit
        if event.type==QUIT:
            Running=False
        if event.type==pg.KEYDOWN:
            if event.key==K_SPACE:
                hero.jump()
            if event.key==K_ESCAPE:
                Running=False
    
    heroSprite.update()
    platSprite.update()
    enemySprite.update()
    timerSprite.update()
    hpSprite.update()
    heroSprite.clear(screen,background.bgim)
    platSprite.clear(screen,background.bgim)
    enemySprite.clear(screen,background.bgim)
    timerSprite.clear(screen,background.bgim)
    hpSprite.clear(screen,background.bgim)
    statSprite.clear(screen,background.bgim)

    heroSprite.draw(screen)
    platSprite.draw(screen)
    enemySprite.draw(screen)
    timerSprite.draw(screen)
    hpSprite.draw(screen)
    statSprite.draw(screen)
    pg.display.update()#or try flip
    FPS_CLOCK.tick(FPS)
#-----------------------------------------------
#Saving results
score=pg.time.get_ticks()-Timer.start
scored=ms2dp(score)
pg.mixer.music.stop()

#-----------------------------------------------
#Read player name

pg.event.clear()
save=True
Running=True

textbg=Textbackground()
textbg.render()

textpol=Textinput()
textSprite=pg.sprite.RenderClear()
textSprite.add(textpol)

while Running:
    for event in pg.event.get():
        #Quit
        if event.type==QUIT:
            Running=False
        if event.type==pg.KEYDOWN:
            if event.key==K_ESCAPE:
                save=False
                Running=False
            #Write
            elif event.key==K_BACKSPACE:
                if len(textpol.text)>0:
                    textpol.text=textpol.text[:-1]
            elif event.key==K_RETURN:
                Running=False
            else:
                if len(textpol.text)<10:
                    textpol.text+=event.unicode
    textbg.render()
    textSprite.update()
    textSprite.clear(screen,textbg.image)
    textSprite.draw(screen)
    pg.display.update()#or try flip
if save:
    f=open("scores.txt","r+")
    try:
        results=[(i.split(" ")[0],i.split(" ")[1],int(i.split(" ")[2])) for i in f]
        for i in range(0,10):
            if results[i][2]<score:
                results.insert(i,(scored,textpol.text,score))
                results.pop()
                break
    except:
        results=gen()
        results.insert(0,(scored,textpol.text,score))
        results.pop()
    
    f.seek(0)
    f.truncate()
    #buff=f.readlines()
    #print(buff,"<--")
    #print(results)
    for i in range(0,10):
    #print(results[i][0]+" "+str(results[i][1])+"\n")
        f.write(results[i][0]+" "+results[i][1]+" "+str(results[i][2])+"\n")
    f.close()
pg.quit()
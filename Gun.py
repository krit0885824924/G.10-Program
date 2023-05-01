
import math
import pygame as pg
pg.init()
win_x, win_y = 800,480
screen = pg.display.set_mode((win_x, win_y))
posX, posY = 70,410
u = 30
a = -1
x = 0
y = 0
t = 0
ux = u*math.cos(math.radians(60))
uy =u*math.sin(math.radians(60))
while(1):
    screen.fill((0, 50, 10))
    pg.draw.rect(screen,(211,211,211),(380,180,10,300))
    pg.draw.rect(screen,(211,211,211),(0,430,50,50))
    if(x>(win_x)):
        x = x-win_x
    if(y>(win_y)):
        y = y-win_y
    
    pg.draw.circle(screen,(255,200,100),(posX+x,posY-y),20)
    x = (ux*t)
    y = (uy*t)+(0.5*a*t**2)
    if pg.mouse.get_pressed()[0]==1:
        t += 0.05
    if pg.mouse.get_pressed()[2]==1:
        t -= 0.05
    if(y<0):
            exit()
    # print(x,y)
    pg.time.delay(2)
    pg.display.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

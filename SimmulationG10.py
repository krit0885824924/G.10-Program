class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos): 
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE 
            
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.unicode.isdigit():
                        self.text += event.unicode
                    else:
                        pass
                self.txt_surface = FONT.render(self.text, True, self.color)
    def resetText(self):
        self.text=''
        
        
    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, Screen):
        Screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pg.draw.rect(Screen, self.color, self.rect, 2)
        
class Rectangle:
    def __init__(self,x=0,y=0,w=0,h=0,color=()):
        self.x = x 
        self.y = y 
        self.w = w 
        self.h = h 
        self.color=color
    def draw(self,screen):
        pg.draw.rect(screen,(self.color),(self.x,self.y,self.w,self.h))
class Button(Rectangle):
    def __init__(self, x=0, y=0, w=0, h=0, color=()):
        Rectangle.__init__(self, x, y, w, h,color)
    
    def isMouseOn(self):
        (x,y) = pg.mouse.get_pos()
        if(self.x<=x<=self.w+self.x and self.y<=y<=self.h+self.y and pg.mouse.get_pressed()[0]==1):
            return True
        pass
class Circle:
    def __init__(self,x,y,r,color):    
        self.x = x
        self.y = y
        self.r = r
        self.color=color
    def draw(self,screen):
        pg.draw.circle(screen,(self.color),(self.x,self.y),self.r)

        
class Polygon:
    def __init__(self,color,point):    
        self.point=point
        self.color=color
    def draw(self,screen):
        pg.draw.polygon(screen,(self.color),self.point)
        
class Calculater:
    def __init__(self,x_basket,y_basket,spring_recoil):
        self.x_basket = x_basket
        self.y_basket = y_basket
        self.spring_recoil = spring_recoil
        
    def calCulate_velocity(self, k):
        self.k = k
        m = 0.32782
        u = ((self.k)*(((self.spring_recoil/100)**2)/m)-(19.62*(self.spring_recoil/100)))**0.5
        self.u = u
        return self.u
    
    def calCulate_height_of_squash(self):
        self.ux = self.u*math.cos(math.radians(60))
        self.uy =self.u*math.sin(math.radians(60))
        height_of_squash = (self.uy*((130-self.y_basket)/self.ux)/100)-(4.905*(((130-self.y_basket))/100/self.ux)**2)
        return height_of_squash
        
    def calCulate_position_machine(self):
        t = (self.uy+((((self.uy)**2)-(4*4.905*0.06165))**0.5))/9.81
        sx = self.ux*t
        self.x_machine = self.x_basket+15
        self.y_machine = ((2.09915+(self.y_basket/100))-sx)*100
        return [('%.2f'%(self.x_machine)),('%.2f' %(self.y_machine))]
    def uxuy(self):
        return [self.ux,self.uy]
          
class Text:
    def __init__(self,keyword,fontsize,color):
        self.fontsize = fontsize 
        self.keyword = keyword 
        self.color=color
        self.font = pg.font.Font('freesansbold.ttf', self.fontsize) 
    def gettext(self):
        return self.font.render(self.keyword, True, self.color) 
    
        
import sys
import pygame as pg
import math

pg.init()
win_x, win_y = 800, 480
screen = pg.display.set_mode((win_x, win_y))

start = Button(345,350,120,50,(31,117,81))
reset = Button(630,400,100,50,(255,0,0))
wall = Rectangle(250,350,20,100,(7,71,131))
triangle = Polygon((164,187,197),[(550,292),(750,292),(650,119)])
basket1 = Circle(602,264,26,(7,71,131))
basket2 = Circle(680,264,26,(7,71,131))
basket3 = Circle(668,208,26,(7,71,131))
c1 = Circle(345,375,25,(31,117,81))
c2 = Circle(465,375,25,(31,117,81))
c3 = Circle(630,425,25,(255,0,0))
c4 = Circle(730,425,25,(255,0,0))
c5= Circle(562,112,4,(255,0,0))
c6= Circle(552,292,4,(255,0,0))
position = Rectangle(560,110,200,200,(164,187,197))
X_axis= Rectangle(550,170,50,2,(7,71,131))
Y_axis= Rectangle(550,120,2,50,(7,71,131))
X_axis1= Rectangle(470,170,50,2,(7,71,131))
Y_axis1= Rectangle(470,120,2,50,(7,71,131))
machine = Rectangle(30,410,40,40,(7,71,131))
squach1=Circle(70,404,6,(0,0,0))
squach2=Circle(465,394,6,(0,0,0))
Basket = Polygon((7,71,131),[(450,450),(480,450),(490,400),(440,400)])
line = Rectangle(30,450,450,3,(7,71,131))


COLOR_INACTIVE = pg.Color('lightskyblue3') 
COLOR_ACTIVE = pg.Color('dodgerblue2')     
FONT = pg.font.Font(None, 32)

input_box1 = InputBox(280, 120, 20, 32) 
input_box2 = InputBox(280, 190, 20, 32) 
input_box3 = InputBox(280, 260, 20, 32)
input_boxes = [input_box1, input_box2, input_box3] 
run = True


text1=Text('Baskets position on X-axis',16,(7,71,131)).gettext()
textRect1=text1.get_rect()
textRect1.center=(150,135)
text2=Text('Baskets position on Y-axis',16,(7,71,131)).gettext()
textRect2 = text2.get_rect()
textRect2.center = (150, 205)
text3 = Text('Spring recoil',16,(7,71,131)).gettext() 
textRect3 = text3.get_rect() 
textRect3.center = (205, 275)
text4 = Text('Analyze',20,(255,255,255)).gettext()
textRect4 = text4.get_rect() 
textRect4.center = (405, 375)
text5 = Text('INPUT VARIABLE',24,(7,71,131)).gettext()
textRect5 = text5.get_rect() 
textRect5.center = (390, 50)
text6 = Text('RESULT',24,(7,71,131)).gettext() 
textRect6 = text6.get_rect() 
textRect6.center = (390, 50)
text7 = Text('Machines position on X-axis :',16,(7,71,131)).gettext()
textRect7 = text7.get_rect() 
textRect7.center = (170, 120)
text8 = Text('Machine positions on Y-axis :',16,(7,71,131)).gettext()
textRect8 = text8.get_rect() 
textRect8.center = (170, 170)
text9 = Text('Reset',20,(255,255,255)).gettext() 
textRect9 = text9.get_rect() 
textRect9.center = (680, 425)
text10 = Text('Squash balls height when crossing the wall :',16,(7,71,131)).gettext()
textRect10 = text10.get_rect() 
textRect10.center = (200,220)
text11 = Text('CM',16,(7,71,131)).gettext() 
textRect11 = text11.get_rect() 
textRect11.center = (400, 120)
text12 = Text('CM',16,(7,71,131)).gettext() 
textRect12 = text12.get_rect() 
textRect12.center = (400, 170)
text19 = Text('CM',16,(7,71,131)).gettext()  
textRect19 = text19.get_rect() 
textRect19.center = (500, 220)
text16 = Text('CM',16,(7,71,131)).gettext() 
textRect16 = text16.get_rect() 
textRect16.center = (500, 135)
text17 = Text('CM',16,(7,71,131)).gettext() 
textRect17 = text17.get_rect() 
textRect17.center = (500, 205)
text18 = Text('CM',16,(7,71,131)).gettext()  
textRect18 = text18.get_rect() 
textRect18.center = (500, 275)
text20 = Text('(0,0)',16,(7,71,131)).gettext()  
textRect20 = text20.get_rect() 
textRect20.center = (560, 100)
text21 = Text('(0,0)',16,(7,71,131)).gettext()  
textRect21 = text21.get_rect() 
textRect21.center = (550, 310)
text22 = Text('X',12,(7,71,131)).gettext()  
textRect22 = text22.get_rect() 
textRect22.center = (605,170)
text23 = Text('Y',12,(7,71,131)).gettext()  
textRect23 = text23.get_rect() 
textRect23.center = (550,115)
text24 = Text('X',12,(7,71,131)).gettext()  
textRect24 = text24.get_rect() 
textRect24.center = (525,170)
text25 = Text('Y',12,(7,71,131)).gettext()  
textRect25 = text25.get_rect() 
textRect25.center = (470,115)


t=0
Show_Setup=True
Show_Result=False
while run:
    screen.fill((253,248,225))
    if Show_Setup==True and Show_Result==False:
        for box in input_boxes:
            box.update() 
            box.draw(screen) 
        screen.blit(text1, textRect1)
        screen.blit(text2, textRect2)
        screen.blit(text3, textRect3)
        screen.blit(text5, textRect5)
        screen.blit(text16, textRect16)
        screen.blit(text17, textRect17)
        screen.blit(text18, textRect18)
        screen.blit(text21, textRect21)
        screen.blit(text22, textRect22)
        screen.blit(text23, textRect23)
        
        start.draw(screen)
        triangle.draw(screen)
        basket1.draw(screen)
        basket2.draw(screen)
        basket3.draw(screen)
        X_axis.draw(screen)
        Y_axis.draw(screen)
        c1.draw(screen)
        c2.draw(screen)
        c6.draw(screen)
        
    if Show_Setup==False and Show_Result==True:
        text13 = Text(str(x_machine),20,(31,117,81)).gettext() 
        textRect13 = text13.get_rect()
        textRect13.center = (330, 120)
        text14 = Text(str(y_machine),20,(31,117,81)).gettext() 
        textRect14 = text14.get_rect()
        textRect14.center = (330, 170)
        text15 = Text(str('%.2f'%(height*100)),20,(31,117,81)).gettext()  
        textRect15 = text15.get_rect()
        textRect15.center = (430, 220)
        
        screen.blit(text6, textRect6)
        screen.blit(text7, textRect7)
        screen.blit(text8, textRect8)
        screen.blit(text10, textRect10)
        screen.blit(text11, textRect11)
        screen.blit(text12, textRect12)
        screen.blit(text13, textRect13)
        screen.blit(text14, textRect14)
        screen.blit(text15, textRect15)
        screen.blit(text19, textRect19)
        screen.blit(text20, textRect20)
        screen.blit(text24, textRect24)
        screen.blit(text25, textRect25)
        reset.draw(screen)
        wall.draw(screen)
        squach.draw(screen)
        position.draw(screen)
        machine.draw(screen)
        squach1.draw(screen)
        squach2.draw(screen)
        Basket.draw(screen)
        line.draw(screen)
        X_axis1.draw(screen)
        Y_axis1.draw(screen)
        c3.draw(screen)
        c4.draw(screen)
        c5.draw(screen)
        
    if start.isMouseOn()==True:
        Show_Result=True
        Show_Setup=False
    if reset.isMouseOn()==True:
        Show_Result=False
        Show_Setup=True
    
    if input_box1.text!='' and input_box2.text!='' and input_box3.text!='':
        x_basket = int(input_box1.text)
        y_basket = int(input_box2.text)
        spring_recoil = int(input_box3.text)
        sim = Calculater(x_basket,y_basket,spring_recoil)
        v=sim.calCulate_velocity(1498.25)
        height=sim.calCulate_height_of_squash()
        x_machine=sim.calCulate_position_machine()[0]
        y_machine=sim.calCulate_position_machine()[1]
        squach = Circle(260,430-(height*100),6,(0,0,0))
        
    
    for event in pg.event.get():
        for box in input_boxes:
            box.handle_event(event)
        if event.type == pg.QUIT:
            pg.quit()
            run = False
    if Show_Setup==True and Show_Result==False:
        screen.blit(text4, textRect4)
    if Show_Setup==False and Show_Result==True:
        screen.blit(text9, textRect9)
    pg.time.delay(1)
    pg.display.update()

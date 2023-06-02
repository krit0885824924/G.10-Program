class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        
        if event.type == pg.MOUSEBUTTONDOWN:# ทำการเช็คว่ามีการคลิก Mouse หรือไม่
            if self.rect.collidepoint(event.pos): #ทำการเช็คว่าตำแหน่งของ Mouse อยู่บน InputBox นี้หรือไม่
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE # เปลี่ยนสีของ InputBox
            
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
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)
        
    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, Screen):
        # Blit the text.
        Screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(Screen, self.color, self.rect, 2)
        
class Rectangle:
    def __init__(self,x=0,y=0,w=0,h=0):
        self.x = x # Position X
        self.y = y # Position Y
        self.w = w # Width
        self.h = h # Height
    def draw(self,screen):
        pg.draw.rect(screen,(255,153,51),(self.x,self.y,self.w,self.h))
class Button(Rectangle):
    def __init__(self, x=0, y=0, w=0, h=0):
        Rectangle.__init__(self, x, y, w, h)
    
    def isMouseOn(self):
        (x,y) = pg.mouse.get_pos()
        if(self.x<=x<=self.w+self.x and self.y<=y<=self.h+self.y and pg.mouse.get_pressed()[0]==1):
            return True
        pass
class Circle:
    def __init__(self,x,y,r):    
        self.x = x
        self.y = y
        self.r = r
    def draw(self,screen):
        pg.draw.circle(screen,(51,51,255),(self.x,self.y),self.r)
        
class Simulation:
    def __init__(self,x_basket,y_basket,spring_recoil):
        self.x_basket = x_basket
        self.y_basket = y_basket
        self.spring_recoil = spring_recoil
        
    def calCulate_velocity(self, k):
        self.k = k
        m = 0.32782
        u = ((self.k)*(((self.spring_recoil/100)**2)/m)-(19.62*m*(self.spring_recoil/100)))**0.5
        self.u = u
        # print(u)
        return self.u
    
    def calCulate_height_of_squash(self):
        self.ux = self.u*math.cos(math.radians(60))
        self.uy =self.u*math.sin(math.radians(60))
        height_of_squash = (self.uy*((130-self.y_basket)/self.ux)/100)-(4.905*(((130-self.y_basket))/100/self.ux)**2)
        # print(height_of_squash)
        return height_of_squash
        
    def calCulate_position_machine(self):
        t = (self.uy+((((self.uy)**2)-(4*4.905*0.06165))**0.5))/9.81
        sx = self.ux*t
        self.x_machine = self.x_basket+15
        self.y_machine = -(sx-2.39915)*100
        # print(t,sx)
        # print(self.x_machine,self.y_machine)
        return [('%.2f'%(self.x_machine)),('%.2f' %(self.y_machine))]
        
# class Text:
#     def __init__(self,font,y,w,h):
#         self.font = font 
#         self.y = y 
#         self.w = w 
#         self.h = h 
        
import sys
import pygame as pg
import math

pg.init()
win_x, win_y = 800, 480
screen = pg.display.set_mode((win_x, win_y))
start = Button(320,300,160,50)
reset = Button(600,400,160,50)
wall = Rectangle(380,350,20,100)

COLOR_INACTIVE = pg.Color('lightskyblue3') # ตั้งตัวแปรให้เก็บค่าสี เพื่อนำไปใช้เติมสีให้กับกล่องข้อความตอนที่คลิกที่กล่องนั้นๆอยู่
COLOR_ACTIVE = pg.Color('dodgerblue2')     # ^^^
FONT = pg.font.Font(None, 32)

input_box1 = InputBox(170, 120, 20, 32) # สร้าง InputBox1
input_box2 = InputBox(420, 120, 20, 32) # สร้าง InputBox2
input_box3 = InputBox(300, 225, 20, 32)
input_boxes = [input_box1, input_box2, input_box3] # เก็บ InputBox ไว้ใน list เพื่อที่จะสามารถนำไปเรียกใช้ได้ง่าย
run = True

font = pg.font.Font('freesansbold.ttf', 16) 
font1 = pg.font.Font('freesansbold.ttf', 24) 
font3 = pg.font.Font('freesansbold.ttf', 20)
text1 = font.render('Baskets position on X-axis', True, (0,0,0)) 
textRect1 = text1.get_rect() 
textRect1.center = (265, 110)
text2 = font.render('Baskets position on Y-axis', True, (0,0,0)) 
textRect2 = text2.get_rect()
textRect2.center = (520, 110)
text3 = font.render('Spring recoil', True, (0,0,0)) 
textRect3 = text3.get_rect() 
textRect3.center = (400, 210)
text4 = font.render('Start', True, (0,0,0)) 
textRect4 = text4.get_rect() 
textRect4.center = (395, 325)
text5 = font1.render('SETUP', True, (0,0,0)) 
textRect5 = text5.get_rect() 
textRect5.center = (390, 50)
text6 = font1.render('RESULT', True, (0,0,0)) 
textRect6 = text6.get_rect() 
textRect6.center = (390, 50)
text7 = font.render('Machines position on X-axis :', True, (0,0,0)) 
textRect7 = text7.get_rect() 
textRect7.center = (250, 130)
text8 = font.render('Machines position on Y-axis :', True, (0,0,0)) 
textRect8 = text8.get_rect() 
textRect8.center = (250, 180)
text9 = font.render('Reset', True, (0,0,0)) 
textRect9 = text9.get_rect() 
textRect9.center = (680, 425)
text10 = font.render('Squash balls height when crossig the wall', True, (0,0,0)) 
textRect10 = text10.get_rect() 
textRect10.center = (400,230)
text11 = font.render('CM', True, (0,0,0)) 
textRect11 = text11.get_rect() 
textRect11.center = (500, 130)
text12 = font.render('CM', True, (0,0,0)) 
textRect12 = text12.get_rect() 
textRect12.center = (500, 180)

Show_Setup=True
Show_Result=False
while run:
    screen.fill((255,255, 204))
    if Show_Setup==True and Show_Result==False:
        for box in input_boxes:
            box.update() 
            box.draw(screen) 
        screen.blit(text1, textRect1)
        screen.blit(text2, textRect2)
        screen.blit(text3, textRect3)
        screen.blit(text5, textRect5)
        start.draw(screen)
        
    if Show_Setup==False and Show_Result==True:
        text13 = font3.render(str(x_machine), True, (0,0,0)) 
        textRect13 = text13.get_rect()
        textRect13.center = (430, 130)
        text14 = font3.render(str(y_machine), True, (0,0,0)) 
        textRect14 = text14.get_rect()
        textRect14.center = (430, 180)
        text15 = font3.render(str('%.2f'%(height*100))+"  CM", True, (0,0,0)) 
        textRect15 = text15.get_rect()
        textRect15.center = (400, 250)
        screen.blit(text6, textRect6)
        screen.blit(text7, textRect7)
        screen.blit(text8, textRect8)
        screen.blit(text10, textRect10)
        screen.blit(text11, textRect11)
        screen.blit(text12, textRect12)
        screen.blit(text13, textRect13)
        screen.blit(text14, textRect14)
        screen.blit(text15, textRect15)
        reset.draw(screen)
        wall.draw(screen)
        squach.draw(screen)
        
    if start.isMouseOn()==True:
        Show_Result=True
        Show_Setup=False
    if reset.isMouseOn()==True:
        Show_Result=False
        Show_Setup=True
        # input_box1.handle_event.
        # input_box2.handle_event.
        # input_box3.handle_event.
    
    if input_box1.text!='' and input_box2.text!='' and input_box3.text!='':
        x_basket = int(input_box1.text)
        y_basket = int(input_box2.text)
        spring_recoil = int(input_box3.text)
        # print(x_basket,y_basket,spring_recoil)
        # x_machine = str(x_basket+15)
        # y_machine = str(y_basket-30)
        sim = Simulation(x_basket,y_basket,spring_recoil)
        v=sim.calCulate_velocity(1498.25)
        height=sim.calCulate_height_of_squash()
        x_machine=sim.calCulate_position_machine()[0]
        y_machine=sim.calCulate_position_machine()[1]
        squach = Circle(390,430-(height*100),8)
        # print(height)
    
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

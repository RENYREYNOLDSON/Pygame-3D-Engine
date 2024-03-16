import pygame,sys,random,math
from pygame.locals import *
pygame.init()

screen=pygame.display.set_mode((1600,900))
pygame.display.set_caption("3D World Engine")
clock=pygame.time.Clock()


#Images / replace this later
lightImg=pygame.image.load("circle.png").convert_alpha()
playerImg=pygame.image.load("blueCharacter2.png").convert_alpha()


#Colours
grey=(50,50,50)
blue=(0,0,255)


#Major Variables
camerax,cameray=0,0
scrollSpeed=4
yChange=0
xChange=0
currentAngle=0#Used to track players angle
xShake,yShake=20,20


#Changable Variables
lineWidth=3
gridWidth=4

rainLength=1000
rainWidth=1
rainSpeed=80
raining=False
rainColour=(80,80,80)


minShake=10
maxShake=50#50 is a good max for screen shake, may want to limit this

health=100




class Building():
    def __init__(self,x,y,w,h,height,colour):
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.height=height
        self.colour=colour
        self.roof_w=self.w*0.01*self.height
        self.roof_h=self.h*0.01*self.height
        #Multipliers for roofs positioning
        #DO w/(w*0.01*self.height)*0.5 for multiplier
        self.xAdd=((self.roof_w-self.w)/2)
        self.yAdd=((self.roof_h-self.h)/2)

        
    def draw(self):
        #Need to calulate roof width and height and adjust location
        #self.colour=randomColour()
        
        xDistance=(self.x-800+camerax+self.xAdd*0.5)*(0.005*self.height)
        yDistance=(self.y-450+cameray+self.yAdd*0.5)*(0.005*self.height)
    
        #South Side
        polygon=[(self.x+camerax,self.y+cameray+self.h),(self.x+camerax+self.w,self.y+cameray+self.h),(camerax+self.x+xDistance+self.w+self.xAdd,cameray+self.y+yDistance+self.h+self.yAdd),(camerax+self.x+xDistance-self.xAdd,cameray+self.y+yDistance+self.h+self.yAdd)]
        pygame.draw.polygon(screen,self.colour,polygon,0)
        #North Side
        polygon=[(self.x+camerax,self.y+cameray),(self.x+camerax+self.w,self.y+cameray),(camerax+self.x+xDistance+self.w+self.xAdd,cameray+self.y+yDistance-self.yAdd),(camerax+self.x+xDistance-self.xAdd,cameray+self.y+yDistance-self.yAdd)]
        pygame.draw.polygon(screen,self.colour,polygon,0)
        #East Side
        polygon=[(self.x+camerax+self.w,self.y+cameray+self.h),(self.x+camerax+self.w,self.y+cameray),(camerax+self.x+xDistance+self.w+self.xAdd,cameray+self.y+yDistance-self.yAdd),(camerax+self.x+xDistance+self.w+self.xAdd,cameray+self.y+yDistance+self.h+self.yAdd)]
        pygame.draw.polygon(screen,self.colour,polygon,0)
        #West Side
        polygon=[(self.x+camerax,self.y+cameray+self.h),(self.x+camerax,self.y+cameray),(camerax+self.x+xDistance-self.xAdd,cameray+self.y+yDistance-self.yAdd),(camerax+self.x+xDistance-self.xAdd,cameray+self.y+yDistance+self.h+self.yAdd)]
        pygame.draw.polygon(screen,self.colour,polygon,0)
        #roof
        pygame.draw.rect(screen,self.colour,(camerax+self.x+xDistance-self.xAdd,cameray+self.y+yDistance-self.yAdd,self.roof_w,self.roof_h),0)
        pygame.draw.rect(screen,(0,0,0),(camerax+self.x+xDistance-self.xAdd,cameray+self.y+yDistance-self.yAdd,self.roof_w,self.roof_h),lineWidth)


        #Drawinh Lines

        #Top Left 
        if (self.y<self.y+yDistance-self.yAdd) or (self.x<self.x+xDistance-self.xAdd):
            pygame.draw.line(screen,(0,0,0),(camerax+self.x,cameray+self.y),(camerax+self.x+xDistance-self.xAdd,cameray+self.y+yDistance-self.yAdd),lineWidth)
        #Top right
        if (self.y<self.y+yDistance-self.yAdd) or (self.x+self.w>self.x+xDistance+self.roof_w-self.xAdd):
            pygame.draw.line(screen,(0,0,0),(camerax+self.x+self.w,cameray+self.y),(camerax+self.x+xDistance+self.w+self.xAdd,cameray+self.y+yDistance-self.yAdd),lineWidth)
        #Bottom Left
        if (self.y+self.h>self.y+yDistance+self.roof_h-self.yAdd) or (self.x<self.x+xDistance-self.xAdd):
            pygame.draw.line(screen,(0,0,0),(camerax+self.x,cameray+self.y+self.h),(camerax+self.x+xDistance-self.xAdd,cameray+self.y+yDistance+self.h+self.yAdd),lineWidth)
        #Bottom Right
        if (self.y+self.h>self.y+yDistance+self.roof_h-self.yAdd) or (self.x+self.w>self.x+xDistance+self.roof_w-self.xAdd):
            pygame.draw.line(screen,(0,0,0),(camerax+self.x+self.w,cameray+self.y+self.h),(camerax+self.x+xDistance+self.w+self.xAdd,cameray+self.y+yDistance+self.h+self.yAdd),lineWidth)


        if collide(800,450,self.x+camerax,self.y+cameray,self.w,self.h) and self.colour!=(255,0,0):
            self.colour=blue
            triggerScreenShake(30,30)

        #Make only draw when on screen? use calculated distance to set max
        #Add roof options
        #Add optional extras
        #Add interiors, as seperate attatched class
        #Add lamp-posts
        #Then add roads in a seperate class
        #Then add player sprite
        #Create a demo map
        #Add way to build towers
        #Fix long buildings
        #If roof is very large, smaller building can overlap 
            #Fix perspective still issues, addition multiplier in xDistance and yDistance must be unique for each?
        #Make it so grid can be taken as land?
            
            

        
    
buildingList=[Building(600,300,200,100,200,grey),#Minimum height currently about 200
              Building(600,600,200,100,200,grey),
              Building(900,250,200,200,300,grey),
              Building(900,700,50,70,200,grey),#Only works for height 200!!!!! must be perfect spot, need to do division
              Building(300,700,100,300,240,grey),
              Building(600,750,100,100,300,grey),
              Building(400,500,100,100,300,grey),
              Building(550,500,50,20,300,grey),
              Building(300,200,100,100,200,grey),
              Building(1020,600,200,150,200,grey)]

class Rain():
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.height=500
        
    def process(self):
        global rainList

        
        vectorx=(self.x-(1600/2))/(1600/2)
        vectory=(self.y-(900/2))/(900/2)
        pygame.draw.line(screen,rainColour,(self.x+vectorx*math.sqrt(self.height),self.y+vectory*math.sqrt(self.height)),
                         (self.x+vectorx*math.sqrt(self.height+rainLength),self.y+vectory*math.sqrt(self.height+rainLength)),rainWidth)
                         
        
        self.height-=rainSpeed
        if self.height<=0:
            pygame.draw.rect(screen,rainColour,(self.x,self.y,2,2),0)
            rainList.remove(self)
        















##Utility Functions

def randomColour():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

def collide(checkx,checky,x,y,w,h):
    if checkx>x and checkx<x+w and checky>y and checky<y+h:
        return True
    else:
        return False

def rotateCentre(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image




    

def drawPlayer():
    global currentAngle
    if xChange==-scrollSpeed and yChange==0:#East
        currentAngle=0
    elif xChange==-scrollSpeed and yChange==-scrollSpeed:#South east
        currentAngle=315
    elif xChange==0 and yChange==-scrollSpeed:#South 
        currentAngle=270
    elif xChange==scrollSpeed and yChange==-scrollSpeed:#South West
        currentAngle=225
    elif xChange==scrollSpeed and yChange==0:#West
        currentAngle=180
    elif xChange==scrollSpeed and yChange==scrollSpeed:#North West
        currentAngle=135
    elif xChange==0 and yChange==scrollSpeed:#South 
        currentAngle=90
    elif xChange==-scrollSpeed and yChange==scrollSpeed:#South 
        currentAngle=45

    image=rotateCentre(playerImg,currentAngle)

    
    screen.blit(image,(790,440))




def drawBuildings():
    for i in buildingList:
        i.draw()
        

def orderBuildings():#Bubble sort for distance from player
    global buildingList
    changed=1
    while changed!=0:
        changed=0
        for i in range(len(buildingList)-1):
            distanceCurrent=math.sqrt((camerax+buildingList[i].x+buildingList[i].w/2-800)**2+(cameray+buildingList[i].y+buildingList[i].h/2-450)**2)
            distanceNext=math.sqrt((camerax+buildingList[i+1].x+buildingList[i+1].w/2-800)**2+(cameray+buildingList[i+1].y+buildingList[i+1].h/2-450)**2)
            if distanceCurrent<distanceNext:
                temp=buildingList[i]
                buildingList[i]=buildingList[i+1]
                buildingList[i+1]=temp


def lightFilter():
    global lightImg
    filter1=pygame.surface.Surface((1600,900))
    filter1.fill((30,30,30))
    lightImg=pygame.transform.scale(lightImg,(200,200))
    filter1.blit(lightImg,(700,350))
    screen.blit(filter1,(0,0),special_flags=pygame.BLEND_RGBA_SUB)

def drawGrid():
    for x in range(40):
        pygame.draw.line(screen,(70,70,70),(camerax-200+x*50,0),(camerax-200+x*50,900),gridWidth)
    for y in range(40):
        pygame.draw.line(screen,(70,70,70),(0,cameray-550+y*50),(1600,cameray-550+y*50),gridWidth)

def manageScreenShake():
    #This will shake the screen using random and decreasing movement
    #Uses the xShake and yShake to adjust the camera's position , or surface?
    global xShake,yShake
    if xShake!=0 or yShake!=0:
        screen.blit(screen,(random.choice([xShake,-xShake]),random.choice([yShake,-xShake])))
    if xShake!=0:
        xShake-=1
    if yShake!=0:
        yShake-=1

def triggerScreenShake(x,y):
    global xShake,yShake
    xShake+=x
    yShake+=y
    if xShake>maxShake:
        xShake=maxShake
    if yShake>maxShake:
        yShake=maxShake

        
def movePlayer():
    global camerax,cameray
    camerax+=xChange
    cameray+=yChange
    for i in buildingList:
        #above
        if (collide(790,440,camerax+i.x,cameray+i.y,i.w,i.h) or collide(810,440,camerax+i.x,cameray+i.y,i.w,i.h)) and yChange>0:
            cameray-=yChange
            
        #below
        if (collide(790,460,camerax+i.x,cameray+i.y,i.w,i.h) or collide(810,460,camerax+i.x,cameray+i.y,i.w,i.h)) and yChange<0:
            cameray-=yChange
        #right
        if (collide(810,440,camerax+i.x,cameray+i.y,i.w,i.h) or collide(810,460,camerax+i.x,cameray+i.y,i.w,i.h)) and xChange<0:
            camerax-=xChange
        #left
        if (collide(790,440,camerax+i.x,cameray+i.y,i.w,i.h) or collide(790,460,camerax+i.x,cameray+i.y,i.w,i.h)) and xChange>0:
            camerax-=xChange

        #Need to stop sticking to vertical walls?
        #Make so if touching door, they can enter


def rainFall():
    global rainList
    edge=200
    for i in range(20):
        rainList.append(Rain(-edge+random.randint(0,1600+edge*2),-edge+random.randint(0,900+edge*2)))

    for rain in rainList:
        rain.process()





rainList=[]





            

while True:
    screen.fill((60,60,60))

    drawGrid()
    drawPlayer()
    #Where floor objects can be drawn, lights, items etc


    
    drawBuildings()
    orderBuildings()

    if raining==True:
        rainFall()
    
    lightFilter()


    manageScreenShake()
    movePlayer()

    

    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==KEYDOWN:
            if event.key==K_d or event.key==K_RIGHT:
                xChange-=scrollSpeed
            elif event.key==K_a or event.key==K_LEFT:
                xChange+=scrollSpeed
            if event.key==K_w or event.key==K_UP:
                yChange+=scrollSpeed
            elif event.key==K_s or event.key==K_DOWN:
                yChange-=scrollSpeed
        
            elif event.key==K_t:#Screen shake
                triggerScreenShake(30,30)
            elif event.key==K_y:#Lose health
                health-=1
            elif event.key==K_r:#Lose health
                raining=not raining

        elif event.type==KEYUP:
            if event.key==K_d or event.key==K_RIGHT:
                xChange+=scrollSpeed
            elif event.key==K_a or event.key==K_LEFT:
                xChange-=scrollSpeed
            elif event.key==K_w or event.key==K_UP:
                yChange-=scrollSpeed
            elif event.key==K_s or event.key==K_DOWN:
                yChange+=scrollSpeed




    pygame.display.flip()
    clock.tick(60)





#Shadow can be moved around screen by moving the light source
#Add smoke
#Add lights
#Add doors and interiors
#Add player sprite
#Add enemies?
#Add a currency
#Add info on hovor over building
#Add health or something? maybe 1 lifetime, must conquer city. Then start new gang and go again with same map?
#Could create layers with surfaces? not being cleared? use for floor light etc
#Sort health System and age
#Add rainbow buildings for certina events as it is super fucking cool
#Make rain stop on buildings?
#Adding scroll feature i think




    

import pygame,sys,random,math
from pygame.locals import *
pygame.init()

screen=pygame.display.set_mode((1600,900))
pygame.display.set_caption("3D World Engine V3")
clock=pygame.time.Clock()


#Images / replace this later
lightImg=pygame.image.load("circle.png").convert_alpha()
playerImg=pygame.image.load("blueCharacter2.png").convert_alpha()

#Fonts
fontObj = pygame.font.Font('freesansbold.ttf', 20)##font


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
toggleFullscreen=False
toggleLighting=True
fps=60


#Enviroment Colours
floorColour=(60,60,60) #60 60 60
gridColour=(70,70,70) #70 70 70
buildingColour=grey #50 50 50
buildingLineColour=(0,0,0) #0 0 0



#Changable Variables
lineWidth=3
gridWidth=4

rainLength=1000
rainWidth=1
rainSpeed=80
raining=False
rainColour=(80,80,80)

zoomLevel=1
zoomSpeed=0.1

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
            pygame.draw.line(screen,buildingLineColour,(camerax+self.x,cameray+self.y),(camerax+self.x+xDistance-self.xAdd,cameray+self.y+yDistance-self.yAdd),lineWidth)
        #Top right
        if (self.y<self.y+yDistance-self.yAdd) or (self.x+self.w>self.x+xDistance+self.roof_w-self.xAdd):
            pygame.draw.line(screen,buildingLineColour,(camerax+self.x+self.w,cameray+self.y),(camerax+self.x+xDistance+self.w+self.xAdd,cameray+self.y+yDistance-self.yAdd),lineWidth)
        #Bottom Left
        if (self.y+self.h>self.y+yDistance+self.roof_h-self.yAdd) or (self.x<self.x+xDistance-self.xAdd):
            pygame.draw.line(screen,buildingLineColour,(camerax+self.x,cameray+self.y+self.h),(camerax+self.x+xDistance-self.xAdd,cameray+self.y+yDistance+self.h+self.yAdd),lineWidth)
        #Bottom Right
        if (self.y+self.h>self.y+yDistance+self.roof_h-self.yAdd) or (self.x+self.w>self.x+xDistance+self.roof_w-self.xAdd):
            pygame.draw.line(screen,buildingLineColour,(camerax+self.x+self.w,cameray+self.y+self.h),(camerax+self.x+xDistance+self.w+self.xAdd,cameray+self.y+yDistance+self.h+self.yAdd),lineWidth)


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
            
            

        
    
buildingList=[Building(600,300,200,100,200,buildingColour),#Minimum height currently about 200
              Building(600,600,200,100,200,buildingColour),
              Building(900,250,200,200,300,buildingColour),
              Building(900,700,50,70,200,buildingColour),#Only works for height 200!!!!! must be perfect spot, need to do division
              Building(300,700,100,300,240,buildingColour),
              Building(600,750,100,100,300,buildingColour),
              Building(400,500,100,100,300,buildingColour),
              Building(550,500,50,20,300,buildingColour),
              Building(300,200,100,100,200,buildingColour),
              Building(1020,600,200,150,200,buildingColour)]

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


def collideBoxes(x1,y1,w1,h1,x2,y2,w2,h2):#Box collide, compares two rectangles for collision
    if collide(x1,y1,x2,y2,w2,h2) or collide(x1+w1,y1,x2,y2,w2,h2) or collide(x1+w1,y1+h1,x2,y2,w2,h2) or collide(x1,y1+h1,x2,y2,w2,h2) or collide(x2,y2,x1,y1,w1,h1) or collide(x2+w2,y2,x1,y1,w1,h1) or collide(x2+w2,y2+h2,x1,y1,w1,h1) or collide(x2,y2+h2,x1,y1,w1,h1) :
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
        pygame.draw.line(screen,gridColour,(camerax-200+x*50,0),(camerax-200+x*50,900),gridWidth)
    for y in range(40):
        pygame.draw.line(screen,gridColour,(0,cameray-550+y*50),(1600,cameray-550+y*50),gridWidth)

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

def generateRandomMap(cameraPosition,mapDimensions,numberBuildings,heightLimits,buildingWidthLimits,buildingHeightLimits):#camera,dimensions,num buildings,height limits,width limits, height limits
    global buildingList#The funtion creates many buildings which should not overlap
    buildingList=[]
    for i in range(numberBuildings):
        placed=False
        while placed==False:
            placed=True
            x=random.randint(cameraPosition[0],cameraPosition[0]+mapDimensions[0])
            y=random.randint(cameraPosition[1],cameraPosition[1]+mapDimensions[1])
            w=random.randint(buildingWidthLimits[0],buildingWidthLimits[1])
            h=random.randint(buildingHeightLimits[0],buildingHeightLimits[1])
            for b in buildingList:
                if collideBoxes(x-50,y-50,w+100,h+100,b.x,b.y,b.w,b.h):#The 50 and 100 are so buildings dont touch, set distance apart
                    placed=False
        height=random.randint(heightLimits[0],heightLimits[1])
        buildingList.append(Building(x,y,w,h,height,buildingColour))



def scaleScreen():
    #Shows zoomed screen, uses the blit to only blit part of the image. SHould use this more!
    newScreen=pygame.transform.scale(screen,(int(1600*zoomLevel),int(900*zoomLevel)))
    screen.blit(newScreen,(0,0),((1600*zoomLevel-1600)/2,(900*zoomLevel-900)/2,1600,900))


            

while True:
    screen.fill(floorColour)

    drawGrid()
    drawPlayer()
    #Where floor objects can be drawn, lights, items etc


    drawBuildings()
    orderBuildings()

    if raining==True:
        rainFall()
        
    if toggleLighting==True:
        lightFilter()


    manageScreenShake()
    movePlayer()

    scaleScreen()
    
    #Put GUI below here

    

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




            #Special dev keys
            elif event.key==K_t:#Screen shake
                triggerScreenShake(30,30)
                
            elif event.key==K_y:#Lose health
                health-=1
                
            elif event.key==K_r:#Toggle Rain
                raining=not raining
                
            elif event.key==K_g:#Generate new map
                generateRandomMap((0,0),(1000,1000),20,(200,300),(80,200),(80,200))
                
            elif event.key==K_f:#Toggle Fullscreen
                if toggleFullscreen==False:
                    toggleFullscreen=True
                    screen=pygame.display.set_mode((1600,900),FULLSCREEN)
                else:
                    toggleFullscreen=False
                    screen=pygame.display.set_mode((1600,900))
                    
            elif event.key==K_l:#Toggle Lighting System
                toggleLighting=not toggleLighting







        elif event.type==KEYUP:
            if event.key==K_d or event.key==K_RIGHT:
                xChange+=scrollSpeed
            elif event.key==K_a or event.key==K_LEFT:
                xChange-=scrollSpeed
            elif event.key==K_w or event.key==K_UP:
                yChange-=scrollSpeed
            elif event.key==K_s or event.key==K_DOWN:
                yChange+=scrollSpeed
                
        elif event.type==MOUSEBUTTONDOWN:#Zooming
            if event.button==5:
                if zoomLevel>1:
                    zoomLevel-=zoomSpeed
            elif event.button==4:
                if zoomLevel<2:
                    zoomLevel+=zoomSpeed

    fpstext = fontObj.render(str(int(clock.get_fps())), True, (255,215,0))
    screen.blit(fpstext,(10,10))
  
    pygame.display.flip()
    clock.tick(fps)


#FIX COLLIDEBOXES funtion as their middles can still overlap


#Shadow can be moved around screen by moving the light source
#Add smoke
#Add lights
#Add doors and interiors
#Add enemies?
#Add a currency
#Add info on hovor over building
#Add health or something? maybe 1 lifetime, must conquer city. Then start new gang and go again with same map?
#Could create layers with surfaces? not being cleared? use for floor light etc
#Sort health System and age
#Add rainbow buildings for certina events as it is super fucking cool
#Make buildings not drawn when off screen
#Add system to speed up and slow down due to framerate
#Add floor/puddle system
#Make run better tho
#Add map size at start to limit movement and fill window with the grid








    
    

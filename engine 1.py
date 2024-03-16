import pygame,sys,random,math
from pygame.locals import *
pygame.init()

screen=pygame.display.set_mode((1600,900))
pygame.display.set_caption("3D World Engine")
clock=pygame.time.Clock()

lightImg=pygame.image.load("circle.png").convert_alpha()

#Colours
grey=(50,50,50)

#Major Variables
camerax,cameray=0,0
scrollSpeed=4
yChange=0
xChange=0


#Changable Variables
lineWidth=4

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


        #Add shadows
        #Make only draw when on screen?
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
        #Sort Perspective - Roof TOO far to the left

        
    
buildingList=[Building(600,300,200,100,200,grey),#Minimum height currently about 200
              Building(600,600,200,100,200,grey),
              Building(900,250,200,200,300,grey),
              Building(900,700,50,70,200,grey),#Only works for height 200!!!!! must be perfect spot, need to do division
              Building(300,700,100,300,240,grey),
              Building(600,750,100,100,300,grey),
              Building(400,500,100,100,300,grey),
              Building(550,500,50,20,300,grey)]

def randomColour():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

"""
buildingList=[]
for i in range(20):
    buildingList.append(Building(random.randint(-100,1600),random.randint(-100,900),random.randint(50,300),random.randint(50,300),random.randint(100,300),randomColour()))
"""

def drawPlayer():
    pygame.draw.rect(screen,(100,0,0),(790,440,20,20),0)

def drawBuildings():
    for i in buildingList:
        i.draw()


def orderBuildings():#Bubble sort for distance from player
    global buildingList
    changed=1
    while changed!=0:
        changed=0
        for i in range(len(buildingList)-1):
            distanceCurrent=math.sqrt((camerax+buildingList[i].x-800)**2+(cameray+buildingList[i].y-450)**2)
            distanceNext=math.sqrt((camerax+buildingList[i+1].x-800)**2+(cameray+buildingList[i+1].y-450)**2)
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

while True:
    screen.fill((60,60,60))

    drawPlayer()
    #Where floor objects can be drawn, lights, items etc


    
    drawBuildings()
    orderBuildings()
    lightFilter()

    camerax+=xChange
    cameray+=yChange
    

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





    

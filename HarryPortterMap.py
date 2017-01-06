import pygame


class PixelCoord:
    x = 0
    y = 0
    center = 0

    def __init__(self):
        self.x = 0
        self.y = 0
        self.center = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.center = 0

    def __str__(self):
        return "object  x : %s, y : %s, center : %s" % (self.x, self.y, self.center)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getCenter(self):
        return self.center

    def getXY(self):
        return self.x, self.y

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setXY(self, x, y):
        self.x = x
        self.y = y

    def setCenter(self, oneBlockSize):
        self.center = [int(self.x + (oneBlockSize / 2)), int(self.y + (oneBlockSize / 2))]


class PygameGridMap:
    gridSizeX = 0
    gridSizeY = 0

    displayWidth = 0
    displayHeight = 0

    screenWidth = 0
    screenHeight = 0

    oneBlockSize = 0

    beacons = []

    test = "??"
    def __init__(self, gridSizeX, gridSizeY, screenWidth,
                 screenHeight):  # gridsizeX(int) ,gridsizeY(int) , screenWidth(int),screenWidth(int)
        self.gridSizeX = gridSizeX
        self.gridSizeY = gridSizeY

        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

    def setBlockSize(self):
        temp1 = self.screenWidth * 1.0 / self.gridSizeX
        temp2 = self.screenHeight * 1.0 / self.gridSizeY

        # which side is smaller than the opposite side
        if temp1 >= temp2:
            self.oneBlockSize = temp2
            leftMargine = int((self.screenWidth - (self.oneBlockSize * self.gridSizeX)) / 2)
            for x in range(0, self.gridSizeX):
                for y in range(0, self.gridSizeY):
                    self.gridWorld[y][x].setY(y * self.oneBlockSize)
                    self.gridWorld[y][x].setX(leftMargine + x * self.oneBlockSize)
                    self.gridWorld[y][x].setCenter(self.oneBlockSize)


        else:
            self.oneBlockSize = temp1
            topMargine = int((self.screenHeight - (self.oneBlockSize * self.gridSizeY)) / 2)
            for y in range(0, self.gridSizeY):
                for x in range(0, self.gridSizeX):
                    self.gridWorld[y][x].setX(x * self.oneBlockSize)
                    self.gridWorld[y][x].setY(topMargine + y * self.oneBlockSize)
                    self.gridWorld[y][x].setCenter(self.oneBlockSize)

    def initGridArray(self):
        self.gridWorld = [[PixelCoord(0, 0) for col in range(self.gridSizeX)] for row in range(self.gridSizeY)]

    def printGridWorld(self):
        for y in range(0, self.gridSizeY):
            for x in range(0, self.gridSizeX):
                print self.gridWorld[y][x]

    # return type : [int, int]
    def changeGridCoordToPixel(self,gridX,gridY):
        return self.gridWorld[gridY][gridX].getCenter()

    def createBeacon(self,id,gridX,gridY):
        pixelX,pixelY = self.changeGridCoordToPixel(gridX,gridY)
        self.beacons.append(Beacon(id,pixelX,pixelY))

    def updateBeacon(self,key,destx,desty,speed):
        for beacon in self.beacons :
            if beacon.beaconID == key:
                beacon.update(destx,desty,speed)





import math
class Beacon:
    beaconID = ""
    x = 0
    y = 0
    destX = 0
    destY = 0
    pos = (0, 0)
    directionAngle = 0.0
    distance = 0.0
    speed = 0
    arrival = False
    def __init__(self, beaconid, x, y,):
        self.beaconID = beaconid
        self.setBeaconPos(x,y)

    def update(self,destx,desty,speed):
        self.setDestination(destx,desty)
        self.updateDistance()
        self.speed = speed

        if self.x > self.destX:
            self.x - self.speed
        else:
            self.x + self.speed

        if self.y > self.destY:
            self.y - self.speed
        else:
            self.y + self.speed


    def setBeaconPos(self,x,y):
        self.x = x
        self.y = y

    def setDestination(self, destx, desty):
        self.destX = destx
        self.destY = desty

    def updateDistance(self):
        if self.destX == self.x and self.destY == self.y:
            self.distance = math.sqrt(math.pow((self.destX - self.x), 2) + math.pow((self.destY - self.y), 2))
            print self.distance
            self.arrival = True
        else:
            self.distance = math.sqrt(math.pow( (self.destX - self.x) ,2 ) + math.pow((self.destY -self.y),2))
            print self.distance








import thread

def printhi(none):
    while 1:
        print "hi"
thread.start_new_thread( printhi, (None,) )

beaconsDic = {}
bdcount = 0

beaconsDic["sim"] = [3,2]
beaconsDic["test2"] = [2,2]
beaconsDic["test1"] = [1,2]
bdcount = 3
'''
print dic["test3"]
print dic["test2"]
print dic["test1"]

for d in dic:
    if d == "test2":
        print " key"
'''

pygameGridMap = PygameGridMap(10, 5, 700, 500)
pygameGridMap.initGridArray()
pygameGridMap.setBlockSize()
pygameGridMap.printGridWorld()
# Initialize the game engine
pygame.init()
size = [700, 500]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("foot tracker")

done = False
clock = pygame.time.Clock()

while not done:
    clock.tick(10)
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
    screen.fill((255, 255, 255))

    # Draw a rectangle outline
    for y in range(pygameGridMap.gridSizeY):
        for x in range(pygameGridMap.gridSizeX):
            pygame.draw.rect(screen, (0, 0, 0),
                             [pygameGridMap.gridWorld[y][x].getX(), pygameGridMap.gridWorld[y][x].getY(),
                              pygameGridMap.oneBlockSize, pygameGridMap.oneBlockSize], 2)
    # Draw a solid rectangle
    # pygame.draw.rect(screen, (0,0,0), [150, 10, 50, 20])

    # Draw a circle
    for y in range(pygameGridMap.gridSizeY):
        for x in range(pygameGridMap.gridSizeX):
            pygame.draw.circle(screen, (255, 0, 0), pygameGridMap.gridWorld[y][x].getCenter(), 2)

    num = len(beaconsDic)
    if num > bdcount:
        for i in range(num - bdcount):
            pygameGridMap.createBeacon()

    '''
    for beacon in range(pygameGridMap.beacons):
            pygame.draw.circle(screen,(0,0,255), beacon. ,2 )
    '''

    '''
    # Rectplace = pygame.draw.rect(screen, (255, 0, 0), (100, 100, 100, 100))
    pos = pygame.mouse.get_pos()
    (pressed1, pressed2, pressed3) = pygame.mouse.get_pressed()
    # if statement
    # if Rectplace.collidepoint(pos) & pressed1 == 1:
    # print("You have opened a chest!")
    if pressed1 == 1:
        print pos
    '''


    pygame.display.flip()
# Be IDLE friendly
pygame.quit()

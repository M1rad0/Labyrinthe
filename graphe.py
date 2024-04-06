from math import sqrt
from tkinter import Canvas

class Graphe:
    composantes:list

    def __init__(self,composantes:list) -> None:
        self.composantes=composantes

    def draw(self,canvas:Canvas,echelle:int,lines:bool=True):
        for point in self.composantes:
            point.draw(canvas,echelle,lines)

class Position:
    location:tuple
    adjacent:list
    
    @staticmethod
    def locDist(point1, point2):
        return sqrt(((point2.location[0]-point1.location[0])**2)+((point2.location[1]-point1.location[1])**2))

    def __init__(self,location:tuple,adjacent:list) -> None:
        self.location=location
        self.adjacent=adjacent
    
    def isClicked(self,clickCoord,echelle):
        comparativeMinX=(self.location[0]*echelle)-(echelle/2)
        comparativeMaxX=(self.location[0]*echelle)+(echelle/2)

        comparativeMinY=(self.location[1]*echelle)-(echelle/2)
        comparativeMaxY=(self.location[1]*echelle)+(echelle/2)
        
        if(clickCoord[0]<=comparativeMaxX and clickCoord[0]>=comparativeMinX and clickCoord[1]<=comparativeMaxY and clickCoord[1]>=comparativeMinY):
            return True
        return False

    def bfs(self):
        result=[]
        visited=[self]
        fil=[self]
        while len(fil)>0:
            v=fil[0]
            fil=fil[1:]
            for voisin in v.adjacent:
                if voisin not in visited:
                    visited.append(voisin)
                    result.append(RelativePosition(voisin,v))
                    fil.append(voisin)

        return result

    def shortestPath(self,other):
        allLinked=self.bfs()
        print(len(allLinked))
        isLinked=RelativePosition.searchPosition(allLinked,other)
        print(isLinked)
        if(isLinked!=-1):
            result=[other]
            relative=allLinked[isLinked]
            while(relative.discoverer!=self):
                nextPoint=relative.discoverer
                isLinked=RelativePosition.searchPosition(allLinked,nextPoint)
                result.insert(0,relative.discoverer)
                relative=allLinked[isLinked]
            return result
        else:
            return None

    def linkDistance(self,other):
        result=self.shortestPath(other)
        print(result)
        return len(result)
    
    def draw(self,canvas:Canvas,echelle,lines:bool=True):
        x=(self.location[0]*echelle)
        y=(self.location[1]*echelle)

        canvas.create_oval(x-(echelle/2),y-(echelle/2),x+(echelle/2),y+(echelle/2),fill='black')
        if(lines):
            for adjPoint in self.adjacent:
                canvas.create_line(x,y,adjPoint.location[0]*echelle,adjPoint.location[1]*echelle,smooth=True)
    
    def __eq__(self, __value: object) -> bool:
        return self.location[0]==__value.location[0] and self.location[1]==__value.location[1]


class RelativePosition:
    pos:Position
    discoverer:Position

    def __init__(self,pos:Position,discoverer:Position) -> None:
        self.pos=pos
        self.discoverer=discoverer

    @staticmethod
    def searchPosition(bfsTable,pos:Position):
        for i in range(0,len(bfsTable)):
            if(bfsTable[i].pos==pos):
                return i
        return -1

class Mobile:
    pos:Position

    def __init__(self,pos) -> None:
        self.pos=pos

    def move(self,other:Position):
        for obj in self.pos.adjacent:
            if(other==obj):
                self.pos=other
                return True
        return False
    
def placeOnCircle(centerLoc:tuple,radius:int,x=None,y=None):
    if(x==None and y==None):
        raise Exception("Veuillez choisir une valeur sur un axe entre x et y")

    elif x==None:
        deltax=sqrt((radius**2)-(y**2))
        result=((centerLoc[0]+deltax,centerLoc[1]+y),(centerLoc[0]-deltax,centerLoc[1]+y))

    else:
        deltay=sqrt((radius**2)-(x**2))
        result=((centerLoc[0]+x,centerLoc[1]+deltay),(centerLoc[0]+x,centerLoc[1]-deltay))

    return result
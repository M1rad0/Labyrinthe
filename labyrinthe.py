import random
from time import sleep
from tkinter import Canvas
from graphe import *

class Souris(Mobile):
    def __init__(self, pos) -> None:
        super().__init__(pos)

    def slowMoveTo(self,other,speed,sleepTime):
        if self.pos.location[0]==other.location[0]:
            if self.pos.location[1]>other.location[1]:
                while self.pos.location[1]>other.location[1]:
                    self.pos=Position((self.pos.location[0],self.pos.location[1]-speed),[])
                    sleep(sleepTime)
            else :
                while self.pos.location[1]<other.location[1]:
                    self.pos=Position((self.pos.location[0],self.pos.location[1]+speed),[])
                    sleep(sleepTime)

        elif self.pos.location[1]==other.location[1]:
            if self.pos.location[0]>other.location[0]:
                while self.pos.location[0]>other.location[0]:
                    self.pos=Position((self.pos.location[0]-speed,self.pos.location[1]),[])
                    sleep(sleepTime)
            else :
                while self.pos.location[0]<other.location[0]:
                    self.pos=Position((self.pos.location[0]+speed,self.pos.location[1]),[])
                    sleep(sleepTime)

class Labyrinthe(Graphe):
    souris:Souris
    fieldData:tuple
    sortie:Position
    lineWidth:int

    def __init__(self, composantes: list ,fieldData:tuple , sortie:Position, entree:Position,lineWidth:int) -> None:
        super().__init__(composantes)
        self.fieldData=fieldData
        self.sortie=sortie
        self.souris=Souris(entree)
        self.lineWidth=lineWidth

    def buildFromMatrix(initialPoint:tuple, nbPerLigne:int ,distanceBetweenPoints:int ,matrix:list):
        print(matrix)

        nbElements=len(matrix)
        x=initialPoint[0]
        y=initialPoint[1]
        composantes=[]
        while(len(composantes)<nbElements):
            composantes.append(Position((x,y),[]))
            if(len(composantes)%nbPerLigne==0):
                x=initialPoint[0]
                y+=distanceBetweenPoints
            else:
                x+=distanceBetweenPoints
        
        i=0
        while(i<len(matrix)):
            indCorr=0
            while(indCorr<len(matrix[i])):
                if (composantes[i] in composantes[indCorr].adjacent) or (matrix[i][indCorr]==1 and Position.locDist(composantes[i],composantes[indCorr])==distanceBetweenPoints):
                    composantes[i].adjacent.append(composantes[indCorr])
                    if(composantes[i] not in composantes[indCorr].adjacent):
                        composantes[indCorr].adjacent.append(composantes[i])
                indCorr+=1
            i+=1

        width=distanceBetweenPoints*(nbPerLigne+1)
        height=distanceBetweenPoints*((len(composantes)//nbPerLigne)+1)
        fieldX0=composantes[0].location[0]-distanceBetweenPoints
        fieldY0=composantes[0].location[1]-distanceBetweenPoints
        fieldX1=fieldX0+width
        fieldY1=fieldY0+height

        fieldData=(fieldX0,fieldY0,fieldX1,fieldY1)
        entree=composantes[0]
        sortie=composantes[-1]

        return Labyrinthe(composantes,fieldData,sortie,entree,distanceBetweenPoints//2)
    
    def createRandomMatrix(lignes, colonnes):
        matrice = []
        for i in range(lignes):
            ligne = []
            for j in range(colonnes):
                seed=random.randint(0,100)
                if(seed<60):
                    ligne.append(0)
                else:
                    ligne.append(1)
            matrice.append(ligne)
        return matrice
    
    def createRandomGame(initialPoint:tuple,nbPerLigne:int, distanceBetweenPoints:int,nbPoints:int):
        matrice= Labyrinthe.createRandomMatrix(nbPoints,nbPoints)

        return Labyrinthe.buildFromMatrix(initialPoint,nbPerLigne,distanceBetweenPoints,matrice)

    def drawSouris(self,canvas: Canvas,echelle:int):
        sourisX0=self.souris.pos.location[0]*echelle-(echelle/2)
        sourisY0=self.souris.pos.location[1]*echelle-(echelle/2)
        sourisY1=self.souris.pos.location[1]*echelle+(echelle/2)
        sourisX1=self.souris.pos.location[0]*echelle+(echelle/2)
        self.dessinSouris=canvas.create_oval(sourisX0,sourisY0,sourisX1,sourisY1,fill='blue')

    def draw(self, canvas: Canvas, echelle: int, lines: bool = True):
        canvas.create_rectangle(self.fieldData[0]*echelle,self.fieldData[1]*echelle,self.fieldData[2]*echelle,self.fieldData[3]*echelle,fill='black')
        for point in self.composantes:
            for adjPoint in point.adjacent:
                canvas.create_line((point.location[0])*echelle,point.location[1]*echelle,adjPoint.location[0]*echelle,adjPoint.location[1]*echelle,width=echelle*self.lineWidth,fill='white')
        
        self.drawSouris(canvas,echelle)

        sortieX0=self.sortie.location[0]*echelle-(echelle/2)
        sortieY0=self.sortie.location[1]*echelle-(echelle/2)
        sortieY1=self.sortie.location[1]*echelle+(echelle/2)
        sortieX1=self.sortie.location[0]*echelle+(echelle/2)
        canvas.create_oval(sortieX0,sortieY0,sortieX1,sortieY1,fill='red')

    def drawShortestPath(self,can:Canvas,echelle):
        shortestPath=self.souris.pos.shortestPath(self.sortie)
        if(shortestPath!=None and len(shortestPath)>0):
            actualPoint=self.souris.pos
            for point in shortestPath:
                actualx0,actualy0=actualPoint.location[0]*echelle,actualPoint.location[1]*echelle
                actualx1,actualy1=point.location[0]*echelle,point.location[1]*echelle

                can.create_line(actualx0,actualy0,actualx1,actualy1,fill='blue')
                actualPoint=point
            return shortestPath
        return None
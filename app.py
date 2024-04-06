import threading
from time import sleep
from tkinter import *
from labyrinthe import Labyrinthe

class GameFrame(Tk):
    game:Labyrinthe
    can:Canvas

    def __init__(self, screenName: str | None = None, baseName: str | None = None, className: str = "Labyrinthe", useTk: bool = True, sync: bool = False, use: str | None = None) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use)
        self.game=Labyrinthe.createRandomGame((10,10),10,3,50)
        self.can=Canvas(self,background='white')
        bouton=Button(self,text="Generate New Game")
        self.state('zoomed')

def moveToExtractPoint(game:Labyrinthe,shortestPath:list):
    for toMoveTo in shortestPath:
        game.souris.slowMoveTo(toMoveTo,0.0625,0.02)

def redraw(frame:GameFrame,echelle:int):
    frame.can.delete(frame.game.dessinSouris)
    frame.game.drawSouris(frame.can,echelle)
    frame.after(20,redraw,frame,echelle)

root=GameFrame()
echelle=25

root.game.draw(root.can,echelle,False)
shortestPath=root.game.drawShortestPath(root.can,echelle)
if shortestPath!=None:
    threadBack=threading.Thread(target=moveToExtractPoint,args=[root.game,shortestPath])
    threadBack.start()
    redraw(root,echelle)

root.can.pack(fill=BOTH, expand=1)
root.mainloop()
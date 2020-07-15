from vpython import *
import numpy as np  
import math 
import time 

# USING VIRTUAL PYTHON TO PLOT THE XYZ AXIS 
def drawAxisXYZ():
    origin = vector(0,0,0)
    rateDim = 50
    radius = 0.3
    scene.title = 'X:RED  Y:GREEN  Z:BLUE'
    sphere(pos = origin, radius = 2, color = color.yellow)
    arrow (pos = origin, axis = vector(rateDim,0,0) , shaftwidth=radius, color = color.red)
    arrow (pos = origin, axis = vector(0,rateDim,0) , shaftwidth=radius, color = color.green)
    arrow (pos = origin, axis = vector(0,0,rateDim) , shaftwidth=radius, color = color.blue)
    arrow (pos = origin, axis = vector(-rateDim,0,0), shaftwidth=radius, color = color.red)
    arrow (pos = origin, axis = vector(0,-rateDim,0), shaftwidth=radius, color = color.green)
    arrow (pos = origin, axis = vector(0,0,-rateDim), shaftwidth=radius, color = color.blue)

def vetor(vet = [0,0,0]):
    return vector(vet[0], vet[1], vet[2])

def makeVector(v, p = 1):
    return [[1,0,0,v[0]],[0,1,0,v[1]], [0,0,1,v[2]], [0,0,0,p]]

class Joint():

    # Denavit-Harteberg parameters 
    teta = 0
    d    = 0 
    a    = 0 
    alfa = 0

    dh = 0

    # Parameters to draw the axis in the cartesian plan 
    posi   = vector(0,0,0)
    posf   = vector(0,0,0)

    # To draw the link
    jointLink = cylinder()
    # To draw the end joint 
    jointAxis = sphere() 

    # To do the DH table 
    def DH (self):
        dh_ = np.array([
                [cos(self.teta),-sin(self.teta)*cos(self.alfa), sin(self.teta)*sin(self.alfa), self.a*cos(self.teta)],
                [sin(self.teta), cos(self.teta)*cos(self.alfa),-cos(self.teta)*sin(self.alfa), self.a*sin(self.teta)],
                [0             , sin(self.alfa)          , cos(self.alfa)               , self.d               ],
                [0             , 0                            , 0                            , 1                    ]
            ])
        return dh_
    
    def getDh(self, dh):
        return [dh[i][3] for i in range(3)]

    # The a and alfa parameters wont be necessary in 2D simulation
    def __init__(self, teta, a, posi, make_trail = False):
        self.teta = teta
        self.alfa = 0
        self.d    = 0 
        self.a    = a 

        if posi is 0 :
            self.dh = self.DH()
            self.posi = vector(0,0,0)
            self.posf = vetor(self.getDh(self.dh))
            self.posf = vector(self.posf.x + self.posi.x, self.posf.y + self.posi.y, self.posf.z + self.posi.z)

        else: 
            self.posi = posi
            self.dh   = self.DH()  
            self.posf = vetor(self.getDh(self.dh))
            self.posf = vector(self.posf.x + self.posi.x, self.posf.y + self.posi.y, self.posf.z + self.posi.z)
        
        # To draw the link
        self.jointLink = cylinder(pos = self.posi, axis = self.posf, radius = 1, length = self.a, color = color.white )
        # To draw the end joint 
        self.jointAxis = sphere(pos = self.posf, radius = 1.5, color = color.red, make_trail = make_trail) 
        self.jointAxis.trail_color = color.cyan

    def rotateLink(self, angPlus):
        self.teta = radians( degrees(self.teta) + angPlus)
        self.dh = self.DH()
        self.posf = vetor(self.getDh(self.dh))
        self.jointLink.axis = self.posf
        self.posf = vector(self.posf.x + self.posi.x, self.posf.y + self.posi.y, self.posf.z + self.posi.z)
        self.jointAxis.pos  = self.posf
        self.dh = self.DH()
    
    def moveLink(self, posi):
        self.posi = posi
        self.jointLink.pos = self.posi
        self.dh = self.DH()
        self.posf = vetor(self.getDh(self.dh))
        self.posf = vector(self.posf.x + self.posi.x, self.posf.y + self.posi.y, self.posf.z + self.posi.z)
        self.jointAxis.pos = self.posf


if __name__ == "__main__":
    drawAxisXYZ()

    v1 = Joint(30, 15, 0      , True)
    v2 = Joint(30, 10, v1.posf, True)
    v3 = Joint(30, 15, v2.posf, True)
    v4 = Joint(30, 10, v3.posf, True)

    rate(60)
    i = 0

    while True:
        i=i+1
        if i > 360*3:
            i = 0 
            v1.jointAxis.clear_trail()
            v2.jointAxis.clear_trail()
            v3.jointAxis.clear_trail()
            v4.jointAxis.clear_trail()

        v1.rotateLink(-1)
        
        v2.moveLink(v1.posf)
        v2.rotateLink(3)

        v3.moveLink(v2.posf)
        v3.rotateLink(2)

        v4.moveLink(v3.posf)
        v4.rotateLink(-2)


        print(v4.posf)
        print("%10.4f %10.4f %10.4f %10.4f" %(v1.teta,v2.teta,v3.teta,v4.teta))
        time.sleep(1/60)
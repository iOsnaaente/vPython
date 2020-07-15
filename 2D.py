from vpython import *
import numpy as np  
import math 
import time 

# USING VIRTUAL PYTHON TO PLOT THE XYZ AXIS 
def drawAxisXYZ():
    origin = vector(0,0,0)
    rateDim = 100
    radius = 0.5
    sphere(pos = origin, radius = 2, color = color.yellow)
    arrow (pos = origin, axis = vector(rateDim,0,0) , shaftwidth=radius, color = color.green)
    arrow (pos = origin, axis = vector(0,rateDim,0) , shaftwidth=radius, color = color.green)
    arrow (pos = origin, axis = vector(0,0,rateDim) , shaftwidth=radius, color = color.green)
    arrow (pos = origin, axis = vector(-rateDim,0,0), shaftwidth=radius, color = color.red)
    arrow (pos = origin, axis = vector(0,-rateDim,0), shaftwidth=radius, color = color.red)
    arrow (pos = origin, axis = vector(0,0,-rateDim), shaftwidth=radius, color = color.red)

def vetor(vet = [0,0,0]):
    return vector(vet[0], vet[1], vet[2])

class Joint():

    # Parameters to draw the axis in the cartesian plan 
    posi   = vector(0,0,0)
    posf   = vector(0,0,0)
    axis   = vector(0,0,0)
    
    length = 1
    radius = 1

    ang = 0

    # To draw the link
    jointLink = cylinder()
    # To draw the end joint 
    jointAxis = sphere() 

    def __init__(self, pos=[0,0,0], ang = 0, length=1, make_trail = False):
        
        self.posi = vetor(pos)
        self.ang = radians(ang)
        self.length = length

        x,y,z = cos(ang)*length, sin(ang)*length, 0
        self.posf = vector(self.posi.x + x, self.posi.y + y, self.posi.z + z )

        self.axis = vector(x,y,z)

        # To draw the link
        self.jointLink = cylinder(pos = self.posi, axis = self.axis, radius = self.radius, length = self.length, color = color.white )
        # To draw the end joint 
        self.jointAxis = sphere(pos = self.posf, axis = self.axis, radius = self.radius+0.5, color = color.red, make_trail = make_trail) 
        self.jointAxis.trail_color = color.cyan

    def endLink(self):
        return [self.posf.x, self.posf.y, self.posf.z]

    def rotateLink(self, angPlus):
        self.ang = radians( degrees(self.ang) + angPlus)

        x,y,z = cos(self.ang)*self.length, sin(self.ang)*self.length, 0
        self.posf = vector(self.posi.x + x, self.posi.y + y, self.posi.z + z )
        self.axis = vector(x,y,z)

        self.jointLink.axis = self.axis
        self.jointAxis.pos  = self.posf
    
    def moveLink(self, pos = [0,0,0]):
        x,y,z = cos(self.ang)*self.length, sin(self.ang)*self.length, 0
        self.posf = vector(self.posi.x + x, self.posi.y + y, self.posi.z + z )
        self.axis = vector(x,y,z)
        self.posi = vetor(pos)
        
        self.jointLink.pos = self.posi
        self.jointAxis.pos = self.posi


if __name__ == "__main__":
    drawAxisXYZ()

    joint_origin = Joint([0,0,0]               , 0 , 32, False)
    joint_one    = Joint(joint_origin.endLink(), 90, 16, False)
    joint_two    = Joint(joint_one.endLink()   , 0 , 8 , False)
    joint_three  = Joint(joint_two.endLink()   , 90, 14 , True )
    time.sleep(2)
    

    rate(60)
    while True:

        joint_origin.rotateLink(0.5)
        joint_one.moveLink(joint_origin.endLink())
        joint_one.rotateLink(2)        
        joint_two.moveLink(joint_one.endLink())
        joint_two.rotateLink(3)        
        joint_three.moveLink(joint_two.endLink())
        joint_three.rotateLink(4)

        
        time.sleep(1/120)

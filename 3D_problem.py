from vpython import *
import numpy as np  
import math 
import time 

def makeTrans(vetPos, vetRot, ang):
    vt = vetorTrans(vetPos[0], vetPos[1], vetPos[2])
    vt = np.dot(vetRot(ang), vt)
    print(vt)

    return [ vt[0][3], vt[1][3], vt[2][3] ]


origin = (0,0,0)

vetorRotX = lambda teta : np.array([[ 1, 0           , 0           , 0 ],
                                    [ 0, np.cos(teta),-np.sin(teta), 0 ],
                                    [ 0, np.sin(teta), np.cos(teta), 0 ],
                                    [ 0, 0           , 0           , 1 ]])

vetorRotY = lambda teta : np.array([[ np.cos(teta), 0, np.sin(teta), 0],
                                    [ 0           , 1, 0           , 0],
                                    [-np.sin(teta), 0, np.cos(teta), 0],
                                    [ 0           , 0,            0, 1]])

vetorRotZ = lambda teta : np.array([[ np.cos(teta),-np.sin(teta), 0, 0],
                                    [ np.sin(teta), np.cos(teta), 0, 0],
                                    [ 0           , 0           , 1, 0],
                                    [ 0           , 0           , 0, 1]])

vetorTransX = lambda dx : np.array([[ 1, 0, 0, dx ],
                                    [ 0, 1, 0, 0  ],
                                    [ 0, 0, 1, 0  ],
                                    [ 0, 0, 0, 1  ]])

vetorTransY = lambda dy : np.array([[ 1, 0, 0, 0  ],
                                    [ 0, 1, 0, dy ],
                                    [ 0, 0, 1, 0  ],
                                    [ 0, 0, 0, 1  ]])

vetorTransZ = lambda dz : np.array([[ 1, 0, 0, 0  ],
                                    [ 0, 1, 0, 0  ],
                                    [ 0, 0, 1, dz ],
                                    [ 0, 0, 0, 1  ]])

vetorTrans = lambda dx,dy,dz : np.array([[ 1, 0, 0, dx ],
                                         [ 0, 1, 0, dy ],
                                         [ 0, 0, 1, dz ],
                                         [ 0, 0, 0, 1  ]])


def matrizRot(teta, d, a, alfa):
    # A = Rz . Tz . Tx . Rx 
    Rz = vetorRotZ(np.radians(teta))
    Tz = vetorTransZ(d)
    Tx = vetorTransX(a)
    Rx = vetorRotX(np.radians(alfa))
    return Rz.dot(Tz).dot(Tx).dot(Rx)   



# USING VIRTUAL PYTHON TO PLOT THE XYZ AXIS 
def drawAxisXYZ():
    origin = vector(0,0,0)
    rateDim = 50
    radius = 0.3
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

    # Denavit-Harteberg parameters 
    teta = 0
    d    = 0 
    a    = 0 
    alfa = 0

    # Parameters to draw the axis in the cartesian plan 
    posi   = vector(0,0,0)
    posf   = vector(0,0,0)
    axis   = vector(0,0,0)
    
    length = 1
    radius = 1

    # To draw the link
    jointLink = cylinder()
    # To draw the end joint 
    jointAxis = sphere() 

    def __init__(self, pos=[0,0,0], ang = 0, length=1):
        
        self.posi = vetor(pos)
        self.ang = radians(ang)
        self.length = length

        x,y,z = cos(ang)*length, sin(ang)*length, 0
        self.posf = vector(self.posi.x + x, self.posi.y + y, self.posi.z + z )

        self.axis = vector(x,y,z)

        # To draw the link
        self.jointLink = cylinder(pos = self.posi, axis = self.axis, radius = self.radius, length = self.length, color = color.white )
        # To draw the end joint 
        self.jointAxis = sphere(pos = self.posf, axis = self.axis, radius = self.radius+0.5, color = color.red) 


    def endLink(self):
        return [self.posf.x, self.posf.y, 0]

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

    joint_origin = Joint([0,0,0], 0, 32)
    joint_one    = Joint(joint_origin.endLink(), 90, 16 )
    joint_two    = Joint(joint_one.endLink(), 0, 8)
    joint_three  = Joint(joint_two.endLink(), 90, 4)
    time.sleep(2)

    rate(60)
    while True:

        joint_origin.rotateLink(1)
        joint_one.moveLink(joint_origin.endLink())
        joint_one.rotateLink(2)        
        joint_two.moveLink(joint_one.endLink())
        joint_two.rotateLink(1)        
        joint_three.moveLink(joint_two.endLink())
        joint_three.rotateLink(2)

        
        time.sleep(1/120)
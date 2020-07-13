import numpy as np 
import math

vetorRotX = lambda teta : np.array([[ 1, 0             , 0             ],
                                    [ 0, math.cos(teta),-math.sin(teta)],
                                    [ 0, math.sin(teta), math.cos(teta)]])

vetorRotY = lambda teta : np.array([[ math.cos(teta), 0, math.sin(teta)],
                                    [ 0             , 1, 0             ],
                                    [-math.sin(teta), 0, math.cos(teta)]])

vetorRotZ = lambda teta : np.array([[ math.cos(teta),-math.sin(teta), 0],
                                    [ math.sin(teta), math.cos(teta), 0],
                                    [ 0             , 0             , 1] ])

ponto = np.array([ 2, 0, 0]) 

op = np.dot(ponto,vetorRotY(math.radians(90)))

print (op)

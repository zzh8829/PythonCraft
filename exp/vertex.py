

import time
import numpy as np


vertices = np.array([0,0,0, 1,0,0, 0,1,0, 1,1,0,
					0,0,1, 1,0,1, 0,1,1, 1,1,1],dtype = 'f')

indices = np.array([2,3,7,6, 4,5,1,0, 0,1,3,2,
					1,5,7,3, 5,4,6,7, 4,0,2,6],dtype = 'i')


for i in range(6):
	v1 = indices[i*4]*3
	v2 = indices[i*4+1]*3
	v3 = indices[i*4+2]*3
	v4 = indices[i*4+3]*3
	print(vertices[v1],vertices[v1+1],vertices[v1+2])
	print(vertices[v2],vertices[v2+1],vertices[v2+2])
	print(vertices[v3],vertices[v3+1],vertices[v3+2])
	print(vertices[v4],vertices[v4+1],vertices[v4+2])


0.0 1.0 0.0
1.0 1.0 0.0
1.0 1.0 1.0
0.0 1.0 1.0

0.0 0.0 1.0
1.0 0.0 1.0
1.0 0.0 0.0
0.0 0.0 0.0

0.0 0.0 0.0
1.0 0.0 0.0
1.0 1.0 0.0
0.0 1.0 0.0

1.0 0.0 0.0
1.0 0.0 1.0
1.0 1.0 1.0
1.0 1.0 0.0

1.0 0.0 1.0
0.0 0.0 1.0
0.0 1.0 1.0
1.0 1.0 1.0

0.0 0.0 1.0
0.0 0.0 0.0
0.0 1.0 0.0
0.0 1.0 1.0
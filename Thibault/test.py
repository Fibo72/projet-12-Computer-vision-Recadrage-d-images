import icp_demo
import pycpd as cpd
import time
import matplotlib.pyplot as plt
import numpy as np
import scipy as scp

img_fix = plt.imread('data\logocolore.png').mean(axis = 2) #logo de base
img_r = plt.imread('data\logorotate.png').mean(axis = 2) # logo tourné
img_tr = plt.imread('data\logorotatesmall.png').mean(axis = 2) #rotation + translation
img_trd = plt.imread('data\logorotatesmalldeforme.png').mean(axis = 2) # rotation + translation + dilatation

plt.imshow(img_r)
plt.figure()

x, y = img_fix.shape
X , Y = np.where(img_fix)


X = X.reshape((x, y))
Y = Y.reshape((x, y))

fix = np.empty((x, y, 3))
r = np.empty((x, y, 3))
tr = np.empty((x, y, 3))
trd = np.empty((x, y, 3))

fix[:,:,0] = X
r[:,:,0] = X
tr[:,:,0] = X
trd[:,:,0] = X

fix[:,:,1] = Y
r[:,:,1] = Y
tr[:,:,1] = Y
trd[:,:,1] = Y

fix[:,:,2] = img_fix
r[:,:,2] =  img_r
tr[:,:,2] = img_tr
trd[:,:,2] = img_trd

#print(r)

pt_fix = fix[fix[:, :, 2] == 0.750]
pt_r = r[r[:, :, 2] == 0.750]
pt_tr = tr[tr[:, :, 2] == 0.750]
pt_trd = trd[trd[:, :, 2] == 0.750]

# méthode 1 

#print(pt_fix.shape, pt_r.shape)

#crop_r = icp.recadre_icp(img_r, pt_fix, pt_r)

#marche pas parce qu'on a pas le même nombre de points

# méthode 2

reg = cpd.RigidRegistration(X =  pt_fix, Y = pt_r )
TY, (s, R, t) = reg.register()



YT = s * np.dot(r, R) + t

# YT = reg.transform_point_cloud(Y = r)


# indice = np.lexsort(keys = YT, axis = )




YT[:,:,0] -= YT[:,:,0].min() 
YT[:,:,1] -= YT[:,:,1].min() 

print(YT[:,:,1].max())

tab = np.empty((YT[:,:,0].max().astype(int) + 1, YT[:,:,1].max().astype(int)+1))


tab[YT[:, :, 0].astype(int), YT[:, :, 1].astype(int)] = YT[:, :, -1]

plt.imshow(tab)
plt.show()

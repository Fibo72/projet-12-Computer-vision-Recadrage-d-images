import pycpd as cpd
# import time
import matplotlib.pyplot as plt
import numpy as np
# import scipy as scp

# img_fix = plt.imread('data//logocolore.png').mean(axis = 2) #logo de base
# img_r = plt.imread('data//logorotate.png').mean(axis = 2) # logo tourné
# img_tr = plt.imread('data//logorotatesmall.png').mean(axis = 2) #rotation + translation
# img_trd = plt.imread('data//logorotatesmalldeforme.png').mean(axis = 2) # rotation + translation + dilatation


# plt.figure()


# x, y = img_fix.shape
# X , Y = np.where(img_fix)
# X1, Y1 = np.meshgrid(x,y)
# print(X1, Y1)

# print(X.shape, Y.shape)

# X = X.reshape((x, y))
# Y = Y.reshape((x, y))

# fix = np.empty((x, y, 3))
# r = np.empty((x, y, 3))
# tr = np.empty((x, y, 3))
# trd = np.empty((x, y, 3))

# fix[:,:,0] = X
# r[:,:,0] = X
# tr[:,:,0] = X
# trd[:,:,0] = X

# fix[:,:,1] = Y
# r[:,:,1] = Y
# tr[:,:,1] = Y
# trd[:,:,1] = Y

# fix[:,:,2] = img_fix
# r[:,:,2] =  img_r
# tr[:,:,2] = img_tr
# trd[:,:,2] = img_trd


# pt_fix = fix[fix[:, :, 2] == 0.750]
# pt_r = r[r[:, :, 2] == 0.750]
# pt_tr = tr[tr[:, :, 2] == 0.750]
# pt_trd = trd[trd[:, :, 2] == 0.750]

def format_img(img : np.ndarray) -> np.ndarray:
    """
    Format an image to be used by the CPD algorithm.
    """
    x, y = img.shape
    X , Y = np.where(img)

    X = X.reshape((x, y))
    Y = Y.reshape((x, y))

    fix = np.empty((x, y, 3))
    fix[:,:,0] = X
    fix[:,:,1] = Y
    fix[:,:,2] = img

    return fix

def recadrage_cpd(pt_fix, pt_target):

    reg = cpd.RigidRegistration(X =  pt_fix, Y = pt_target )
    TY, (s, R, t) = reg.register()


    return s, R, t

def apply_recadr(img, s,R,t):
    YT = s * np.dot(img, R) + t   

    YT[:,:,0] -= YT[:,:,0].min() 
    YT[:,:,1] -= YT[:,:,1].min() 



    tab = np.empty((YT[:,:,0].max().astype(int) + 1, YT[:,:,1].max().astype(int)+1))


    tab[YT[:, :, 0].astype(int), YT[:, :, 1].astype(int)] = YT[:, :, -1]

    return tab



# tab = recadrage_cpd(img_fix, img_r, pt_fix, pt_r)
# tab2 = recadrage_cpd(img_fix, img_tr, pt_fix, pt_tr)
# tab3 = recadrage_cpd(img_fix, img_trd, pt_fix, pt_trd)
# plt.subplot(221)
# plt.imshow(tab)
# plt.subplot(222)
# plt.imshow(tab2)
# plt.subplot(223)
# plt.imshow(tab3)
# plt.show()

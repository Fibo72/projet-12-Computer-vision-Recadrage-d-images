import numpy as np
import pycpd as cpd

def recadrage_cpd(img_fix, img_target, pt_fix, pt_target):

    x, y = img_fix.shape
    X , Y = np.where(img_fix)

    X = X.reshape((x, y))
    Y = Y.reshape((x, y))

    fix = np.empty((x, y, 3))
    r = np.empty((x, y, 3))
    fix[:,:,0] = X
    r[:,:,0] = X
    fix[:,:,1] = Y
    r[:,:,1] = Y
    fix[:,:,2] = img_fix
    r[:,:,2] =  img_target

    reg = cpd.RigidRegistration(X =  pt_fix, Y = pt_target )
    TY, (s, R, t) = reg.register()

    #compute the transformed image
    YT = s * np.dot(r, R) + t   

    YT[:,:,0] -= YT[:,:,0].min() 
    YT[:,:,1] -= YT[:,:,1].min() 



    tab = np.empty((YT[:,:,0].max().astype(int) + 1, YT[:,:,1].max().astype(int)+1))


    tab[YT[:, :, 0].astype(int), YT[:, :, 1].astype(int)] = YT[:, :, -1]

    return tab
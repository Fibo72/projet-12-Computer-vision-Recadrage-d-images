import pycpd as cpd
import matplotlib.pyplot as plt
import numpy as np
from functools import partial


def format_img(img : np.ndarray) -> np.ndarray:
    """
    Format an image to be used by the CPD algorithm.
    """
    x, y = img.shape
    X , Y = np.indices(img.shape).reshape(2, -1)
    
    X = np.array(X)
    Y = np.array(Y)

    X = X.reshape((x, y))
    Y = Y.reshape((x, y))

    fix = np.empty((x, y, 3))
    fix[:,:,0] = X
    fix[:,:,1] = Y
    fix[:,:,2] = img

    return fix

def recadrage_cpd(pt_fix, pt_target):

    reg = cpd.RigidRegistration(**{'X': pt_fix, 'Y': pt_target, 'max_iterations': 100, 'tolerance': 1e-5})
    reg.register()


    s, R, t = reg.get_registration_parameters()
    

    return s, R, t

def apply_recadr(img, s,R,t):
    YT = s * np.dot(img, R) + t   

    YT[:,:,0] -= YT[:,:,0].min() 
    YT[:,:,1] -= YT[:,:,1].min() 
    YT[:,:,2] -= YT[:,:,2].min()


    tab = np.empty((YT[:,:,0].max().astype(int) + 1, YT[:,:,1].max().astype(int)+1))
    tab[YT[:, :, 0].astype(int), YT[:, :, 1].astype(int)] = YT[:, :, -1]
    return tab


# def thibault(img_fix, img_target, pt_fix, pt_target):

#     x, y = img_fix.shape
#     X , Y = np.where(img_fix)

#     X = X.reshape((x, y))
#     Y = Y.reshape((x, y))

#     fix = np.empty((x, y, 3))
#     r = np.empty((x, y, 3))
#     fix[:,:,0] = X
#     r[:,:,0] = X
#     fix[:,:,1] = Y
#     r[:,:,1] = Y
#     fix[:,:,2] = img_fix
#     r[:,:,2] =  img_target

#     reg = cpd.RigidRegistration(X =  pt_fix, Y = pt_target )
#     TY, (s, R, t) = reg.register()

#     YT = s * np.dot(r, R) + t   

#     YT[:,:,0] -= YT[:,:,0].min() 
#     YT[:,:,1] -= YT[:,:,1].min() 



#     tab = np.empty((YT[:,:,0].max().astype(int) + 1, YT[:,:,1].max().astype(int)+1))


#     tab[YT[:, :, 0].astype(int), YT[:, :, 1].astype(int)] = YT[:, :, -1]

#     return tab

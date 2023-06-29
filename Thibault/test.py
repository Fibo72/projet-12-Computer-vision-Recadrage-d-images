import pycpd as cpd
import matplotlib.pyplot as plt
import numpy as np

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
    
    reg = cpd.RigidRegistration(pt_fix, pt_target)
    s, R, t = reg.get_registration_parameters()
    

    return s, R, t

def apply_recadr(img, s,R,t):
    YT = s * np.dot(img, R) + t   

    YT[:,:,0] -= YT[:,:,0].min() 
    YT[:,:,1] -= YT[:,:,1].min() 


    tab = np.empty((YT[:,:,0].max().astype(int) + 1, YT[:,:,1].max().astype(int)+1))


    tab[YT[:, :, 0].astype(int), YT[:, :, 1].astype(int)] = YT[:, :, -1]

    return tab

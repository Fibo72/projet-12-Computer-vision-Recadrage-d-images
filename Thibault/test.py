import pycpd as cpd
import matplotlib.pyplot as plt
import numpy as np
from functools import partial


def format_img(img : np.ndarray) -> np.ndarray:
    """Format the image to be used by the cpd library

    Args:
        img (np.ndarray): image to format (n,m)

    Returns:
        np.ndarray: image formatted (n,m, 3) with element like : (x, y, z)
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

def recadrage_cpd(pt_fix : np.ndarray, pt_target : np.ndarray) -> tuple:
    """Trouve la transformation rigide entre pt_fix et pt_target

    Args:
        pt_fix (np.ndarray): liste de point (x, y) ou (x, y, z) de l'image fixe
        pt_target (np.ndarray): liste de point (x, y) ou (x, y, z) de l'image à recadrer

    Returns:
        tuple: s, R, t : s = scale (float), R = rotation (2,2) ou (3,3) selon la dimension des points , t = translation (2,) ou (3,) selon la dimension des points
    """

    reg = cpd.RigidRegistration(**{'X': pt_fix, 'Y': pt_target, 'max_iterations': 100, 'tolerance': 1e-5})
    reg.register()


    s, R, t = reg.get_registration_parameters()
    

    return s, R, t

def apply_recadr(img : np.ndarray, s : float, R : np.ndarray, t: np.ndarray) -> tuple:


    """effectue le recadrage de l'image par la transformation rigide fournie

    Args:
        img (np.ndarray): image formatée à recadrer (n, m, 3)
        s (float): scale
        R (np.ndarray): rotation (2,2) ou (3,3) selon la dimension de l'image
        t (np.ndarray): translation (2,) ou (3,) selon la dimension de l'image

    Returns:
        tuple: tab : image recadrée (n, m), min_x, min_y, min_z : coordonnées du point en bas à gauche de l'image recadrée (poru eviter les valeurs négatives)
    """
    YT = s * np.dot(img, R) + t   
    min_x = YT[:,:,0].min() 
    min_y = YT[:,:,1].min()
    min_z = YT[:,:,2].min()
    YT[:,:,0] -= min_x
    YT[:,:,1] -= min_y
    YT[:,:,2] -= min_z


    tab = np.empty((YT[:,:,0].max().astype(int) + 1, YT[:,:,1].max().astype(int)+1))
    tab[YT[:, :, 0].astype(int), YT[:, :, 1].astype(int)] = YT[:, :, -1]
    return tab, min_x, min_y, min_z

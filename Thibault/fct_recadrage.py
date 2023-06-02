import numpy as np
import matplotlib.pyplot as plt
import pycpd as cpd

def recadrage_cpd(source, target, pt_source, pt_target ):
    """recadre une image par pcd
    besoin de récupérer les points Lsourcees sous la forme nx3 """

    #mise en forme des données

    x, y = source.shape
    X , Y = np.where(source)
    X = X.reshape((x, y))
    Y = Y.reshape((x, y))

    Lsource = np.empty((x, y, 3))
    Ltarget = np.empty((x, y, 3))

    Lsource[:,:,0] = X
    Lsource[:,:,1] = Y
    Ltarget[:,:,0] = X
    Ltarget[:,:,1] = Y
    Lsource[:,:,2] = source
    Ltarget[:,:,2] =  target

    # Calcul par cpd

    reg = cpd.RigidRegistration(X =  pt_source, Y = pt_target )
    TY, (s, R, t) = reg.register()

    YT = s * np.dot(target, R) + t

    # application à l'image

    YT[:,:,0] -= YT[:,:,0].min() 
    YT[:,:,1] -= YT[:,:,1].min() 

    tab = np.empty((YT[:,:,0].max().astype(int) + 1, YT[:,:,1].max().astype(int)+1))

    tab[YT[:, :, 0].astype(int), YT[:, :, 1].astype(int)] = YT[:, :, -1]

    return tab


if __name__ == "__main__" :


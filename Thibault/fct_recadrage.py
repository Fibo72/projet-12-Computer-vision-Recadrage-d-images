import numpy as np
import matplotlib.pyplot as plt
import pycpd as cpd

def recadrage_cpd(target, pt_source, pt_target):
    """recadre une image par pcd
    besoin de récupérer les points sourcees sous la forme nx3 """

    #mise en forme des données

    x, y = target.shape
    X , Y = np.meshgrid(np.arange(x), np.arange(y)) 

    X = X.reshape((x, y))
    Y = Y.reshape((x, y))

    Ltarget = np.empty((x, y, 3))

    Ltarget[:,:,0] = X
    Ltarget[:,:,1] = Y
    Ltarget[:,:,2] =  target

    # Calcul par cpd

    reg = cpd.RigidRegistration(X =  pt_source, Y = pt_target )
    TY, (s, R, t) = reg.register()

    YT = s * np.dot(Ltarget, R) + t

    # application à l'image

    YT[:,:,0] -= YT[:,:,0].min() 
    YT[:,:,1] -= YT[:,:,1].min() 

    tab = np.empty((YT[:,:,0].max().astype(int) + 1, YT[:,:,1].max().astype(int)+1))

    tab[YT[:, :, 0].astype(int), YT[:, :, 1].astype(int)] = YT[:, :, -1]

    return tab

if __name__ == "__main__":
    #test
    target = np.zeros((100, 100))
    target += 0.1
    target[20:50, 20:70] = 1

    print("target")
    plt.imshow(target)
    plt.show()

    pt_source = np.array([[20, 20, 0.1], [20, 70, 0.1], [50, 20, 0.1], [50, 70, 0.1]])
    pt_target = np.array([[20, 20, 0.1], [20, 70, 0.1], [50, 20, 0.1], [50, 70, 0.1]])

    print("recadré?")
    plt.imshow(recadrage_cpd(target, pt_source, pt_target))
    plt.show()
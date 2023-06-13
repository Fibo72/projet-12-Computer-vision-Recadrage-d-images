import numpy as np
import matplotlib.pyplot as plt
import pycpd as cpd

def recadrage_cpd(target, pt_source, pt_target):
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
    Ltarget[:,:,2] = target

    # Calcul par cpd

    reg = cpd.RigidRegistration(X =  pt_source, Y = pt_target )
    TY, (s, R, t) = reg.register()

    YT = s * apply_rotation( Ltarget,R)  + t

    # application à l'image

    YT[:,:,0] -= YT[:,:,0].min() 
    YT[:,:,1] -= YT[:,:,1].min() 

    tab = np.empty((YT[:,:,0].max().astype(int) + 1, YT[:,:,1].max().astype(int)+1))

    tab[YT[:, :, 0].astype(int), YT[:, :, 1].astype(int)] = YT[:, :, -1]

    return tab


if __name__ == "__main__" :

    img_fix = plt.imread('Thibault\data\logocolore.jpg').mean(axis = 2) #logo de base
    img_r = plt.imread('Thibault\data\logorotate.jpg').mean(axis = 2) # logo tourné
    # img_tr = plt.imread('data//logorotatesmall.png').mean(axis = 2) #rotation + translation
    # img_trd = plt.imread('data//logorotatesmalldeforme.png').mean(axis = 2) # rotation + translation + dilatation

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
    # tr[:,:,2] = img_tr
    # trd[:,:,2] = img_trd



    pt_fix = fix[fix[:, :, 2] == 0.750]
    pt_r = r[r[:, :, 2] == 0.750]
    pt_tr = tr[tr[:, :, 2] == 0.750]
    pt_trd = trd[trd[:, :, 2] == 0.750]

    Rr = recadrage_cpd( img_r, pt_fix, pt_r)
    Rtr = recadrage_cpd( img_tr, pt_fix, pt_tr)
    Rtrd = recadrage_cpd(img_trd, pt_fix, pt_trd)

    plt.figure()

    plt.subplot(221)
    plt.imshow(img_fix)
    plt.subplot(222)
    plt.imshow(Rr)
    plt.subplot(223)
    plt.imshow(Rtr)
    plt.subplot(224)
    plt.imshow(Rtrd)
    plt.show()






    print(Rr)
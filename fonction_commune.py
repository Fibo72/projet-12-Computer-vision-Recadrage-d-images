import json
import cv2
import os
import numpy as np

def recadrage(path_dict: str)-> list:
    """Crop images

    Args:
        img_dict (.json): Have to follow this format :
            {
            img: (dict) ->
                {
                    nb_img: (int) -> Number of img
                    img_folder: (list of string) -> folder of the img k
                    img_name: (list of string) -> name of the img k
                    p1: (list of int) -> #1st point of the img k
                    p2: (list of int) -> ...
                    p3: (list of int) -> ...
                    p4: (list of int) -> ...
                }

            crop_number: (int) -> Number of the image on which all the other will be cropped

            out_path: (string) -> Path where new images will be savec
            
            comment: (String) -> A comment linked to this special cropp
        }
    return:
        list -> list of the cropped images
    """

    
    load_dict = json.load(open(path_dict))

    img_dict = load_dict["img_dict"]
    nb_img = img_dict["nb_img"]
    img_folder = img_dict["img_folder"]
    img_name = img_dict["img_name"]
    p1 = img_dict["p1"]
    p2 = img_dict["p2"]
    p3 = img_dict["p3"]
    p4 = img_dict["p4"]

    crop_number = load_dict["crop_number"]
    out_path = load_dict["out_path"]

    if ((len(img_folder) != nb_img) | (len(img_name) != nb_img) | (len(p1) != nb_img) | (len(p2) != nb_img) | (len(p3) != nb_img) | (len(p4) != nb_img)):
        raise ValueError
    

    if (os.path.isdir(out_path)):
        raise FileNotFoundError
    

    rslt = []
    final_pt = [p1[crop_number], p2[crop_number], p3[crop_number], p4[crop_number]]


    for k in range(nb_img):
        if (k!= crop_number):
            actual_pt = [p1[k], p2[k], p3[k], p4[k]]
            M = cv2.getPerspectiveTransform(actual_pt,final_pt)
            with cv2.imread(img_folder[k] + img_name[k]) as im:
                im_tr = cv2.warpPerspective(im, M, im.shape)
                rslt.append(im_tr)
    return rslt




def generate_json(path_dict: str, img_folder: list, img_name: list, p1: list, p2: list, p3: list, p4: list, crop_number: int, out_path: str, comment: str)->None:
    """Generate a json file to crop images

    Args:
        path_dict (str): Path of the folder
        img_folder (list): List of the folder of the images
        img_name (list): List of the name of the images
        p1 (list): List of the #1st point of the images
        p2 (list): List of the #2nd point of the images
        p3 (list): List of the #3rd point of the images
        p4 (list): List of the #4th point of the images
        crop_number (int): Number of the image on which all the other will be cropped
        out_path (str): Path where new images will be savec
        comment (str): A comment linked to this special cropp
    """
    if (len(img_folder) != len(img_name) != len(p1) != len(p2) != len(p3) != len(p4)):
        raise ValueError

    img_dict = {
        "nb_img": len(img_folder),
        "img_folder": img_folder,
        "img_name": img_name,
        "p1": p1,
        "p2": p2,
        "p3": p3,
        "p4": p4
    }

    load_dict = {
        "img_dict": img_dict,
        "crop_number": crop_number,
        "out_path": out_path,
        "comment": comment
    }

    with open(path_dict, "w") as f:
        json.dump(load_dict, f, indent=4)



def prof_topo(A,B, img):
    """Return the profile of the topography

    Args:
        A (list): #1st point of the profile
        B (list): #2nd point of the profile
        img (np.array): Image of the topography

    Returns:
        list: Profile of the topography
    """
    x1, y1 = A
    x2, y2 = B

    def f(x):
        return (y2-y1)/(x2-x1)*(x-x1)+y1


    X = np.round(np.arange(x1, x2+1)).astype(int)
    Y = np.round(f(X)).astype(int)
    
    prof = img[Y,X]

    return X, Y, prof


if  __name__ == "__main__":
    import matplotlib.pyplot as plt
    path_dict = 'test/1_14__18_7.png'
    
    load_pic = plt.imread(path_dict)

    data = prof_topo((1,14),(18,7), load_pic)
    print(data[2])
    plt.figure()
    plt.plot(data[2])
    plt.show()

    plt.figure()
    plt.imshow(load_pic)
    plt.plot(data[0], data[1],'bx')
    plt.show()

    np.meshgrid(data[0], data[1])
    img = np.zeros((20, 20,4))
    i = 0
    for y,k in zip(data[0], data[1]):
        img[k,y] = data[2][i,:]
        i+=1
    plt.figure()
    plt.imshow(img)
    plt.show()
import json
import cv2
import os
import numpy as np

# def recadrage(path_dict: str)-> list:
#     """Crop images

#     Args:
#         img_dict (.json): Have to follow this format :
#             {
#             img: (dict) ->
#                 {
#                     nb_img: (int) -> Number of img
#                     img_folder: (list of string) -> folder of the img k
#                     img_name: (list of string) -> name of the img k
#                     p1: (list of int) -> #1st point of the img k
#                     p2: (list of int) -> ...
#                     p3: (list of int) -> ...
#                     p4: (list of int) -> ...
#                 }

#             crop_number: (int) -> Number of the image on which all the other will be cropped

#             out_path: (string) -> Path where new images will be savec
            
#             comment: (String) -> A comment linked to this special cropp
#         }
#     return:
#         list -> list of the cropped images
#     """

    
#     load_dict = json.load(open(path_dict))

#     img_dict = load_dict["img_dict"]
#     nb_img = img_dict["nb_img"]
#     img_folder = img_dict["img_folder"]
#     img_name = img_dict["img_name"]
#     p1 = img_dict["p1"]
#     p2 = img_dict["p2"]
#     p3 = img_dict["p3"]
#     p4 = img_dict["p4"]

#     crop_number = load_dict["crop_number"]
#     out_path = load_dict["out_path"]

#     if ((len(img_folder) != nb_img) | (len(img_name) != nb_img) | (len(p1) != nb_img) | (len(p2) != nb_img) | (len(p3) != nb_img) | (len(p4) != nb_img)):
#         raise ValueError
    

#     if (os.path.isdir(out_path)):
#         raise FileNotFoundError
    

#     rslt = []
#     final_pt = [p1[crop_number], p2[crop_number], p3[crop_number], p4[crop_number]]


#     for k in range(nb_img):
#         if (k!= crop_number):
#             actual_pt = [p1[k], p2[k], p3[k], p4[k]]
#             M = cv2.getPerspectiveTransform(actual_pt, final_pt)
#             with cv2.imread(img_folder[k] + img_name[k]) as im:
#                 im_tr = cv2.warpPerspective(im, M, im.shape)
#                 rslt.append(im_tr)
#     return rslt



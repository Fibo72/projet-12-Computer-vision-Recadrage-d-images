import struct
import numpy as np
import matplotlib.pyplot as plt
import json 


def header_reader(path: str) -> dict:
    """Take a .dat file from MetroPro and return the heder decoded

    Args:
        data (string): path to .dat file

    Returns:
        dict: Decoded header with MetroPro documentation + data, the keys are : 
        magic_number, header_format, header_size, ac_org_x, ac_org_y, ac_width, ac_height, ac_n_bucket, ac_range, ac_n_bytes, itensity_raw,
        cn_org_x, cn_org_y, cn_width, cn_height, cn_n_bytes, intf_scale_factor, wavelength_in, obliquity_factor,phase_res, phase_raw
    """

    with open(path,'rb') as my_file:
        data = my_file.read()
    
    header = {}

    header['magic_number'] = int.from_bytes(data[:4], "big")
    header['header_format'] = int.from_bytes(data[4:6], "big")
    header['header_size'] = int.from_bytes(data[6:10], "big")

    header['ac_org_x'] = int.from_bytes(data[48:50], "big")
    header['ac_org_y'] = int.from_bytes(data[50:52], "big")
    header['ac_width'] = int.from_bytes(data[52:54], "big")
    header['ac_height'] = int.from_bytes(data[54:56], "big")
    header['ac_n_bucket'] = int.from_bytes(data[56:58], "big")
    header['ac_range'] = int.from_bytes(data[58:60], "big")
    header['ac_n_bytes'] = int.from_bytes(data[60:64], "big")
    header['itensity_raw'] = data[header['header_size']: header['header_size'] + header['ac_n_bytes']]

    header['cn_org_x'] = int.from_bytes(data[64:66], "big")
    header['cn_org_y'] = int.from_bytes(data[66:68], "big")
    header['cn_width'] = int.from_bytes(data[68:70], "big")
    header['cn_height'] = int.from_bytes(data[70:72], "big")
    header['cn_n_bytes'] = int.from_bytes(data[72:76], "big")
    header['intf_scale_factor'] = struct.unpack('f',data[167:163:-1])[0]
    print(data[168:172])
    header['wavelength_in'] = struct.unpack('f',data[171:167:-1])[0]
    header['obliquity_factor'] = struct.unpack('f',data[179:175:-1])[0]
    header['phase_res'] = int.from_bytes(data[218:220], "big")
    
    header['phase_raw'] = data[header['header_size'] + header['ac_n_bytes']: header['header_size'] +header['ac_n_bytes'] + header['cn_n_bytes']]

    return header



def decod_phase_img(header: dict) ->np.ndarray:
    """Take the header of data and return a picture in meter

    Args:
        header (dict): Header of the data

    Returns:
        np.array: picture
    """
    img = []


    for i in range(0,header['cn_n_bytes'],4):
        val = int.from_bytes(header['phase_raw'][i:i+4], "big", signed = True)
        if (abs(val) < 0x7FFFFFF8):
            img.append(val)
        else :
            img.append(0)
    img = np.array(img)
    img_threshold = (img-np.min(img))
    pic = np.reshape(img_threshold*255/np.max(img_threshold), (header['cn_height'],header['cn_width'])).astype(np.uint8)
    return pic


def encode(header: dict, itensity_img: np.ndarray, phase_img : np.ndarray, path: str, name: str):
    """Encode the header and the picture in a .dat file"""

    intensity_img = np.reshape(itensity_img, (header['ac_height']*header['ac_width']))
    phase_img = np.reshape(phase_img, (header['cn_height']*header['cn_width']))


    file = open(f"{path + name}.dat", 'wb')
    file.write(header['magic_number'].to_bytes(4, "big"))
    file.write(header['header_format'].to_bytes(2, "big"))
    file.write(header['header_size'].to_bytes(4, "big"))
    file.write(header['ac_org_x'].to_bytes(2, "big"))
    file.write(header['ac_org_y'].to_bytes(2, "big"))
    file.write(header['ac_width'].to_bytes(2, "big"))
    file.write(header['ac_height'].to_bytes(2, "big"))
    file.write(header['ac_n_bucket'].to_bytes(2, "big"))
    file.write(header['ac_range'].to_bytes(2, "big"))
    file.write(header['ac_n_bytes'].to_bytes(4, "big"))
    
    for i in range(header['ac_n_bytes']):
        file.write(itensity_img[i].to_bytes(1, "big"))
    
    file.write(header['cn_org_x'].to_bytes(2, "big"))
    file.write(header['cn_org_y'].to_bytes(2, "big"))
    file.write(header['cn_width'].to_bytes(2, "big"))
    file.write(header['cn_height'].to_bytes(2, "big"))
    file.write(header['cn_n_bytes'].to_bytes(4, "big"))
    file.write(header['intf_scale_factor'].to_bytes(4, "big"))
    file.write(header['wavelength_in'].to_bytes(4, "big"))
    file.write(header['obliquity_factor'].to_bytes(4, "big"))
    file.write(header['phase_res'].to_bytes(2, "big"))
    
    for i in range(header['cn_n_bytes']):
        file.write(phase_img[i].to_bytes(1, "big"))

    file.close()





def convert(header, phase_img, type):
    """Convert the phase image in meter or waves"""
    R = {
        '1': {
            '0': 4096,
            '1': 32768
        },
        '2' :{
            '0':4096,
            '1':32768,
            '2':131072,
        },
        '3' :{
            '0':4096,
            '1':32768,
            '2':131072,
        }
    }
    if (type == 'waves'):
        return phase_img * header['intf_scale_factor']* header['obliquity_factor'] / R[str(header['header_format'])][str(header['phase_res'])]
    elif (type == 'meter'):
        print(header['wavelength_in'])
        return phase_img * header['intf_scale_factor']* header['obliquity_factor'] * header['wavelength_in'] / (R[str(header['header_format'])])[str(header['phase_res'])]


def get_phase_img(path: str) -> np.ndarray:
    """Take a path to a .dat file and return the picture in meter

    Args:
        path (str): path to .dat file

    Returns:
        np.array: picture
    """
    return decod_phase_img(header_reader(path))




def generate_json(path_dict: str, img_folder: list, img_name: list, p1: list, p2: list, p3: list, p4: list, crop_number: int, out_path: str, comment: str)->None:
    """Generate a json file to crop images

    Args:
        path_dict (str): Path of the folder
        img_folder (list): List of the folder of images
        img_name (list): List of the name of images
        p1 (list): List of the #1st point of images
        p2 (list): List of the #2nd point of images
        p3 (list): List of the #3rd point of images
        p4 (list): List of the #4th point of images
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
    a = None


if (__name__ == '__main__'):
    path = 'C:/Users/Aymeric/Desktop/Stage/Prog'


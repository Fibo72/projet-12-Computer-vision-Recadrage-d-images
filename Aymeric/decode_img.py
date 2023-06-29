import struct
import numpy as np
import matplotlib.pyplot as plt
import json 
from Thibault.test import recadrage_cpd, format_img, apply_recadr

#Lecture image
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
    header['intensity_raw'] = data[header['header_size']: header['header_size'] + header['ac_n_bytes']]

    header['cn_org_x'] = int.from_bytes(data[64:66], "big")
    header['cn_org_y'] = int.from_bytes(data[66:68], "big")
    header['cn_width'] = int.from_bytes(data[68:70], "big")
    header['cn_height'] = int.from_bytes(data[70:72], "big")
    header['cn_n_bytes'] = int.from_bytes(data[72:76], "big")
    header['intf_scale_factor'] = struct.unpack('f',data[167:163:-1])[0]
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

def decod_intensity_img(header: dict) ->np.ndarray:
    """Take the header of data and return a picture in meter

    Args:
        header (dict): Header of the data

    Returns:
        np.array: picture
    """
    img = []


    for i in range(0, header['ac_n_bytes'], 2):

        val = int.from_bytes(header['intensity_raw'][i:i+2], "big", signed = True)

        if (abs(val) < header['ac_range']):
            img.append(val)
        else :
            img.append(0xFFFF)

    img = np.array(img)
    img_threshold = (img-np.min(img))
    pic = np.reshape(img_threshold*255/np.max(img_threshold), (header['ac_height'],header['ac_width'], header['ac_n_bucket'])).astype(np.uint8)
    return pic

def encode(header: dict, intensity_img: np.ndarray, org_intensity : np.ndarray, phase_img : np.ndarray, org_phase : np.ndarray, path: str, name: str):
    """Encode the header and the picture in a .dat file"""

    ac_height, ac_width = intensity_img.shape[:2]
    cn_height, cn_width = phase_img.shape
    intensity_img = np.reshape(intensity_img, ac_height*ac_width)
    phase_img = np.reshape(phase_img, cn_height*cn_width)


    file = open(f"{path + name}.dat", 'wb')
    file.write(header['magic_number'].to_bytes(4, "big"))
    file.write(header['header_format'].to_bytes(2, "big"))
    file.write(header['header_size'].to_bytes(4, "big"))

    
    file.write((org_intensity[0]).to_bytes(2, "big"))
    file.write((org_intensity[1]).to_bytes(2, "big"))
    file.write(ac_width.to_bytes(2, "big"))
    file.write(ac_height.to_bytes(2, "big"))
    file.write(header['ac_n_bucket'].to_bytes(2, "big"))
    file.write(np.max(intensity_img).to_bytes(2, "big"))
    file.write((ac_height*ac_width*header['ac_n_bucket']*2).to_bytes(4, "big"))
    
    for i in range((ac_height*ac_width*header['ac_n_bucket']*2)):
        file.write(intensity_img[i].to_bytes(1, "big"))
    
    file.write((org_phase[0]).to_bytes(2, "big"))
    file.write((org_phase[0]).to_bytes(2, "big"))
    file.write(cn_width.to_bytes(2, "big"))
    file.write(cn_height.to_bytes(2, "big"))
    file.write((cn_height*cn_width*8).to_bytes(4, "big"))
    file.write(header['intf_scale_factor'].to_bytes(4, "big"))
    file.write(header['wavelength_in'].to_bytes(4, "big"))
    file.write(header['obliquity_factor'].to_bytes(4, "big"))
    file.write(header['phase_res'].to_bytes(2, "big"))
    
    for i in range(header['cn_n_bytes']):
        file.write(phase_img[i].to_bytes(1, "big"))

    file.close()


def convert(header, phase_img, type) -> np.ndarray:
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
        return phase_img * header['intf_scale_factor']* header['obliquity_factor'] * header['wavelength_in'] / (R[str(header['header_format'])])[str(header['phase_res'])]
    else:
        raise Exception('Type must be waves or meter')

def get_img(path: str, type : str) -> np.ndarray:
    """Take a path to a .dat file and return the picture in meter

    Args:
        path (str): path to .dat file
        type (str): type of the img

    Returns:
        np.array: picture
        if type == 'intensity' : img.shape = (header['ac_height'],header['ac_width'], header['ac_n_bucket'])
        if type == 'phase' : img.shape = (header['cn_height'],header['cn_width'])
    """
    if type == 'intensity':
        return decod_intensity_img(header_reader(path))
    elif type == 'phase':
        return decod_phase_img(header_reader(path))
    else :
        raise Exception("Type not found")

def get_org_img(header : dict, type : str) -> np.ndarray:
    '''Return the org of a img
    Args:
        header (dict): header of the img
        type (str): type of the img
        Returns:
            np.ndarray: org of the img 
                if type == 'intensity' : org = np.array(x,y,z) for each bucket the org.shape = (3, header['ac_n_bucket'])
                if type == 'phase' : org = np.array(x,y,z) the org.shape = (3,1)'''

    x,y,z = 0,0,0

    if type == 'intensity':
        org = np.empty((3, header['ac_n_bucket']))
        x,y = header['ac_org_x'], header['ac_org_y']
        img = decod_intensity_img(header)

        
        for i in range(header['ac_n_bucket']):
            z = img[x, y, i]
            org[:,i] = [x,y,z]
        return org
    
    elif type == 'phase':
        x,y = header['cn_org_x'], header['cn_org_y']
        img = decod_phase_img(header)
        z = img[x,y]
        return np.array([[x],[y],[z]])
    
    raise Exception("Type not found")

def generate_json(path_dict: str,  img_name: list, p1: np.ndarray, crop_number: int, out_path: str , comment: str)->None:
    """Generate a json file to crop images

    Args:
        path_dict (str): Path of the folder
        img_name (list): List of the name of images
        p1 (np.ndarray): (n,m,2) array of points
        crop_number (int): Number of the image on which all the other will be cropped
        out_path (str): Path where new images will be savec
        comment (str): A comment linked to this special cropp
    """

    img_dict = {
        "img_name": img_name,
        "p1": p1,
    }

    load_dict = {
        "img_dict": img_dict,
        "crop_number": crop_number,
        "out_path": out_path,
        "origin_path": path_dict,
        "comment": comment
    }

    with open(path_dict, "w") as f:
        json.dump(load_dict, f, indent=4)

#truc random
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



def recadrage(path_dict : str):

    with open(path_dict, "r") as f:
        load_dict = json.load(f)
    
    img_dict = load_dict["img_dict"]
    crop_number = load_dict["crop_number"]
    out_path = load_dict["out_path"]
    origin_path = load_dict["origin_path"]
    comment = load_dict["comment"]

    img_name = img_dict["img_name"]
    p1 = img_dict["p1"]

    header_0 = header_reader(origin_path + '/' + img_name[crop_number])

    img_phase_org = get_img(origin_path +  '/' + img_name[crop_number], 'phase')
    img_intensity_org = get_img(origin_path +  '/' + img_name[crop_number], 'intensity')

    img_phase_format_0 = format_img(img_phase_org)
    #TODO faire avec les intensité (/!\ multi dimension PAS PRISE EN CHARGE PAR THIBAULT DONC FAIRE DOUBLE FOR)
    x0 = p1[crop_number]
    #TODO faire les origines 



    for i in range(len(img_name)):
        if i != crop_number:

            header_i = header_reader(origin_path +  '/' + img_name[i])

            img_phase_i = get_img(origin_path +  '/' + img_name[i], 'phase')
            img_phase_format_i = format_img(img_phase_i)

            x_i  = p1[i]
            s, R, t = recadrage_cpd(x_i, x0)

            img_phase_recadr_i = apply_recadr(img_phase_format_i, s, R, t)
            img_intensity_recadr_i = apply_recadr(img_intensity_org, s, R, t)
            
            encode(header = header_i, 
                   intensity_img = img_intensity_recadr_i, org_intensity = np.array([0,0]), 
                   phase_img = img_phase_recadr_i, org_phase = np.array([0,0]),
                   path = out_path, name = img_name[i])
        else :
            encode(header_0, 
                   img_intensity_org, np.array([0,0]), 
                   img_phase_org,  np.array([0,0]),
                   out_path, img_name[crop_number])





if (__name__ == '__main__'):
    for i in range(1, 8):
        header = header_reader(f'data//CALSPAR16C_init-to-d7//CALSPAR16C_d{i}_image1-5x.dat')
        print(i, header['ac_n_bucket'])
        tab = get_img(f'data//CALSPAR16C_init-to-d7//CALSPAR16C_d{i}_image1-5x.dat', 'intensity')
        org = get_org_img(header_reader(f'data//CALSPAR16C_init-to-d7//CALSPAR16C_d{i}_image1-5x.dat'), 'intensity')

        plt.figure()
        plt.imshow(tab, cmap = 'gray')
        plt.plot(org[0, 0], org[1, 0], 'ro')
        plt.show()

        tab = get_img(f'data//CALSPAR16C_init-to-d7//CALSPAR16C_d{i}_image1-5x.dat', 'phase')
        org = get_org_img(header_reader(f'data//CALSPAR16C_init-to-d7//CALSPAR16C_d{i}_image1-5x.dat'), 'phase')

        plt.figure()
        plt.imshow(tab, cmap = 'gray')
        plt.plot(org[0, 0], org[1, 0], 'ro')
        plt.show()
        
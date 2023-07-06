from Thibault.test import recadrage_cpd, format_img, apply_recadr
import struct
import numpy as np
import matplotlib.pyplot as plt
import json 

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
            img.append(4)

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

def encode(header: dict, intensity_img: np.ndarray, org_intensity : np.ndarray, phase_img : np.ndarray, org_phase : np.ndarray, path: str, name: str) -> None:
    """Generate a .dat file from the header and the pictures

    Args:
        header (dict): header of the original file
        intensity_img (np.ndarray): new intensity data format (n,m, nb_bucket)
        org_intensity (np.ndarray): origin of the intensity data format (3, nb_bucket)
        phase_img (np.ndarray): new phase data format (n,m)
        org_phase (np.ndarray): origin of the phase data format (3, 1)
        path (str): path where .dat file will be saved
        name (str): name of the .dat file

    Returns:    
    return (None): None
    """


    ac_height, ac_width = intensity_img.shape[:2] #TODO : gerer les buckets
    cn_height, cn_width = phase_img.shape
    intensity_img = np.reshape(intensity_img, ac_height*ac_width)
    phase_img = np.reshape(phase_img, cn_height*cn_width)

    with open(f"{path + '/' + name}", 'wb') as file:
        file.seek(0)

        for i in range(header['header_size']):
            file.write((0x00).to_bytes(1, "big"))
        
        file.seek(0)
        file.write(header['magic_number'].to_bytes(4, "big"))
        file.write(header['header_format'].to_bytes(2, "big"))
        file.write(header['header_size'].to_bytes(4, "big"))

        file.seek(48)
        #origine
        file.write(int(org_intensity[0, 0]).to_bytes(2, "big"))
        file.write(int(org_intensity[1, 0]).to_bytes(2, "big"))
        #dimensions
        file.write(ac_width.to_bytes(2, "big")) #width
        file.write(ac_height.to_bytes(2, "big")) #height
        file.write(header['ac_n_bucket'].to_bytes(2, "big")) #n_bucket
        #range
        file.write(int(np.max(intensity_img)).to_bytes(2, "big"))
        #n_bytes
        file.write((ac_height*ac_width*header['ac_n_bucket']*4).to_bytes(4, "big"))
        
        #phase
        file.seek(64)
        #origine
        file.write(int(org_phase[0, 0]).to_bytes(2, "big"))
        file.write(int(org_phase[1, 0]).to_bytes(2, "big"))
        #dimensions
        file.write(cn_width.to_bytes(2, "big")) #width
        file.write(cn_height.to_bytes(2, "big")) #height
        file.write((cn_height*cn_width*4).to_bytes(4, "big")) #n_bytes

        file.seek(164)
        file.write(struct.pack('f', header['intf_scale_factor']))
        file.write(struct.pack('f', header['wavelength_in']))

        file.seek(176)
        file.write(struct.pack('f', header['obliquity_factor']))

        file.seek(218)
        file.write(header['phase_res'].to_bytes(2, "big"))
        
        file.seek(header['header_size'] - 1)
        intensity_img_line = np.reshape(intensity_img, (ac_height*ac_width*header['ac_n_bucket'], 1))
        for i in range(ac_height*ac_width*header['ac_n_bucket']):
            file.write(int(intensity_img_line[i]).to_bytes(4, "big"))
        
        
        phase_img_line = np.reshape(phase_img, (cn_height*cn_width, 1))

        for i in range(cn_height*cn_width):
            file.write(int(phase_img_line[i]).to_bytes(4, "big"))

def convert(header : dict, phase_img : np.ndarray, type : str) -> np.ndarray:
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

def prof_topo(A : list,B : list, img : np.ndarray) -> tuple:

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

    step = np.sign(x2-x1)
    X = np.round(np.arange(x1, x2+1,step)).astype(int)
    Y = np.round(f(X)).astype(int)

    prof = img[X,Y]
    
    return X, Y, prof

def recadrage(path_dict : str) -> None:
    """Crop all the images in the json file
    path_dict (str): Path of the json file
    
    return None
            but generate cropped image in .dat format in the out_path folder specified in the json file"""


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
    n_bucket = header_0['ac_n_bucket']

    x0 = p1[crop_number]
    x0 = np.array(x0)

    x0_augm = np.empty((np.shape(x0)[0],3))
    x0_augm[:, :2] = x0
    x0_augm[:, 2] = img_phase_org[x0[:,1], x0[:,0]]
    
    org_phase_0 = get_org_img(header_0, 'phase')
    org_intensity_0 = get_org_img(header_0, 'intensity')


    for i in range(len(img_name)):
        if i != crop_number:

            header_i = header_reader(origin_path +  '/' + img_name[i])

            img_phase_i = get_img(origin_path +  '/' + img_name[i], 'phase')
            img_intensity_i = get_img(origin_path +  '/' + img_name[i], 'intensity')
            
            org_intensity_i = get_org_img(header_i, 'intensity')
            org_phase_i = get_org_img(header_i, 'phase')
            
            x_i  = p1[i]
            x_i = np.array(x_i)

            x_i_augm = np.empty((np.shape(x_i)[0],3))
            x_i_augm[:, :2] = x_i
            x_i_augm[:, 2] = img_phase_i[x_i[:,1], x_i[:,0]]


            s, R, t = recadrage_cpd(x_i_augm, x0_augm)


            
            img_phase_format_i = format_img(img_phase_i)
            img_phase_recadr_i, min_x_phase, min_y_phase, min_z_phase = apply_recadr(img_phase_format_i, s, R, t)

            #-----------------Recadrage des origines devrait être fonctionnalisé-----------------#
            org_phase_recadr_i = s*np.dot( org_phase_i[:,0],R) + t
            org_phase_recadr_i -= np.array([min_x_phase, min_y_phase, min_z_phase])
            org_phase_recadr_i[0], org_phase_recadr_i[1] = org_phase_recadr_i[1], org_phase_recadr_i[0] 
            org_phase_recadr_i = org_phase_recadr_i[:, np.newaxis]
            #------------------------------------------------------------------------------------#
        
            img_intensity_i_0 = format_img(img_intensity_i[:,:,0])
            img_intensity_recadr_i_0, min_x_intensity, min_y_intensity, min_z_intensity = apply_recadr(img_intensity_i_0, s, R, t)

            #-----------------Recadrage des origines devrait être fonctionnalisé-----------------#
            org_intensity_recadr_i = s*np.dot(org_intensity_i[:,0], R) + t
            org_intensity_recadr_i -= np.array([min_x_intensity, min_y_intensity, min_z_intensity])
            org_intensity_i[0], org_intensity_i[1] = org_intensity_i[1], org_intensity_i[0]
            org_intensity_recadr_i = org_intensity_recadr_i[:, np.newaxis]
            #------------------------------------------------------------------------------------#

            img_intensity_recadr_i = np.empty((np.shape(img_intensity_recadr_i_0)[0], np.shape(img_intensity_recadr_i_0)[1], n_bucket))
            img_intensity_recadr_i[:,:,0] = img_intensity_recadr_i_0
            
            for k in range(1, n_bucket):

                img_intensity_i_k = format_img(img_intensity_i[:,:,k])
                img_intensity_recadr_i_k = apply_recadr(img_intensity_i_k, s, R, t)[0]
                img_intensity_recadr_i[:,:,k] = img_intensity_recadr_i_k


            encode(header = header_i, 
                   intensity_img = img_intensity_recadr_i, org_intensity = org_intensity_recadr_i, 
                   phase_img = img_phase_recadr_i, org_phase = org_phase_recadr_i,
                   path = out_path, name = img_name[i])
            
            # print(org_intensity_recadr_i, org_phase_recadr_i)
        else :

            # print(org_intensity_0, org_phase_0)
            encode(header_0, 
                   intensity_img = img_intensity_org, org_intensity = org_intensity_0, 
                   phase_img = img_phase_org,  org_phase = org_phase_0,
                   path = out_path, name = img_name[crop_number])





if (__name__ == '__main__'):
    get_img('data//CALSPAR15C_init-to-d7//CALSPAR15C_d2_image1-5x.dat', 'phase')
        
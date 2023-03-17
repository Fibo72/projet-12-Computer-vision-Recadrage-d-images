import struct
import numpy as np
import matplotlib.pyplot as plt


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
    header['intf_scale_factor'] = struct.unpack('f',data[164:168])[0]
    header['wavelength_in'] = struct.unpack('f',data[168:172])[0]
    header['obliquity_factor'] = struct.unpack('f',data[176:180])[0]
    header['phase_res'] = int.from_bytes(data[218:220], "big")
    header['phase_raw'] = data[header['header_size'] + header['ac_n_bytes']: header['header_size'] +header['ac_n_bytes'] + header['cn_n_bytes']]

    return header




def decod_phase_img(header: dict) ->np.array:
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
            img.append(val*(header['intf_scale_factor']*header['wavelength_in']*header['obliquity_factor']/32768))
        else :
            img.append(0)

    pic = np.reshape(np.array(img), (header['cn_height'],header['cn_width']))
    return pic


if (__name__ == '__main__'):
        
    pic = decod_phase_img(header_reader('data\CALSPAR16C_init-to-d7\CALSPAR16C_d1_image2-20x.dat'))

    plt.imshow(pic, cmap = 'gnuplot_r')

    plt.show()


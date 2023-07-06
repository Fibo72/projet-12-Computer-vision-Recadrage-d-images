from Aymeric.decode_img import *

img1 = get_img("data\CALSPAR15C_init-to-d7\CALSPAR15C_d1_image1-5x.dat", 'phase')
header1 = header_reader("data\CALSPAR15C_init-to-d7\CALSPAR15C_d1_image1-5x.dat")

img1_= convert(header1, img1, 'meter')
plt.figure()
plt.imshow(img1_)
plt.show()

X_max = np.array(img1_.shape[0])
Y_max = np.array(img1_.shape[1])

print(convert(header1, X_max, 'meter'))
print(convert(header1, Y_max, 'meter'))
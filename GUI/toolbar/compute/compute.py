import numpy as np
from GUI.toolbar.compute.loading import Loading

class Computer():
    def __init__(self, master):
        self.master = master
        self.pb = None
        self.factors = None
        self.output_dir = None

    def compute(self, ref_index, points):
        '''
        Compute and return (s,R,t) for each image which is not the reference.
        we have :
            - s : scale factor
            - R : rotation matrix
            - t : translation vector
        the expected result is a numpy array of shape (n,3) where n is the number of images

        note that at index ref_index, (s,R,t) = (1, identity, 0)
        '''
        # TODO : compute the result

    def tranform_image(self, images, s, R, t):
        '''
        Apply the transformation (s,R,t) to the image and return the result.
        '''
        # TODO : apply the transformation
    
    def process_transformations(self, images, factors):
        '''
        Apply the transformations to the images and return the result.
        '''
        self.pb = Loading(self.master, self)

        transformed_images = np.empty_like(images)
        images_amount = len(images)

        for i in range(images_amount):
            self.pb.update(i, images_amount)
            transformed_images[i] = self.tranform_image(images[i], *factors[i])
        
        self.pb.enable_button()
        return transformed_images
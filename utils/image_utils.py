import cv2

def read_image(path):

    image = cv2.imread(path)

    return image
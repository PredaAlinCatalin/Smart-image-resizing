import sys
import cv2 as cv
import numpy as np
import copy

from parameters import *
from select_path import *

import pdb

def compute_energy(img):
    """
    calculeaza energia la fiecare pixel pe baza gradientului
    :param img: imaginea initiala
    :return:E - energia
    """
    # urmati urmatorii pasi:
    # 1. transformati imagine in grayscale
    # 2. folositi filtru sobel pentru a calcula gradientul in directia X si Y
    # 3. calculati magnitudinea pentru fiecare pixel al imaginii
    E = np.zeros((img.shape[0],img.shape[1]))
    #TODO: scrieti codul

    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    sobelx = cv.Sobel(img_gray, cv.CV_64F, 1, 0)
    sobely = cv.Sobel(img_gray, cv.CV_64F, 0, 1)

    E = np.abs(sobelx) + np.abs(sobely)
    return E

def show_path(img, path, color):
    new_image = img.copy()
    for row, col in path:
        new_image[row, col] = color

    E = compute_energy(img)
    new_image_E = img.copy()
    new_image_E[:, :, 0] = E.copy()
    new_image_E[:, :, 1] = E.copy()
    new_image_E[:, :, 2] = E.copy()

    for row, col in path:
        new_image_E[row, col] = color
    cv.imshow('path img', np.uint8(new_image))
    cv.imshow('path E', np.uint8(new_image_E))
    cv.waitKey(1000)


def delete_path(img, path):
    """
    elimina drumul vertical din imagine
    :param img: imaginea initiala
    :path - drumul vertical
    return: updated_img - imaginea initiala din care s-a eliminat drumul vertical
    """
    updated_img = np.zeros((img.shape[0], img.shape[1] - 1, img.shape[2]), np.uint8)
    for i in range(img.shape[0]):
        col = path[i][1]
        # copiem partea din stanga
        updated_img[i, :col] = img[i, :col].copy()
        # copiem partea din dreapta
        updated_img[i, col:] = img[i, col + 1:].copy()
        
    return updated_img

def decrease_width(params: Parameters, num_pixels, resized_image=None):
    if resized_image is not None:
        img = resized_image.copy()
    else:
        img = params.image.copy() # copiaza imaginea originala
    for i in range(num_pixels):
        print('Eliminam drumul vertical numarul %i dintr-un total de %d.' % (i+1, num_pixels))

        # calculeaza energia dupa ecuatia (1) din articol                
        E = compute_energy(img)
        path = select_path(E, params.method_select_path)
        if params.show_path:
            show_path(img, path, params.color_path)
        img = delete_path(img, path)

    cv.destroyAllWindows()
    return img


def decrease_height(params: Parameters, num_pixels, resized_image=None):
    if resized_image is not None:
        img = resized_image.copy()
    else:
        img = params.image.copy() # copiaza imaginea originala
    img = cv.rotate(img, cv.ROTATE_90_CLOCKWISE)
    for i in range(num_pixels):
        print('Eliminam drumul vertical numarul %i dintr-un total de %d.' % (i + 1, num_pixels))

        # calculeaza energia dupa ecuatia (1) din articol
        E = compute_energy(img)
        path = select_path(E, params.method_select_path)
        if params.show_path:
            show_path(img, path, params.color_path)
        img = delete_path(img, path)

    img = cv.rotate(img, cv.ROTATE_90_COUNTERCLOCKWISE)
    cv.destroyAllWindows()
    return img


def delete_object(params: Parameters, x0, y0, w, h):
    return None

def resize_image(params: Parameters):

    if params.resize_option == 'micsoreazaLatime':
        # redimensioneaza imaginea pe latime
        resized_image = decrease_width(params, params.num_pixels_width)
        return resized_image

    elif params.resize_option == 'micsoreazaInaltime':
        resized_image = decrease_height(params, params.num_pixels_height)
        return resized_image
    
    elif params.resize_option == 'amplificaContinut':

        pixels_width = int(params.image.shape[1] * 0.05)
        pixels_height = int(params.image.shape[0] * 0.05)
        resized_image = cv.resize(params.image, (params.image.shape[1] + pixels_width, params.image.shape[0] + pixels_height))
        resized_image = decrease_width(params, pixels_width, resized_image)
        resized_image = decrease_height(params, pixels_height, resized_image)
        return resized_image

    elif params.resize_option == 'eliminaObiect':
        return None

    else:
        print('The option is not valid!')
        sys.exit(-1)
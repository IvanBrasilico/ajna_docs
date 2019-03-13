import cv2
import PIL
import numpy as np
from PIL import ImageOps

def autocontrast(pil_image: PIL.Image, cutoff: int = 15) -> PIL.Image:
    return ImageOps.autocontrast(pil_image, cutoff=cutoff)


def equalize(pil_image: PIL.Image) -> PIL.Image:
    return ImageOps.equalize(pil_image)


def expand_tocolor(pil_image: PIL.Image,
                   alpha: float = 1.33,
                   beta: float = 1.4) -> PIL.Image:
    imgarray = np.asarray(pil_image)
    gray = np.array(imgarray[:, :,  0] * 3. * alpha ** beta, dtype=np.float32)
    enhanced_R = gray.copy()
    enhanced_R[enhanced_R > 254] = 254
    enhanced_G = (gray - 255)
    enhanced_G[enhanced_G > 254] = 254
    enhanced_G[enhanced_G < 0] = 0
    enhanced_B = (gray - 511)
    enhanced_B[enhanced_B < 0] = 0
    enhanced_B[enhanced_B > 254] = 254
    enhanced_RGB = np.dstack((enhanced_R, enhanced_G, enhanced_B)).astype(np.uint8)
    enhanced_color = PIL.Image.fromarray(enhanced_RGB)
    return enhanced_color


def enhancedcontrast_cv2(pil_image: PIL.Image) -> PIL.Image:
    opencvImage = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    # CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3., tileGridSize=(8, 8))
    lab = cv2.cvtColor(opencvImage, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
    l, a, b = cv2.split(lab)  # split on 3 different channels
    l2 = clahe.apply(l)  # apply CLAHE to the L-channel
    lab = cv2.merge((l2, a, b))  # merge channels
    new_img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR
    return PIL.Image.fromarray(new_img)

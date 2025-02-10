from PIL import Image 
from PIL.ExifTags import TAGS
import uuid
import numpy as np
import os


class Colors:
    """
    definizione dei colori
    usati per la stampa dei messaggi
    """
    WARNING = "\033[93m" # yellow
    SUCCESS = "\033[92m" # green
    MESSAGE = "\033[94m" # blue
    RESET = "\033[0m" # default color


class Utilities:
    """
    Questa classe contiene i metodi 
    """
    
    def findPixelsInRange(image, min_rgb, max_rgb, start_index, p_width, p_height, out = False):
        """
        trova i pixel che rientrano all'interno di un certo range di valori rgb

        Parameters:
            image (pillow.Image):
                immagine di cui classificare i pixel
            min_rgb (touple):
                valore minimo del range rgb
            max_rgb (touple):
                valore massimo del range rgb 
            start_index (touple):
                touple contenente gli indici (i, j) da cui 
                far partire il quadrato
        """
        founded = []
        out_of_range = []

        img_array = np.array(image)

        
        for i in range(start_index[0], start_index[0] + p_height):
            for j in range(start_index[1], start_index[1] + p_width):
                r, g, b = img_array[i][j]
                if min_rgb[0] <= r <= max_rgb[0] and \
                min_rgb[1] <= g <= max_rgb[1] and \
                min_rgb[2] <= b <= max_rgb[2]:
                    founded.append((i,j))
                else:
                    out_of_range.append((i,j))

        if out:
            return founded, out_of_range
        else:
            return founded
        

    def isImageFile(filename):
        img_ext = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp'}
        _,ext = os.path.splitext(filename)
        return ext.lower() in img_ext
        
    

    def uniqueIDGenerator(dict):
        """
        genera un id unico per un dizionario,
        poiche il metodo uuid4 genera un codice casuale con alta probabilita 
        di essere univoco è stato implementato questo medo al fine di
        garantire che questa eventualita non si verifichi in ogni caso
        """
        ID = str(uuid.uuid4())

        if ID not in dict:
            return ID
        else:
            return Utilities.uniqueIDGenerator(dict)
            


    def extractImageMetadata(image):
        """
        estrae i metadati da un immagine
        
        Parameters:
            image (pillow.Image):
                immagine da cui estrarre i metadati
        """
        coded_metadata = image._getexif()
        meta_data = {}

        # verifica che siano presenti metadati
        if coded_metadata:
            for tag, value in coded_metadata.items():
                tag_name = TAGS.get(tag, tag)
                meta_data[tag_name] = value
        else:
            return 0
        
        return meta_data
    

    def colorPixels(image, start_index, p_width, p_height, color):
        """
        colora i pixel di un quadrato p_width, p_height partendo da 
        start_index
        """
        pixels = image.load()

        for i in range(start_index[0], start_index[0] + p_height):
            for j in range(start_index[1], start_index[1] + p_width):
                pixels[j, i] = color


    def colorBlockPixels(image, pixels_list, color):
        pixels = image.load()

        for px_blocks in pixels_list:
            # print(el)
            for px in px_blocks:
                if px[1] < image.width and px[0] < image.height:  
                    pixels[px[1], px[0]] = color
                else:
                    print(f'''
                        img_width:{image.width}
                        img_height: {image.height}
                        px[0]: {px[0]}
                        px[1]: {px[1]}
                    ''')
            # for px in el[0]:
            #     pixels[px[1], px[0]] = color



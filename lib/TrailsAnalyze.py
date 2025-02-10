from PIL import Image
import math
import numpy as np

class TrailsAnalyze:
    
    def findStarCenter(image, pixel_block):
        """
        Calcola il valore del pixel centrale che rappresenta la stella
        e il relativo errore

        parameters:
            ponderate (bool):
                se True, nel calcolo della posizione media e del relativo
                errore esegue una media ponderata sulla luminosita dei pixel
                he compongono l'immagine

        Returns:
            stars (list):
                ritorna una lista contenenti delle touple nel formato
                (i, j, di, dj) rappresentati la miglior stima degli indici
                i, j che rappresentano il pixel centrale della stella e i relativi
                errori di, dj
        """
        i_sum = 0
        j_sum = 0
        i_dev = 0
        j_dev = 0
        l_sum = 0

        # verifica che l'array non sia vuoto
        if len(pixel_block) == 0:
            return (0,0,0,0)

        # carica i pixel dell'immagine
        image_pixels = image.load()

        # calcolo delle cordinate del centro
        for pixel in pixel_block:
            r = image_pixels[pixel[1],pixel[0]][0]
            g = image_pixels[pixel[1],pixel[0]][1]
            b = image_pixels[pixel[1],pixel[0]][2]       

            brightness =  0.299 * r + 0.587 * g + 0.114 * b

            i_sum += pixel[0] * brightness
            j_sum += pixel[1] * brightness
            l_sum += brightness

        i_best = math.ceil(i_sum/l_sum)
        j_best = math.ceil(j_sum/l_sum)

        # calcolo degli errori sulle cordinate delc centro
        for pixel in pixel_block:
            r = image_pixels[pixel[1],pixel[0]][0]
            g = image_pixels[pixel[1],pixel[0]][1]
            b = image_pixels[pixel[1],pixel[0]][2]    

            brightness =  0.299 * r + 0.587 * g + 0.114 * b

            i_dev += ((pixel[0] - i_best)**2) * brightness
            j_dev += ((pixel[1] - j_best)**2) * brightness   

        i_err = math.ceil(np.sqrt(i_dev/l_sum))    
        j_err = math.ceil(np.sqrt(j_dev/l_sum))  

        return (i_best, j_best, i_err, j_err)    


    def findTrailsCenter():
        pass    



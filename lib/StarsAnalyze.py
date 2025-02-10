from PIL import Image
# from IPython.display import display
import numpy as np
import random
import copy
# from .Utilities import Colors
# from .Utilities import Utilities
# from .TrailsAnalyze import TrailsAnalyze
from Utilities import Colors
from Utilities import Utilities
from TrailsAnalyze import TrailsAnalyze
from scipy.spatial import cKDTree




class StarsAnalyze:
    """Analizza le stelle presenti nell'immagine"""
    def __init__(self, image):
        self.image = image
        self.founded_stars = []
        self.removed_stars = []


    def findStars(self, min_magnitude = 0.16, max_magnitude = 1, group = 30, smls_np = 50, center_value = False):
        """
        riconosce all'interno di un immagine i pixel contigui 
        che rappresentano una stella e ritorna dizionario
        le cui chiavi sono pixel rappresentativi della stella
        e i valori delle liste con touple conteneti le coordinate dei
        pixel relativi a quella stella

        Parameters:
            min_magnitude (float): 
                valore di magnitudine minimo (compreso tra 0 e 1).
                Nota: il valore minimo non puo essere superiore di quello massimo

            max_magnitude (float):
                valore di magnitudine massimo (compreso tra 0 e 1)
                Nota: il valore massimo non puo essere inferiore di quello minimo

            
            group (int):
                la distanza neccessaria per classificare i pixel
                vicini che rappresentano una stella

            smls_np (int):
                il numero minimo di pixel che un blocco deve contenere
                per essere classificato come valido per analisi

        Returns:
            new_dict (dict):
                dizionario con coppie chiave valore, in cui la chiave e un
                valore intero univoco che identifica la stella e 
                il valore una lista contenente tutte le coordinate 
                dei pixel che rappresentano quella stella
        """

        # converte il valore di magnitudine in  valori rgb
        min = min_magnitude * 255
        max = max_magnitude * 255

        # trova i pixel validi
        image_array = np.array(self.image)

        mask = (
        (image_array[..., 0] >= min) & (image_array[..., 0] <= max) &
        (image_array[..., 1] >= min) & (image_array[..., 1] <= max) &
        (image_array[..., 2] >= min) & (image_array[..., 2] <= max)
        )

        # trova i pixel validi
        valid_pixels = np.argwhere(mask)

        # raggruppa i pixel validi in gruppi contigui
        tree = cKDTree(valid_pixels)
        visited = set()
        groups = []

        for idx, pixel in enumerate(valid_pixels):
            if idx in visited:
                continue
            cluster_indices = tree.query_ball_point(pixel, r=group)
            cluster = valid_pixels[cluster_indices]
            groups.append(cluster.tolist())
            visited.update(cluster_indices)

        
        for el in groups:
            if len(el) > smls_np:
                self.founded_stars.append(el)
            else:
                self.removed_stars.append(el)

        return self.founded_stars


    def showFoundedStars(self, fnd_c = (125, 190, 255), rmv_c = (255, 100, 100), show = True):
        """
        Visualizza le stelle trovate nell'immagine

        parameters:
            fnd_c (touple):
                touple con valori rgb con cui evidenziare le stelle trovate

            rmv_c (touple):
                touple con valori rgb con cui evidenziare le stelle rimosse

            show_removed (bool):
                Se True, evidenzia le stelle che sono state rimosse, 
                se false mostra solo le stelle valide per l'analisi.
        """
        image_pixels = self.image.load()

        # evidenzia le stelle che sono state trovate
        for star_block in self.founded_stars:
            for i, j in star_block:
                image_pixels[j, i] = fnd_c

        # evidenzia le stelle scartate
        for star_block in self.removed_stars:
            for i, j in star_block:
                image_pixels[j, i] = rmv_c

        if show == True:
            self.image.show()


    def saveImage(self, path, image_name):
        self.image.save(f'{path}/{image_name}')





















from PIL import Image
import numpy as np
import random
import copy
import os
from StarsAnalyze import StarsAnalyze
from Utilities import Utilities
from Utilities import Colors
from TrailsAnalyze import TrailsAnalyze
from pprint import pprint
import json
import pandas as pd
from PIL import ImageDraw
import random


class StarsTracker:
    """
    Si occupa di tracciare la posizione delle stelle a diverse istanti di tempo
    """
    def __init__(self, images_path: str, star_options: list):
        self.images_path = images_path
        self.star_options = star_options
        self.stars_data = pd.DataFrame(columns=["id", "immagine", "centro", "blocchi", "timestamp"])
        self.metadata_cache = {}
        self.n_valid_for_analysis = 0
        self.n_founded = 0


    def _load_images(self):
        "carica le immagini e le ordina"
        images_names = [image for image in os.listdir(self.images_path) if Utilities.isImageFile(image)]
        images_names.sort()
        return images_names


    def _extract_metadata(self, images_names):
        for image_name in images_names:
            image_path = f"{self.images_path}/{image_name}"
            with Image.open(image_path) as img:
                self.metadata_cache[image_name] = Utilities.extractImageMetadata(img)


    def _find_stars_initial_position(self, first_image: Image.Image, image_name: str):
        """Trova le stelle iniziali nella prima immagine e inizializza il DataFrame."""
        stars_analyze = StarsAnalyze(first_image)
        stars_positions = stars_analyze.findStars(*self.star_options)

        # calcola il numero di stelle trovate
        self.n_valid_for_analysis = stars_analyze.founded_stars
        self.n_founded = stars_analyze.founded_stars + stars_analyze.removed_stars


        print(f"""{Colors.SUCCESS} 
        Trovati {len(stars_analyze.founded_stars + stars_analyze.removed_stars)} blocchi di pixel che rappresentano stelle
            - {len(stars_analyze.founded_stars)} classificati validi per analisi
            - {len(stars_analyze.removed_stars)} scartati
        {Colors.RESET}""")

        for block in stars_positions:
            star_id = Utilities.uniqueIDGenerator(self.stars_data["id"].tolist())
            center = TrailsAnalyze.findStarCenter(first_image, block)
            timestamp = self.metadata_cache[image_name]['DateTime']

            self.stars_data = pd.concat([
                self.stars_data,
                pd.DataFrame([{"id": star_id, "immagine": image_name, "centro": center, "blocchi": block, "timestamp": timestamp}])
            ], ignore_index=True)


    def _track_stars_in_image(self, current_image: Image.Image, image_name: str, prev_image_name: str, src_size: int):
        """Traccia le stelle nell'immagine corrente basandosi sulle posizioni precedenti."""
        for idx, row in self.stars_data[self.stars_data["immagine"] == prev_image_name].iterrows():
            prev_center = row["centro"]
            s_i, s_j = prev_center[0] - int(src_size/2) , prev_center[1] - int(src_size/2)


            # Controlla che il ritaglio sia all'interno dell'immagine
            if not (0 <= s_i  < current_image.height and 0 <= s_j  < current_image.width):
                continue

            # Esegui il ritaglio
            region = current_image.crop((s_j, s_i, s_j + src_size, s_i + src_size))
            region_analyze = StarsAnalyze(region)
            found_stars = region_analyze.findStars(*self.star_options)

            if found_stars:
                # Calcola il centro della stella nel ritaglio
                center = TrailsAnalyze.findStarCenter(region, found_stars[0])
                global_center = (center[0] + s_i, center[1] + s_j, center[2], center[3])  # Coordinate globali del centro

                # Calcola le coordinate globali dei blocchi
                global_block = [(x + s_i, y + s_j) for x, y in found_stars[0]]

                # print('global_block',global_block)

                # Salva nel DataFrame
                timestamp = self.metadata_cache[image_name]['DateTime']

                self.stars_data = pd.concat([
                    self.stars_data,
                    pd.DataFrame([{
                        "id": row["id"],
                        "immagine": image_name,
                        "centro": global_center,
                        "blocchi": global_block,
                        "timestamp": timestamp
                    }])
                ], ignore_index=True)


    
    def _filter_tracking_result(self, filter_value):
        # Raggruppa per 'id' e conta le righe per ciascun ID
        id_counts = self.stars_data['id'].value_counts()

        # Filtra solo gli ID con almeno 50 righe
        valid_ids = id_counts[id_counts >= filter_value].index

        # Filtra il DataFrame mantenendo solo gli ID validi
        self.stars_data = self.stars_data[self.stars_data['id'].isin(valid_ids)]



    def startTracking(self, filter_value = 10, src_size: int = 20) -> pd.DataFrame:
        """Avvia il tracciamento delle stelle e restituisce il DataFrame con i dati."""
        images_names = self._load_images()

        # Estrazione anticipata dei metadati
        self._extract_metadata(images_names)


        # messaggio inziziale 
        print(f"""{Colors.MESSAGE}
RICERCA POSIZIONI STELLE NELL'IMMAGINE:
              
        OPZIONI DI RICERCA SELEZIONATE:
            magintudine minima =    {self.star_options[0]} / rgb {int(self.star_options[0] * 255)}
            magnitudine massima =   {self.star_options[1]} / rgb {int(self.star_options[1] * 255)}
            group distance =        {self.star_options[2]}
            valid block dimension > {self.star_options[3]} px
            {Colors.RESET}
        """)

        # Processa la prima immagine
        first_image = Image.open(f"{self.images_path}/{images_names[0]}")
        self._find_stars_initial_position(first_image, images_names[0])

        # Processa le immagini successive
        for i, image_name in enumerate(images_names[1:], start=1):
            print(f"\r{Colors.MESSAGE}Analizzo immagine {i} di {len(images_names) - 1}...{Colors.RESET}", end='', flush=True)
            current_image = Image.open(f"{self.images_path}/{image_name}")
            self._track_stars_in_image(current_image, image_name, images_names[i - 1], src_size)

        print(f"\n{Colors.SUCCESS}Tracciamento completato. Dati salvati in DataFrame.{Colors.RESET}")

        # filtra i dati
        self._filter_tracking_result(filter_value)
        return self.stars_data
    


    def showStarTrakingResult(self, save_path: str = None):

        # nomi delle immagini
        images_names = [image for image in os.listdir(self.images_path) if Utilities.isImageFile(image)]
        images_names.sort()

        # immagine
        image = Image.open(f'{self.images_path}/{images_names[0]}')
        pixels = image.load()


        star_ids = list(self.stars_data["id"].unique())

        for star_id in star_ids:
            star_rows = self.stars_data[self.stars_data["id"] == star_id]

            # genera valori rgb casuali
            r = random.randint(20, 244)
            g = random.randint(20, 244)
            b = random.randint(20, 244)

            pixels_to_draw = list(star_rows["blocchi"])
            # print(pixels_to_draw)
            Utilities.colorBlockPixels(image, pixels_to_draw, (r, g, b))


        # Salva l'immagine se richiesto
        if save_path != None:
            image.save(save_path)
            print(f"Immagine salvata in: {save_path}")
        else:
            image.show()
    

    def saveData(self, path, data_name):
        self.stars_data.to_csv(f'{path}/{data_name}.csv', index=False)



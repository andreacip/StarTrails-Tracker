# Star Trails Tracking Library

## Descrizione
Questa libreria Python è progettata per analizzare e tracciare il movimento delle stelle in una serie di immagini catturate a intervalli regolari. L'obiettivo è identificare le stelle, calcolarne le posizioni precise e analizzare i dati per studiare fenomeni come gli star trails, utilizzando tecniche di elaborazione delle immagini e analisi dei dati.

## Funzionalità principali
- **Identificazione delle stelle**:
  - Riconosce i pixel contigui che rappresentano le stelle in un'immagine e li raggruppa in base alla loro luminosità.
  - Classifica le stelle in base a criteri configurabili, come magnitudine luminosa e dimensioni del gruppo.

- **Tracciamento delle stelle**:
  - Segue il movimento delle stelle in una serie di immagini successive.
  - Utilizza ritagli localizzati per migliorare la precisione del tracciamento e ridurre i costi computazionali.

- **Calcolo del centro delle stelle**:
  - Determina il centro luminoso di ogni stella utilizzando una media ponderata basata sulla luminosità dei pixel.
  - Calcola gli errori associati per valutare l'affidabilità delle stime.

- **Gestione dei dati**:
  - Salva i risultati del tracciamento in un formato tabellare (CSV) per analisi successive.
  - Estrae i metadati EXIF dalle immagini per sincronizzare i dati temporali.

- **Visualizzazione**:
  - Colora i pixel per evidenziare le stelle identificate e le loro traiettorie.

## Requisiti
- Python 3.8 o superiore
- Librerie Python necessarie:
  - `numpy`
  - `pandas`
  - `Pillow`
  - `scipy`

## Installazione
1. Clona il repository:
   ```bash
   git clone https://github.com/username/star-trails-tracking.git
   ```
2. Accedi alla directory del progetto:
   ```bash
   cd star-trails-tracking
   ```
3. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

## Utilizzo

### Identificazione delle stelle
Per analizzare un'immagine e identificare le stelle presenti:

```python
from StarsAnalyze import StarsAnalyze
from PIL import Image

image = Image.open("path/to/image.jpg")
stars_analyzer = StarsAnalyze(image)
stars = stars_analyzer.findStars(min_magnitude=0.2, max_magnitude=1.0)
print(stars)
```

### Tracciamento delle stelle
Per tracciare il movimento delle stelle in una sequenza di immagini:

```python
from StarsTracker import StarsTracker

tracker = StarsTracker(images_path="path/to/images", star_options=[0.2, 1.0, 30, 50])
data = tracker.startTracking()
print(data)
```

### Visualizzazione delle stelle identificate
Per evidenziare le stelle trovate e salvare un'immagine annotata:

```python
stars_analyzer.showFoundedStars(fnd_c=(125, 190, 255))
stars_analyzer.saveImage(path="output", image_name="annotated_image.jpg")
```

### Salvataggio dei dati
Per salvare i dati del tracciamento in un file CSV:

```python
tracker.saveData(path="output", data_name="star_tracking_results")
```

## Struttura del progetto
- **`StarsAnalyze.py`**:
  Identifica e raggruppa le stelle in base ai pixel contigui e alla luminosità.
- **`StarsTracker.py`**:
  Traccia il movimento delle stelle attraverso una sequenza di immagini.
- **`TrailsAnalyze.py`**:
  Calcola il centro e l'errore delle stelle in base alla luminosità dei pixel.
- **`Utilities.py`**:
  Contiene funzioni di supporto per l'elaborazione delle immagini, la gestione dei dati e la visualizzazione.

## Contributi
Contributi, segnalazioni di bug e richieste di funzionalità sono benvenuti! Per favore, apri un'issue o invia una pull request.

## Licenza
Questo progetto è distribuito sotto la licenza MIT. Consulta il file [LICENSE](LICENSE) per maggiori dettagli.

## Contatti
Autore: [Andrea Cipriano]([https://github.com/username](https://github.com/andreacip))  
Email: andreacipriano.ac@hotmail.com



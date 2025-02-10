from PIL import Image
from lib.StarsAnalyze import StarsAnalyze
import time



if __name__ == "__main__":
    img = Image.open('images/test_img.jpg')
    test_img = StarsAnalyze(img)
    start_time = time.time()
    stars = test_img.findStars()
    end_time = time.time()
    total = end_time - start_time
    test_img.showFoundedStarsCenter()
    print(f'tempo impiegato {total}')

    # pass``
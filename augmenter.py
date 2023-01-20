from pathlib import Path
import os
from pprint import pprint
import time
from subprocess import Popen, PIPE
import cv2
from cv2 import dnn_superres

sr = dnn_superres.DnnSuperResImpl_create()

if __name__ == "__main__":
    Path('Augmented').mkdir(exist_ok=True)

    augmentation_error_paths = []

    for path in next(os.walk('Downloads/'))[1]:
        input_chapter_folder = 'Downloads/' + path
        output_chapter_folder = 'Augmented/' + path

        if Path(output_chapter_folder).is_dir():
            if len(os.listdir(input_chapter_folder)) == len(os.listdir(output_chapter_folder)):
                print(f"Directory {output_chapter_folder} already augmented entirely, skipping...")
                continue
        
        Path(output_chapter_folder).mkdir(exist_ok=True)
        print(f"Augmenting folder {input_chapter_folder} into {output_chapter_folder}...", end="")
        start_time = time.time()

        for filename in os.listdir(input_chapter_folder):
            # print(f"Augmenting file {filename}")
            print(".", end="", flush=True)
            # Read image
            image = cv2.imread(input_chapter_folder + '/' + filename)

            # Read the desired model
            path = "FSRCNN_x4.pb"
            sr.readModel(path)

            # Set the desired model and scale to get correct pre- and post-processing
            sr.setModel("fsrcnn", 4)

            # Upscale the image
            result = sr.upsample(image)

            # Save the image
            cv2.imwrite(output_chapter_folder + '/' + filename, result)

        print(f" ({round(time.time() - start_time, 3)}s)\n")
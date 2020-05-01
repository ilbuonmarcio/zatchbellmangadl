from pathlib import Path
import os
from pprint import pprint
import time
from subprocess import Popen, PIPE

if __name__ == "__main__":
    Path('Augmented').mkdir(exist_ok=True)

    augmentation_error_paths = []

    for path, _, files in os.walk('Downloads/'):
        if len(files) == 0:
            continue

        input_chapter_folder = path
        output_chapter_folder = 'Augmented/' + path.replace('Downloads/', '')

        if Path(output_chapter_folder).is_dir():
            if len(os.listdir(input_chapter_folder)) == len(os.listdir(output_chapter_folder)):
                print(f"Directory {output_chapter_folder} already augmented entirely, skipping...")
                continue

        
        Path(output_chapter_folder).mkdir(exist_ok=True)
        print(f"Augmenting folder {input_chapter_folder} into {output_chapter_folder}...")
        start_time = time.time()

        process = Popen(
            [
                '.\waifu2x-ncnn-vulkan.exe',
                '-v',
                '-i',
                input_chapter_folder,
                '-o',
                output_chapter_folder,
                '-s',
                '2'
            ],
            stdout=PIPE,
            stderr=PIPE
        )
        stdout, stderr = process.communicate()

        if ' failed' in str(stderr, encoding='utf-8'):
            augmentation_error_paths.append(input_chapter_folder)
            print(f"One or more files on input folder {input_chapter_folder} has some erroneous file in it, check it and rerun the application for augmenting those files")
        else:
            print(f"Folder {input_chapter_folder} augmented successfully in {time.time() - start_time}s\n")

    if len(augmentation_error_paths) == 0:
        print("There are no errors found in the input directories, all files are augmented correctly!")
    else:
        print("The following input paths has some errors in it, check it manually and rerun the application")
        for path in augmentation_error_paths:
            print(path)
        print("Rerun the augmenter after you fixed all those paths")

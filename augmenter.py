from pathlib import Path
import os
from pprint import pprint

if __name__ == "__main__":
    Path('Augmented').mkdir(exist_ok=True)

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
        os.system(f".\waifu2x-ncnn-vulkan.exe -v -i {input_chapter_folder} -o {output_chapter_folder} -s 2")

        



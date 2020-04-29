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
        
        files = [f[2] for f in os.walk(input_chapter_folder)][0]

        Path(output_chapter_folder).mkdir(exist_ok=True)
        for f in files:
            os.system(f".\waifu2x-ncnn-vulkan.exe -i {input_chapter_folder}/{f} -o {output_chapter_folder}/{f} -s 2")

        



import requests
import bs4
from pprint import pprint
import time
import ntpath
from pathlib import Path


INVALID_CHAR_FILENAME_FILTER = '<>:"/\|?* '
BASE_URL = "https://mangakakalot.com/chapter/konjiki_no_gash/chapter_"


if __name__ == "__main__":
    # Getting all chapters list from page 1
    first_page = requests.get(BASE_URL + "1").content
    soup = bs4.BeautifulSoup(first_page, 'html.parser')
    
    # Getting all chapter IDs and titles
    chapters = [
        [elem['value'], elem.contents[0]]
        for elem in soup.find('select', {'id': 'c_chapter'}).findChildren('option')
    ]

    for chapter in chapters:
        for invalid_char in INVALID_CHAR_FILENAME_FILTER:
            chapter[1] = chapter[1].replace(invalid_char, '_')

    for chapter in chapters:
        chapter_id = chapter[0]
        chapter_title = chapter[1]

        print(f"[ID:{chapter_id}] Getting image url list for {chapter_title}")

        page = requests.get(BASE_URL + chapter_id).content
        soup = bs4.BeautifulSoup(page, "html.parser")

        chapter_images_urls = [elem['src'] for elem in soup.find('div', {'id': 'vungdoc'}).findChildren('img')]
        chapter.append(chapter_images_urls)

        time.sleep(1)

    Path('Downloads').mkdir(exist_ok=True)

    for chapter in chapters:
        image_urls = chapter[2]
        chapter_save_path = 'Downloads/' + chapter[1] + '/'

        # Check if already downloaded
        # If already downloaded, skip to next one
        if Path(chapter_save_path).is_dir():
            if len([f[2] for f in os.walk(chapter_save_path)][0]) == len(chapter[2]):
                print(f"Folder {chapter_save_path} already downloaded entirely, skipping...")

        Path(chapter_save_path).mkdir(exist_ok=True)
        print(f"Created folder {chapter_save_path}")

        for image_url in image_urls:
            print(f"Dowloading from {image_url}", end=" ")
            image = requests.get(image_url)
            image_name = ntpath.basename(image_url)
            image_buffer = image.content
            
            with open(chapter_save_path + image_name, 'wb') as output_file:
                output_file.write(image_buffer)
            print("Done!")

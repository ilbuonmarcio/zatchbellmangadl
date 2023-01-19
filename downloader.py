import requests
import bs4
import ntpath
from pathlib import Path
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

INVALID_CHAR_FILENAME_FILTER = '<>:"/\|?*. '
BASE_URL = "https://mangakakalot.com/chapter/gc894419/chapter_"


def download_image(image_url, chapter_save_path):
    print(f"Dowloading from {image_url}", end=" ")
    image = requests.get(image_url)
    image_name = ntpath.basename(image_url)
    image_buffer = image.content
    
    with open(chapter_save_path + image_name, 'wb') as output_file:
        output_file.write(image_buffer)
    print("Done!")


if __name__ == "__main__":
    # Getting all chapters list from page 1
    first_page = requests.get(BASE_URL + "1").content
    soup = bs4.BeautifulSoup(first_page, 'html.parser')
    
    # Getting all chapter IDs and titles
    chapters = [
        [elem['data-c'], elem.contents[0]]
        for elem in soup.find('select', {'class': 'navi-change-chapter'}).findChildren('option')
    ]

    for chapter in chapters:
        for invalid_char in INVALID_CHAR_FILENAME_FILTER:
            chapter[1] = chapter[1].replace(invalid_char, '_')

    Path('Downloads').mkdir(exist_ok=True)
    print(f"Found {len(chapters)} in website!")
    for chapter in chapters:
        chapter_save_path = 'Downloads/' + chapter[1] + '/'

        # Check if already downloaded
        # If already downloaded, skip to next one
        if Path(chapter_save_path).is_dir():
            files = [f[2] for f in os.walk(chapter_save_path) if len(f[2]) > 0]
            if len(files) > 0:
                print(f"Folder {chapter_save_path} already downloaded, skipping...")
                continue

        Path(chapter_save_path).mkdir(exist_ok=True)
        print(f"Created folder {chapter_save_path}")

        driver.get(BASE_URL + chapter[0])

        # Downloading actual images
        imgs = driver.find_elements(By.CSS_SELECTOR, "div.container-chapter-reader img")
        for i in range(0, len(imgs)):
            with open(f"{chapter_save_path}/{i}.png", 'wb') as output_file:
                output_file.write(imgs[i].screenshot_as_png)

    driver.close()


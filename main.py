import requests
from lxml import html
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from fpdf import FPDF
import unicodedata

def unicode_normalize(s):
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')


def extract_tab(driver):
    print('extracting tab')

    tab = driver.find_element_by_class_name('_3g9-D').text

    return tab


def try_all_fonts(array_to_write, fonts_to_use):
    for font in fonts_to_use:
        print('using font : ' + font)
        write_to_pdf(array_to_write, font, font)


def write_to_pdf(array_to_write, meta_information, artist, name_song, font, path):
    print('writing pdf')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font(font, "B", size=16)

    pdf.cell(200, 20, txt = name_song + " by " + artist, ln=1, align="C")

    pdf.set_font(font, size=10)

    for info in meta_information:
        pdf.cell(200, 5, txt=info, ln=1, align="L")

    pdf.cell(200, 20, txt="", ln=1, align="L")

    for line in array_to_write:
        line = line.replace(u"\u2019", "")
        line = line.replace(u"\u2013", "")

        pdf.cell(200, 5, txt=str(line), ln=1, align="L")

    path = path + name_song + ".pdf"

    pdf.output(path)

    print('written pdf')


def extract_meta_info(driver):
    print('extracting meta info')

    meta_information = driver.find_elements_by_class_name('_17Weg')
    artist = driver.find_elements_by_class_name('_2x2k1')

    if artist != []:
        artist = str(artist[0].text)
    else:
        artist = "Unknown"

    try:
        song = str(driver.find_element_by_xpath('//header[@class="_30s9W"]//h1').text)
    except:
        song = ""
    index = 0
    for info in meta_information:
        meta_information[index] = str(info.text)
        index += 1

    return meta_information, artist, song


def create_driver(url):
    print("creating driver")

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver_to_use = webdriver.Chrome(executable_path='C:\\Users\\tesser\Desktop\chromedriver', options=chrome_options)
    driver_to_use.get(url)
    time.sleep(1)

    return driver_to_use


def main(url, path):
    fonts = ['Courier', 'Helvetica', 'Symbol', 'Times', 'ZapfDingbats']
    best_font = 'Courier'

    print("starting process")

    driver = create_driver(url)

    meta_info, artist, song = extract_meta_info(driver)
    tab_extracted = extract_tab(driver)

    print("parsing tab")
    tab_in_lines = tab_extracted.splitlines()

    write_to_pdf(tab_in_lines, meta_info, artist, song, best_font, path)

    print("closing driver")
    driver.close()

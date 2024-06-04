"""import docstring"""
from pathlib import Path
from typing import List

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


def scrap(url: str, wd: webdriver, limit: int) -> List[str]:
    """"""
    wd.get(url)
    xpath_pattern = '//*[@href and not(contains(@href, "css") or contains(@href, "png") or contains(@href, "php"))]'
    elems_with_urls = wd.find_elements(By.XPATH, xpath_pattern)
    urls = [href.get_attribute('href') for href in elems_with_urls]

    return urls


def filter()


def scrap_everywhere(str, wd: webdriver, limit: int) -> List[str]:
    """A recursive function that scrap on every site"""


def main(start_url: str, output_file: Path, limit: int) -> None:
    """Try to scrap everywhere and find relevant sites"""
    print('Initializing webdriver...')
    wd = webdriver.Chrome()
    wd.implicitly_wait(5)

    urls2scrap = [start_url]
    urls_relevant = []
    for url in urls2scrap:
        if not url or len(urls_relevant) >= limit:
            print(f'Finished scrapping. Scrapped {len(urls_relevant)} relevant urls.')
        else:
            urls_raw = scrap(url, wd, limit)

    print(f'Writing results to {output_file}.')
    with open(output_file, 'w') as file:
        for url in urls_relevant:
            file.write(url, '\n')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Try to scrap everywhere and find relevant sites')
    parser.add_argument('start_url', type=str, help='Starting url.')
    parser.add_argument('output_file', type=Path, help='A txt file to store results.')
    parser.add_argument('-l', '--limit', type=int, default=50, help='The number of urls. Default set to 50.')

    args = parser.parse_args()

    main(start_url=args.url,
         output_file=args.output_file,
         limit=args.limit)

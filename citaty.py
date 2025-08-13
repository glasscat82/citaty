import os
from bs4 import BeautifulSoup
from art import tprint
from helper import *


PATH_JSON_FILES = 'json'

@try_decorator
def get_tags(col):
    """ parsing tags """
    col_tags = col.find('div', {'class':'quote__tags'})
    if col_tags is None:
        return False

    res = {}
    sources_or_tags = col_tags.findChildren('div', recursive=False)
    for index, source_or_tag in enumerate(sources_or_tags, 1):
        if index == 1:
            sources = source_or_tag.find_all('div', {'class':'field-item'})
            res['source'] = [item.text.strip() for item in sources]

        if index == 2:
            tags = source_or_tag.find_all('div', {'class':'field-item'})
            res['tags'] = [item.text.strip() for item in tags]

        if index > 2:
            continue

    return res

@try_decorator
def get_row(col):
    """ row """
    col_body = col.find('div', {'class':'field-name-body'}).text.strip()
    col_tags = get_tags(col)

    row = {}
    row['body'] = col_body

    if col_tags is not False:
        row = row | col_tags

    return row

@try_decorator
def get_links(html:str):
    """ links url """
    soup = BeautifulSoup(html, 'lxml')
    selection_main = soup.find('main', {'id':'content'})
    view_content = selection_main.find('div', {'class':'view-content'})

    links = []
    for col in view_content.find_all('article'):
        col_row = get_row(col)
        if col_row is False:
            continue

        links.append(col_row)

    return links

@benchmark
def main(url: str, page:int):
    """ this main """
    for i in range(page):
        url_get = f'{url}?page={i}' if i >= 1 else url

        html = get_html(url_get)
        if html is not False:
            links = get_links(html)
            append_json(links, f'./{PATH_JSON_FILES}/{get_file_name(url_get)}')
            pc(f'[+] → {i}', url_get, color = 2)
        else:
            pc(f'[-] 159 → html is False', color = 1)

def get_file_name(url: str):
    """ return file name """
    urls_get = url.split('?')
    urls = urls_get[0].split('/')

    return f'{urls[-1]}_{dt.now():%d-%m-%Y_%H}.json'

if __name__ == "__main__":
    """ parsing citaty """
    tprint('.: citaty :.', font='cybermedium')

    if os.path.isdir(PATH_JSON_FILES) is False:
        os.makedirs(f'./{PATH_JSON_FILES}', exist_ok=True)
        pc('[+] created folder', color=3)

    url = f'https://citaty.info/man/viktor-pelevin'
    main(url, 50)
""" this helper function """
from datetime import datetime as dt
import sys, json
import requests, fake_useragent

def benchmark(func):
    def wrapper(*args, **kwargs):
        now = dt.now()
        #-----------------start
        return_value = func(*args, **kwargs)
        #-----------------end
        end = dt.now()
        pc(f'[+] the end → {str(end - now)}', color = 6)
        return return_value
    return wrapper

def try_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            return_value = func(*args, **kwargs)
        except Exception as e:
            pc(sys.exc_info()[1], color = 1)
            return_value = False

        return return_value
    return wrapper

def pc(text: str, *args, color: int = 6):
    """ 1 red, 2 green, 3 yello, 4 blue, 5 purple, 6 blue """
    print(f'\033[3{color}m{text}', *args, sep=' / ', end='\033[0m\n')

def wtf(html, filename):
    with open(filename, "w") as f:
        f.write(html)

def write_json(data, path):
    with open(path, 'w', encoding='utf8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    except Exception as e:
        pc(f'[-] 26 → {sys.exc_info()[1]}', color = 1)
        return False

def append_json(json, path):
    get_json = load_json(path)
    data = get_json + json if get_json is not False else json
    write_json(data, path)

def get_html(url_page: str):
    """ return HTML """
    header = {'User-Agent': str(fake_useragent.UserAgent().google)}
    try:
        page = requests.get(url=url_page, headers = header, timeout = 10)
        return page.text

    except Exception as e:
        pc(sys.exc_info()[1], color = 1)
        return False
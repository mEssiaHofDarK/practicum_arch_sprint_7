import json

import requests
import names
import os
from bs4 import BeautifulSoup

base_url = 'https://dota2.fandom.com'
h_url = "https://dota2.fandom.com/ru/wiki/%D0%98%D1%81%D1%82%D0%BE%D1%80%D0%B8%D1%8F"
uniq_names = set()
current_dir = os.path.dirname(__file__)


def get_link_data(url):
    return requests.get(url).text


def clean_hyperlinks(text):
    remove_items = ['[1]', '[2]', '[3]', '[4]', '[5]', '[6]', '[7]', '[8]', '[9]', ]
    for remove_item in remove_items:
        text = text.replace(remove_item, '')
    return text


def generate_new_name():
    while True:
        name = names.get_first_name()
        if name and name not in uniq_names:
            break
    uniq_names.add(name)
    return name


def replace_name(text, name, new_name):
    return text.replace(name, new_name)


def parse():
    name_mapping = {}
    res = get_link_data(h_url)
    soup = BeautifulSoup(res, 'html.parser')
    links = {link.text: base_url + link.get('href') for link in ((soup.find('tbody')).find_all('a'))[3:]}
    links_num = len(links)
    count = 0
    for name, link in links.items():
        count += 1
        link_data = get_link_data(link)
        soup = BeautifulSoup(link_data, 'html.parser')
        try:
            text = clean_hyperlinks(soup.find('p').text)
        except Exception:
            print(f'{name} - SKIP (completing on {count/links_num*100}%)')
            continue
        if not text:
            print(f'{name} - EMPTY DATA (completing on {count/links_num*100}%)')
            continue
        new_name = generate_new_name()
        new_text = replace_name(text, name, new_name)
        with open(f'{current_dir}/knowledge_base/{new_name}.txt', 'w') as f:
            f.write(new_text + "\n")
        name_mapping[name] = new_name
        print(f'{name} - OK (completing on {(count/links_num*100):.2f}%)')
    with open(f'{current_dir}/name_mapping.json', 'w') as f:
        json.dump(name_mapping, f)


if __name__ == '__main__':
    parse()
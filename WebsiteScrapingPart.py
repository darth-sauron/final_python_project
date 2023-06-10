import json

import requests as requests
from bs4 import BeautifulSoup


def del_non_ascii(word):
    """
        Removes non-ASCII characters from a word.

        Args:
            word (str): The input word.

        Returns:
            str: The word with non-ASCII characters removed.
    """

    new_word = ''.join(char if ord(char) < 128 else ' ' for char in word)
    return new_word


def make_races(website, j_file):
    """
        Scrapes race or class information from a website and saves it in a JSON file.

        Args:
            website (str): The URL of the website to scrape.
            j_file (str): The path to the JSON file to save the race or class information.
    """

    response = requests.get(website)
    content = response.content

    soup = BeautifulSoup(content, 'html.parser')
    elements = soup.find_all('h2')

    races_dict = {}

    for element in elements:

        div = element.find_next('div', class_='table-wrapper')
        table = div.find('table')

        tmp = {}
        races_dict[element.text] = tmp

        rows = table.tbody.find_all('tr')

        for row in rows:
            columns = row.find_all('td')
            if len(columns) == 2:
                ability_score = columns[0].text.strip()
                value = columns[1].text.strip()

                ability_score = del_non_ascii(ability_score)
                value = del_non_ascii(value)
                races_dict[element.text][ability_score] = value

    json_races = json.dumps(races_dict, indent=4)
    j = open(j_file, "w")
    j.write(json_races)
    j.close()

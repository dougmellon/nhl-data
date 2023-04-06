import argparse
import requests
import logging
from bs4 import BeautifulSoup

choices = [
    'draft',
    'player-stats'
]

parser = argparse.ArgumentParser(
    prog='NHL-Data',
    description='Tool for grabbing and parsing NHL data',
    epilog='Fuck the Habs'
)

parser.add_argument(
    '-r',
    '--request',
    required=True,
    nargs=1,
    choices=choices,
    help='Type of request being made. Options: draft'
)

parser.add_argument(
    '-y',
    '--year',
    nargs=1,
    help='Accepts a year in the format #### (eg. 2023)'
)

args = parser.parse_args()


def scrape_draft_results(year):
    url = f'https://www.hockey-reference.com/draft/NHL_{year}_entry.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    picks_table = soup.find(id='div_stats').find('tbody')
    picks_array = picks_table.find_all('tr')

    picks = []

    for pick in picks_array:
        try:
            picks.append({
                'pick_num': pick.find('th', {'data-stat': 'pick_overall'}).text,
                'team_name': pick.find('td', {'data-stat': 'team_name'}).text,
                'player_name': pick.find('td', {'data-stat': 'player'}).text,
                'birth_country': pick.find('td', {'data-stat': 'birth_country'}).text,
                'position': pick.find('td', {'data-stat': 'pos'}).text,
                'draft_age': pick.find('td', {'data-stat': 'draft-age'}),
                'amateur_team': pick.find('td', {'data-stat': 'amateur_team'}).text
            })

        except Exception:
            logging.warning('Encountered a row without identifying data. (Hint: Likely a header)')

    return picks


def print_all_picks(picks):
    for i in picks:
        print('Overall Pick: {pick_num}, Team: {team_name}, Player Name: {player_name}, '
              'Birth Country: {birth_country}, Position: {position}, Draft Age: {draft_age}, '
              'Amateur Team: {amateur_team} \n'.format(**i))


if __name__ == '__main__':
    print_all_picks(scrape_draft_results(args.year[0]))

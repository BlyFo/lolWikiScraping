import re
import ast
import sys
import requests
from enum import Enum
from bs4 import BeautifulSoup


class Color(Enum):
    RESET = 'RESET'
    BLACK = 'BLACK'
    RED = 'RED'
    GREEN = 'GREEN'
    YELLOW = 'YELLOW'
    BLUE = 'BLUE'
    MAGENTA = 'MAGENTA'
    CYAN = 'CYAN'
    WHITE = 'WHITE'
    # There are more but I'm lazy


def get_info():
    url = "https://leagueoflegends.fandom.com/wiki/Module:ChampionData/data"

    # Make a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
      # Parse the HTML content with BeautifulSoup
        page = BeautifulSoup(response.text, 'html.parser')

        # Find the element with class "mw-code mw-script"
        script_element = page.find('pre', class_='mw-code mw-script')

      # Check if the element is found
        if script_element:
          # Extract and print the text inside the element
            extracted_text = script_element.get_text()
            return extracted_text
        else:
            print("Element with class 'mw-code mw-script' not found on the page.")
    else:
        print(
            f"Failed to retrieve the page. Status code: {response.status_code}")
    # In case nothing is found
    return None


def parse_info(info: str):
    # Extract the Lua-like code between "-- <pre>", "-- </pre>", white space and return
    lua_code = info.split("-- <pre>")[-1].split("-- </pre>")[0]
    lua_code = lua_code.strip().replace("return ", "")

    # Replace [<String>] with "<String>"
    cleaned_keys_string = re.sub(r'\["(.*?)"\]', r'"\1"', lua_code)

    # Replace [<Number>] with "<Number>"
    cleaned_keys_number = re.sub(r'\[(\d+)\]', r'"\1"', cleaned_keys_string)

    # Replace "=" with ":"
    cleaned_equals = cleaned_keys_number.replace("=", ":")

    # Remove hp_level since sometimes has broken data like 45+56/8
    lines = cleaned_equals.split('\n')
    lines2 = list(filter(lambda l: '"hp_lvl"' not in l, lines))
    cleaned_text = '\n'.join(lines2)

    try:
        data_dict = ast.literal_eval(cleaned_text)
    except SyntaxError as e:
        print(f"Error parsing Lua-like code: {e}")
        data_dict = {}

    return data_dict


def print_colored_text(text: str, color: Color):
    colors = {
        Color.RESET: '\033[0m',
        Color.BLACK: '\033[30m',
        Color.RED: '\033[31m',
        Color.GREEN: '\033[32m',
        Color.YELLOW: '\033[33m',
        Color.BLUE: '\033[34m',
        Color.MAGENTA: '\033[35m',
        Color.CYAN: '\033[36m',
        Color.WHITE: '\033[37m',
    }

    return colors[color] + text + colors[Color.RESET]


def print_champ_stats(champ: str, game_mode: str, info: dict):
    PORCENTAGE_STATS = ["dmg_dealt", "dmg_taken"]
    game_mode_stats = info[champ]['stats'][game_mode]

    print(f"{champ} - {game_mode.upper()}:")

    for stat in game_mode_stats.items():
        value = stat[1]
        is_porcentage = False

        if stat[0] in PORCENTAGE_STATS:
            is_porcentage = True
            value = int(value * 100 - 100)

        stat_sign = "+" if value >= 0 else ""
        value_string = f"{stat_sign}{value}" + "%" if is_porcentage else ""
        value_color = Color.GREEN if value >= 0 else Color.RED
        value_string_colored = print_colored_text(value_string, value_color)

        print(f"  {stat[0]}: {value_string_colored}")


def main():
    champ = ""
    game_mode = "aram"
    arguments = sys.argv

    if len(arguments) == 1:
        error = print_colored_text(
            "   [ERROR] No arguments provided.",
            Color.RED
        )
        print(error)
        print("   Use -> <Script> <CHAMP> <GAME_MODE>")
        return

    if len(arguments) == 2:
        champ = arguments[1]

    if len(arguments) == 3:
        champ = arguments[1]
        game_mode = arguments[2]

    champ = champ.capitalize()
    page_info = get_info()
    if page_info:
        parsed_info = parse_info(page_info)
        print_champ_stats(champ, game_mode, parsed_info)


main()

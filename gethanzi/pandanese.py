#!/Users/richardlong/Code/scripts/gethanzi/.venv/bin/python3

import sys;
import argparse;
from bs4 import BeautifulSoup;
import requests;
import pyperclip


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


parser = argparse.ArgumentParser(description='Get menumonics from pandanese.com')

parser.add_argument('hanzi', metavar='C', type=str, help='the char to lookup')

args = parser.parse_args()

url = f"https://www.pandanese.com/search?q={args.hanzi}"
soup = BeautifulSoup(requests.get(url).text, 'html.parser')
dic = {}
labels = ['meaning', 'mneumonic', 'reading', 'reading mneumonic']
count = 0
for tag in soup.find_all('div', class_='definition_value'):
    text = tag.text.strip()
    dic[labels[count]] = text
    count += 1
    if count == 4:
        break

if dic.get('meaning') == None:
    print(color.RED + "No results found" + color.END)
    sys.exit(1)

print()
formattedOutput = ''
terminalOutput = ''
for key, value in dic.items():
    formattedOutput += f"<div><b>{key}</b>: {value}</div>\n<div><br></div>\n\n"
    terminalOutput += f"{color.BOLD}{color.CYAN}{key}{color.END}{color.END}: {value}\n\n"

print(terminalOutput)

pyperclip.copy(formattedOutput)

print(color.BOLD + color.GREEN + "Copied to clipboard" + color.END)



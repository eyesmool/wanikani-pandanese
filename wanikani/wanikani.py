#!/Users/richardlong/Code/scripts/wanikani/.venv/bin/python3

import sys;
import argparse;
from bs4 import BeautifulSoup;
import requests;
import pyperclip
import re

def listToDict(lst):
    res_dict = {}
    for i in range(0, len(lst), 2):
        res_dict[lst[i]] = lst[i + 1]
    return res_dict

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

parser = argparse.ArgumentParser(description='Get menumonics from wanikani.com')

parser.add_argument('type', metavar='type', type=str, help='vocab / kanji')
parser.add_argument('char', metavar='char', type=str, help='the char to lookup')


args = parser.parse_args()

def format_and_print(char, color, dic, radicalsDict=None):
    formattedOutput = f'<div><b>{char}</b></div>\n'
    terminalOutput = f'{color.BOLD}{color.PURPLE}character: {color.END}{color.END}{char}\n\n'
    if (radicalsDict):
        formattedOutput += "<div><b>Radicals</b>:</div>\n"
        terminalOutput += f"{color.BOLD}{color.PURPLE}radicals{color.END}{color.END}:\n"
        for key, value in radicalsDict.items():
            formattedOutput += f"<li>{key}: {value}</li>\n"
            terminalOutput += f"{color.BOLD}{color.PURPLE}{key}{color.END}{color.END}: {value}\n"
        formattedOutput += "<div><br></div>\n\n"
        terminalOutput += "\n"
    
    for key, value in dic.items():
        formattedOutput += f"<div><b>{key}</b>: {value}</div>\n<div><br></div>\n\n"
        terminalOutput += f"{color.BOLD}{color.PURPLE}{key}{color.END}{color.END}: {value}\n\n"
    
    print(terminalOutput)

    pyperclip.copy(formattedOutput)

    print(color.BOLD + color.GREEN + "Copied to clipboard" + color.END)

if args.type == 'vocab':
    url = f"https://www.wanikani.com/vocabulary/{args.char}"
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    dic = {}
    cleaned_text = ''
    for section in soup.find_all('section', class_='subject-section__subsection'):
        cleaned_text += re.sub(r'\s+', ' ', section.text).strip() + '\n'
    
    if (cleaned_text == ''): 
        print(color.RED + f"{args.type} not found" + color.END)
        sys.exit()

    # print(cleaned_text)
    
    primary_pattern = r"Primary\s(.+?)(?:\sAlternatives|\sWord\sType)"
    primary = re.search(primary_pattern, cleaned_text)
    if primary:
        dic['primary'] = primary.group(1)
    
    alternatives_pattern = r"Alternatives\s(.+)\sWord\sType"
    alternatives = re.search(alternatives_pattern, cleaned_text)
    if alternatives:
        dic['alternatives'] = alternatives.group(1)
    
    meaning_explanation_pattern = r"Word\sType\s.+\sExplanation(.+)"
    meaning_explanation = re.search(meaning_explanation_pattern, cleaned_text)
    if meaning_explanation:
        dic['meaning_explanation'] = meaning_explanation.group(1)
      
    pronunciation_pattern = r"(.+)\sKyoko"
    pronunciation = re.search(pronunciation_pattern, cleaned_text)
    if pronunciation:
        dic['pronunciation'] = pronunciation.group(1)
    
    mnemonic_pattern = r"\)\sExplanation\s(.+)\sContext\sSentences"
    mnemonic = re.search(mnemonic_pattern, cleaned_text)
    if mnemonic:
        dic['mnemonic'] = mnemonic.group(1)
    
    
    format_and_print(args.char, color, dic)

if args.type == 'kanji':
    url = f"https://www.wanikani.com/kanji/{args.char}"
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    dic = {}
    cleaned_text = ''
    radicals_text = ''
    # Get radical information
    for tag in soup.find_all('section', class_='subject-section subject-section--components'):
        radicals_text += re.sub(r'\s+', ' ', tag.text).strip()

    radicals_text = re.sub(r'Radical\sCombination','', radicals_text).strip()
    # print(radicals_text)
    # this is a bit of a hack with the ｲ character, but it works for now
    pattern = r'([\u4e00-\u9fff\u30a0-\u30ff\u2e80-\u2effｲ]+)\s+([a-zA-Z\s]+)'
    matches = re.findall(pattern, radicals_text)
    radicalsArray = [item for match in matches for item in match]
    radicalDict = listToDict(radicalsArray)

    for section in soup.find_all('section', class_='subject-section__subsection'):
        cleaned_text += re.sub(r'\s+', ' ', section.text).strip() + '\n'
    
    if (cleaned_text == ''): 
        print(color.RED + f"{args.type} not found" + color.END)
        sys.exit()
    
    primary_pattern = r"Primary\s(.+?)(?:\sAlternatives|\sWord\sType|\n)"
    primary = re.search(primary_pattern, cleaned_text)
    if primary:
        dic['primary'] = primary.group(1)
    
    meaning_mnemonic_pattern = r"Mnemonic\s(.+)\n"
    meaning_mnemonic = re.search(meaning_mnemonic_pattern, cleaned_text)
    if meaning_mnemonic:
        dic['meaning mnemonic'] = meaning_mnemonic.group(1)

    onyomi_pattern = r"On’yomi\s(.+)\sKun’yomi"
    onyomi = re.search(onyomi_pattern, cleaned_text)
    if onyomi:
        dic['onyomi'] = onyomi.group(1).strip()
    
    kunyomi_pattern = r"Kun’yomi\s(.+)\sNanori"
    kunyomi = re.search(kunyomi_pattern, cleaned_text)
    if kunyomi:
        dic['kunyomi'] = kunyomi.group(1).strip()
    
    nanori_pattern = r"Nanori\s(.+)\n"
    nanori = re.search(nanori_pattern, cleaned_text)
    if nanori:
        dic['nanori'] = nanori.group(1).strip()
        
    reading_mnemonic_pattern = r"Nanori.+\sMnemonic\s(.+)\n"
    reading_mnemonic = re.search(reading_mnemonic_pattern, cleaned_text)
    if reading_mnemonic:
        dic['reading mnemonic'] = reading_mnemonic.group(1).strip()
        
    format_and_print(args.char, color, dic, radicalDict)
    print(color.BOLD + color.YELLOW + f"Source: {url} " + color.END)

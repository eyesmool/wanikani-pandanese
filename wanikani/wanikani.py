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

def fetch_kanji_data(char):
    url = f"https://www.wanikani.com/kanji/{char}"
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    dic = {}
    radicals_text = ''
    cleaned_text = ''
    # Get radical information
    for tag in soup.find_all('section', class_='subject-section subject-section--components'):
        radicals_text += re.sub(r'\s+', ' ', tag.text).strip()

    radicals_text = re.sub(r'Radical\sCombination','', radicals_text).strip()
    # print(radicals_text)
    # this is a bit of a hack with the ｲ and L character, but it works for now
    pattern = r'([\u4e00-\u9fff\u30a0-\u30ff\u2e80-\u2effｲL㠯]+)\s+([a-zA-Z\s]+)'
    matches = re.findall(pattern, radicals_text)
    radicalsArray = [item for match in matches for item in match]
    radicalDict = listToDict(radicalsArray)

    for section in soup.find_all('section', class_='subject-section__subsection'):
        cleaned_text += re.sub(r'\s+', ' ', section.text).strip() + '\n'

    if (cleaned_text == ''): 
        print(color.RED + f"kanji {char} not found" + color.END)
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

    return dic, radicalDict, url
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
parser.add_argument('-r', '--recursive', action='store_true', help='recursively looks up kanji')
parser.add_argument('-b', '--breakdown', action='store_true', help='breaks down non hira/kana chars')
parser.add_argument('-l', '--lookup', action='store_true', help='looks up every kanji')
parser.add_argument('-f', '--format', action='store_true', help='formats for anki flexbox')


# TODO: have a --radical flag that looks adds radicals




args = parser.parse_args()

def format_and_print(char, color, dic, radicalsDict=None, radical=None):
    formattedOutput = f'<div class="kanji"><b>{char}</b></div>\n'
    if (radical):
        terminalOutput = f'{color.BOLD}{color.PURPLE}radical: {color.END}{color.END}{char}\n\n'
    else:
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
        if key == 'breakdown': 
            breakDown = ''
            formatBreakDown = '<div>'
            for k, v in value.items():
                breakDown += f"[{k}: {v}] "
                formatBreakDown += f"<li>[{k}: {v}]</li>"
            formatBreakDown += '</div>'
            formattedOutput += f"<div><b>{key}</b>: {formatBreakDown}</div>\n<div><br></div>\n\n"
            terminalOutput += f"{color.BOLD}{color.PURPLE}{key}{color.END}{color.END}: {breakDown}\n\n"
            continue
        formattedOutput += f"<div><b>{key}</b>: {value}</div>\n<div><br></div>\n\n"
        terminalOutput += f"{color.BOLD}{color.PURPLE}{key}{color.END}{color.END}: {value}\n\n"
    
    print(terminalOutput)

    pyperclip.copy(formattedOutput)

    print(color.BOLD + color.GREEN + "Copied to clipboard" + color.END)
    
    return formattedOutput

if args.type == 'vocab':
    url = f"https://www.wanikani.com/vocabulary/{args.char}"
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    dic = {}
    cleaned_text = ''
    rawBreakdown = ''
    for section in soup.find_all('section', class_='subject-section__subsection'):
        cleaned_text += re.sub(r'\s+', ' ', section.text).strip() + '\n'
    
    if (cleaned_text == ''): 
        print(color.RED + f"{args.type} not found" + color.END)
        sys.exit()
    
    for section in soup.find_all('div', class_='subject-character-grid'):
        rawBreakdown += re.sub(r'\s+', ' ', section.text).strip() + '\n'
        # print(rawBreakdown)
        kanjiSplit = re.findall(r'[一-龥]+|[ぁ-ん]+|[A-Za-z]+(?: [A-Za-z]+)?', rawBreakdown)
        kanjiBreakdown = {}
        for i in range(0, len(kanjiSplit), 3):
            kanjiBreakdown[kanjiSplit[i]] = kanjiSplit[i + 1] + ' ' + kanjiSplit[i + 2]
        dic['breakdown'] = kanjiBreakdown
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
    
    # mnemonic_pattern = r"\)\sExplanation\s(.+)\sContext\sSentences"
    mnemonic_pattern = r"\)\sExplanation\s(.+)\n"
    mnemonic = re.search(mnemonic_pattern, cleaned_text)
    if mnemonic:
        dic['mnemonic'] = mnemonic.group(1)
    
    if args.recursive and args.format and 'breakdown' in dic:
        formattedOutput = """<div class="flex">"""
        formattedOutput += """<div class="child">"""
        formattedOutput += format_and_print(args.char, color, dic)
        formattedOutput += """</div>"""
        for k, v in dic['breakdown'].items():
            formattedOutput += """<div class="child">"""
            kanji_dic, radicalDict, kanji_url = fetch_kanji_data(k)
            formattedOutput += format_and_print(k, color, kanji_dic, radicalDict)
            formattedOutput += """</div>"""
            pyperclip.copy(formattedOutput)
        formattedOutput += """</div>"""
    elif args.recursive and 'breakdown' in dic:
        formattedOutput = format_and_print(args.char, color, dic)
        for k, v in dic['breakdown'].items():
            kanji_dic, radicalDict, kanji_url = fetch_kanji_data(k)
            formattedOutput += format_and_print(k, color, kanji_dic, radicalDict)
            pyperclip.copy(formattedOutput)
    else:
        formattedOutput = format_and_print(args.char, color, dic)
        pyperclip.copy(formattedOutput)

    print(color.BOLD + color.YELLOW + f"Source: {url} " + color.END)

if args.type == 'kanji':
    if args.lookup or args.recursive:
        formattedOutput = """<div class="flex">"""
        for char in args.char:
            dic, radicalDict, url = fetch_kanji_data(char)
            formattedOutput += """<div class="child">"""
            # formattedOutput += f"""<div class="hanzi">{char}</div> <br>"""
            formattedOutput += format_and_print(char, color, dic, radicalDict)
            formattedOutput += """</div>"""
            print(color.BOLD + color.YELLOW + f"Source: {url} " + color.END)
        formattedOutput += """</div>"""
        pyperclip.copy(formattedOutput)
else:
        dic, radicalDict, url = fetch_kanji_data(args.char)
        format_and_print(args.char, color, dic, radicalDict)
        print(color.BOLD + color.YELLOW + f"Source: {url} " + color.END)

if args.type == 'radical':
    # use radical text from radicalDict i.e. (穴: Hole) to make 
    #     url = f"https://www.wanikani.com/radicals/hole"
    url = f"https://www.wanikani.com/radicals/{args.char}"
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    dic = {}
    radicals_text = ''
    for tag in soup.find_all('section', class_='subject-section__content'):
        radicals_text += re.sub(r'\s+', ' ', tag.text).strip()
    # to do: finish this
    # print(radicals_text)
    mnemonic_pattern = r"Mnemonic\s(.+?)[^\x00-\x7F]"
    mnemonic = re.search(mnemonic_pattern, radicals_text)
    if mnemonic:
        dic['mnemonic'] = mnemonic.group(1).strip()
    
    format_and_print(args.char, color, dic, None, args.char)
    print(color.BOLD + color.YELLOW + f"Source: {url} " + color.END)


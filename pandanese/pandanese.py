#!/Users/richardlong/Code/scripts/gethanzi/.venv/bin/python3

import sys;
import argparse;
from bs4 import BeautifulSoup;
import requests;
import pyperclip
import concurrent.futures
from collections import OrderedDict


def format_output(char, dic):
    formattedOutput = f"<div><b>hanzi</b>: {char}</div>\n<div><br></div>\n\n"
    terminalOutput = f"{color.BOLD}{color.CYAN}hanzi{color.END}{color.END}: {char}\n\n"
    for key, value in dic.items():
        formattedOutput += f"<div><b>{key}</b>: {value}</div>\n<div><br></div>\n\n"
        terminalOutput += f"{color.BOLD}{color.CYAN}{key}{color.END}{color.END}: {value}\n\n"

    print(terminalOutput)

    pyperclip.copy(formattedOutput)

    print(color.BOLD + color.GREEN + "Copied to clipboard" + color.END)
    
    return formattedOutput
    
def get_substrings(hanzi):
    # TODO: can make more efficient if 希望 exists then so do the individual components
    substrings = [hanzi[i:j] for i in range(len(hanzi)) for j in range(i+1, len(hanzi)+1)]
    substrings.sort(key=len, reverse=True)
    print(substrings)

    subStrOrderedDict = OrderedDict()
    dic = {}

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_subStr = {executor.submit(does_whole_hanzi_exist, subStr): subStr for subStr in substrings}

        for future in concurrent.futures.as_completed(future_to_subStr):
            subStr = future_to_subStr[future]
            try:
                exists, hanziReq = future.result()
                if exists:
                    subStrOrderedDict[subStr] = None  # Using OrderedDict to maintain order
                    dic[subStr] = hanziReq
            except Exception as e:
                print(f"Error processing {subStr}: {e}")

    return list(subStrOrderedDict.keys()), dic
def does_whole_hanzi_exist(char):
    url = f"https://www.pandanese.com/search?q={char}"
    # print(f"Checking if {char} exists ")
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
        return False, dic
    # print(color.GREEN + f"{char}" + "exists" + color.END)
    return True, dic
def req_format_and_print(char):
    url = f"https://www.pandanese.com/search?q={char}"
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

    if dic.get('meaning') is None:
        print(color.RED + "No results found" + color.END)
        return 0

    return format_output(char, dic)

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
parser.add_argument('-r', '--recursive', action='store_true', help='recursively looks up hanzi')
parser.add_argument('-l', '--lookup', action='store_true', help='looks up all chars')
parser.add_argument('-f', '--format', action='store_true', help='formats output as flexbox for anki cards')
# TODO: add a -s search option that searches for substrings and checks if they exist against a dictionary




args = parser.parse_args()
if args.format and args.lookup and args.recursive:    
    formattedOutput = """<div class="flex">"""
    if does_whole_hanzi_exist(args.hanzi):
        formattedOutput += """<div class="child">"""
        formattedOutput += f"""<div class="hanzi">{args.hanzi}</div> <br>"""
        formattedOutput += req_format_and_print(args.hanzi)
        formattedOutput += """</div>"""
    for char in args.hanzi:
        formattedOutput += """<div class="child">"""
        formattedOutput += f"""<div class="hanzi">{char}</div> <br>"""
        formattedOutput += req_format_and_print(char)
        formattedOutput += """</div>"""
    formattedOutput += """</div>"""
    pyperclip.copy(formattedOutput)
    print(color.BOLD + color.GREEN + "Formatted output copied to clipboard" + color.END)
elif args.format and args.recursive:
    subStrSet, dic = get_substrings(args.hanzi)
    formattedOutput = ""
    formattedOutput += """<div class="flex">"""
    seen = set()
    for hanzi in dic:
        if hanzi in seen:
            continue
        formattedOutput += """<div class="child">"""
        formattedOutput += f"""<div class="hanzi">{hanzi}</div> <br>"""
        formattedOutput += format_output(hanzi, dic[hanzi])
        formattedOutput += """</div>"""
        if len(hanzi) > 1:
            for char in hanzi:
                if char in seen: continue
                formattedOutput += """<div class="child">"""
                formattedOutput += f"""<div class="hanzi">{char}</div> <br>"""
                formattedOutput += format_output(char, dic[char])
                formattedOutput += """</div>"""
                seen.add(char)
                
        # for char in hanzi:
        #     formattedOutput += """<div class="child">"""
        #     formattedOutput += f"""<div class="hanzi">{char}</div> <br>"""
        #     if (dic[char]):
        #         formattedOutput += format_output(hanzi, dic[char])
        #     else:
        #         formattedOutput += req_format_and_print(char)
        #     formattedOutput += """</div>"""
    formattedOutput += """</div>"""
    pyperclip.copy(formattedOutput)
    print(color.BOLD + color.GREEN + "Formatted output copied to clipboard" + color.END)
elif args.format and args.lookup:
    formattedOutput = """<div class="flex">"""
    for char in args.hanzi:
        formattedOutput += """<div class="child">"""
        formattedOutput += f"""<div class="hanzi">{char}</div> <br>"""
        formattedOutput += req_format_and_print(char)
        formattedOutput += """</div>"""
    formattedOutput += """</div>"""
    pyperclip.copy(formattedOutput)
    print(color.BOLD + color.GREEN + "Formatted output copied to clipboard" + color.END)
elif args.format:    
    formattedOutput = """<div class="flex">"""
    formattedOutput += """<div class="child">"""
    formattedOutput += f"""<div class="hanzi">{args.hanzi}</div> <br>"""
    formattedOutput += req_format_and_print(args.hanzi)
    formattedOutput += """</div>"""
    pyperclip.copy(formattedOutput)
    print(color.BOLD + color.GREEN + "Formatted output copied to clipboard" + color.END)
elif args.lookup:    
    for char in args.hanzi:
        req_format_and_print(char)
elif args.recursive:
    subStrSet = get_substrings(args.hanzi)
    for subStr in subStrSet:
        req_format_and_print(subStr)
        for char in subStr:
            req_format_and_print(char)
else:    
    req_format_and_print(args.hanzi)
    




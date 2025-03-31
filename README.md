
# WaniKani Scraper & Anki Formatter

A Python script that extracts kanji, vocabulary, and radical data from [WaniKani](https://www.wanikani.com/) and formats it for Anki flashcards with clean HTML/CSS.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![demo](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExNWcxNWN3ZGt0Njc2eGMzMHRnNWtkYWtkdWxmdjU5bjk1eDBqMm03NiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/9ITOVcfMDWwpMX6owE/giphy.gif)

## Features

- **Scrapes WaniKani data** for kanji, vocabulary, and radicals
- **Recursive decomposition** of complex characters into components
- **Anki-ready HTML formatting** with responsive flexbox layout
- **Clipboard integration** for quick card creation
- **Command-line interface** with multiple options:
  - Lookup single characters or multiple at once
  - Include radical breakdowns
  - Format output for Anki

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/wanikani-scraper.git
   cd wanikani
   ```

## Usage

### Basic Commands

Look up a kanji:
```bash
./wanikani.py kanji 漢 -f
```

Look up vocabulary:
```bash
./wanikani.py vocab 日本語 -r
```

Look up radicals:
```bash
./wanikani.py radical hole
```

### Options

| Flag | Description |
|------|-------------|
| `-r` | Recursive lookup (decompose characters) |
| `-b` | Show radical breakdown |
| `-l` | Lookup every kanji in input string |
| `-f` | Format output for Anki |

## Output Example

Formatted Anki output (automatically copied to clipboard):
```html
<div class="flex">
  <div class="child">
    <div class="kanji"><b>語</b></div>
    <div><b>Radicals</b>:</div>
    <li>言: word</li>
    <li>五: five</li>
    <li>口: mouth</li>
    <div><br></div>
    <div><b>primary</b>: language</div>
    <div><b>onyomi</b>: ゴ</div>
    <div><b>kunyomi</b>: かた(る) かた(らう)</div>
  </div>
</div>
```

## Dependencies

- Python 3.8+
- BeautifulSoup4
- requests
- pyperclip

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.



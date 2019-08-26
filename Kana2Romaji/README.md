# KANA2ROMAJI
> KANA2ROMAJI is a tool to translate characters from Japanese kana(仮名) to Romaji.

## Usage
```sh
$ python3 kana2romaji.py
```

## Input & Output
* Input source could be:
    1. Text File.
    2. Console Input.
    3. Clipboard.
* Output destination could be:
    1. Console Output (Screen or tty).
    2. Clipboard.
    3. Text File.

> Note: Clipboard support need a 3rd party library "pyperclip".
> To install pyperclip, enter `pip install pyperclip` in your console.

## Requirements
* ConsoleIOTools: `pip install consoleiotools`
* pyperclip: `pip install pyperclip`

## Translation Rules
1. Any romaji from kana is followed by a space char.
2. Space before ")" is removed and a space char is added after it.
3. Katakanas(片仮名) -- such like あいうえお -- become lowercases. Hiraganas(平仮名) -- such like アイウエオ -- become UPPERCASEs.
4. Youons(拗音) -- such like りょ -- are translated before others.
5. Characters other than kanas are not touched.

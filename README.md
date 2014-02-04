猫 (neko)
===
Neko wants to be a MOO inspired roguelike. 

### Requirements
It sure doesn't work on Python3 due to the `libtcod` wrapping. It's tested on __Python 2.7__ so use that or any higher version of __Python2__ to be safe.

Only tested on Windows too. Still have to get a Vagrant setup included.

### Testing
The `tokenizer` and `match` modules have some basic unit tests. Just run the modules to test (e.g. `python .\tokenizer.py`).

### Running
Just go `python .\main.py` and that's it.

### Features
It's a console. It reads a string command from the bottom line of your screen (there is a prompt there). Then it will parse that string and display the output in a text view on top (this is the main area).
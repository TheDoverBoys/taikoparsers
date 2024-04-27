# taikoparsers - parser and viewers for the system 10 taiko games' formats

## setting it up
you only need python 3.10+ and the pyglet module  
install it like this  
```
pip install pyglet
```
to run the thing
```
python [script] [input file]
```
taiko2parser.py runs files from taiko 2  
taiko3parser.py runs files from taiko 3, 4, 5, 6 and RT, as well as the first three PS2 games + anime matsuri  
taikoCS4parser.py runs files from taiko yondaime (theoretically TDM too?)

## controls
- UP / DOWN - change measure
- LEFT / RIGHT - change beat position
- A / D - change quantization
- P - take screenshot
- ESC - quit

## changelog (taiko3parser)
### v1.113 - apr 26 2024
- tweaked line code
- added new check for unused branch areas

### v1.112 - mar 31 2024
- changed sprite sheet resolution

### v1.111 - feb 29 2024
- added small log upon entering a file

### v1.101 - aug 20 2023
- tweaked screenshot function

### v1.1 - aug 20 2023
- added quantization bars
- added screenshot function
- changed variable names
- fixed drag+drop support

### v1.0 - aug 19 2023
- initial release

## changelog (taiko2parser)
### v1.002 - apr 26 2024
- tweaked line code
- added new check for unused branch areas

### v1.001 - mar 31 2024
- changed sprite sheet resolution
- added small log upon entering a file

### v1.0 - sep 2 2023
- initial release

## changelog (taikoCS4parser)
### v1.001 - apr 27 2024
- fixed bug in unused branch area check

### v1.0 - apr 26 2024
- initial release
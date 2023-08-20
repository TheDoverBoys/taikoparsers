# taiko3parser - a parser and viewer for taiko 3's chart format
***NOTE: THIS IS LITERALLY MY FIRST PYTHON PROGRAM THIS IS UNOPTIMIZED TO HELL***
## setting it up
you only need python 3.10+ and the pyglet module  
install it like this  
```
pip install pyglet
```
to run the thing
```
python taiko3parser.py [input file]
```
the input files are charts extracted from taiko 3's data  
taiko 4, taiko 5, taiko 6 and taiko RT chart files are also compatible, as the format itself is the same

## controls
- UP / DOWN - change measure
- LEFT / RIGHT - change beat position
- A / D - change quantization
- P - take screenshot
- ESC - quit

## changelog
### v1.101 - aug 20 2023
- tweaked screenshot function

### v1.1 - aug 20 2023
- added quantization bars
- added screenshot function
- changed variable names
- fixed drag+drop support

### v1.0 - aug 19 2023
- initial release
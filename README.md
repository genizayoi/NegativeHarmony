# Mathematical NegativeHarmony
Mathematical NegativeHarmony for music generation.
```
Usage: negative.py [OPTIONS] FILE_NAME_PATH

Options:
  -r, -R, --recursive             Option to apply each listed directory.
  -c, -C, --config_section_name TEXT
                                  Config section name in
                                  config_files/setting.conf. default="DEFAULT"

  -m, -M, --mode TEXT             CLASS = [ N | N+ | N+part1 | N+part2 |
                                  prepare ] Determine the mode of the
                                  algorithm. default="N"

  -a, -A, --analyze               Option to analyze and generate romanNumeral
                                  part.

  -d, -D, --delete_analysis_part  Option to remove the analysis part in the
                                  stream.

  -e, -E, --extension TEXT        CLASS = [ mxl | xml | midi | ... ] File
                                  extension for saving. default="mxl"

  --help                          Show this message and exit.
  ```
## 1. Environment
Music21 and other Add-ons environments are required. You can install them with:  
```
pip3 install music21
pip3 install click
pip3 install tqdm
```
## 2. Get Original Pieces
You can get classical music pieces with Rome(harmony) analysis part through:  
```
git clone https://github.com/sohoelf/When-in-Rome
```
I organized music pieces in the ```When-in-Rome/analysis_on_score_pieces``` folder.  
If you want to apply this modeling to music pieces that doesn't have Rome analysis part,  
you also can use the ```--analyze``` option. (I will introduce it in the next chapter.)  
## 3. Generate Negative Music Pieces
Usage: 
```
python3 negative.py [OPTIONS] <FILE_NAME_PATH>
```
*****
For example, when you want to get **N+** (NegativeHarmony with N+ mode) piece of **one** music piece:
```
python3 negative.py -m N+ ~/When-in-Rome/analysis_on_score_pieces/analysis_on_score_092.mxl
``` 
Get **N+** pieces of **all music pieces in** ```analysis_on_score_pieces``` **folder** with ```-r``` option:
```
python3 negative.py -r -m N+ ~/When-in-Rome/analysis_on_score_pieces
``` 
*****
If you want to apply N+ modeling to music pieces that doesn't have Rome analysis part,  
use```-a```option **to generate rome part** (in N+/N+part1/N+part2 modeling, rome analysis part is required):  
```
python3 negative.py -m N+ ~/music_piece_without_rome_part -a
``` 
Or give up N+ modeling and use N modeling (rome analysis part not required in N modeling):  
```
python3 negative.py -m N ~/music_piece_without_rome_part
```
*****
Specify the extension of generated file with ```-e``` option (default is mxl):  
```
python3 negative.py -m N+ ~/music_piece -e midi
``` 
*****
Use the ```-d``` option to remove the Rome analysis part immediately before output:  
```
python3 negative.py -m N+ ~/music_piece -e midi -d
``` 
## 4. Actual Example
```
cd ~
git clone https://github.com/sohoelf/NegativeHarmony
git clone https://github.com/sohoelf/When-in-Rome
pip3 install music21
pip3 install click
pip3 install tqdm
cd NegativeHarmony
vi config_files/setting.conf
``` 
(Change 3rd line ```save_path = /negative_pieces``` to ```save_path = /negative_pieces_N_PLUS```.)
```
python3 negative.py -r -m N+ ~/When-in-Rome/analysis_on_score_pieces
vi config_files/setting.conf
```
(Change 3rd line ```save_path = /negative_pieces``` to ```save_path = /negative_pieces_N_PLUS_PART1```.)
```
python3 negative.py -r -m N+part1 ~/When-in-Rome/analysis_on_score_pieces -d
cd ~/When-in-Roma/negative_pieces_N_PLUS
ls
cd ~/When-in-Roma/negative_pieces_N_PLUS_PART1
ls
```

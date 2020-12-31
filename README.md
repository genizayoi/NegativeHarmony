# NegativeHarmony
NegativeHarmony theory for music generation

```
Usage: negative.py [OPTIONS] FILE_NAME_PATH

Options:
  -r, -R, --recursive             Option to apply each listed directory.
  -m, -M, --mode TEXT             CLASS = [ N | N+ | N+part1 | N+part2 |
                                  prepare ] Determine the mode of the
                                  algorithm. default="N"

  -c, -C, --config_section_name TEXT
                                  Config section name in
                                  config_files/setting.conf. default="DEFAULT"

  -e, -E, --extension TEXT        CLASS = [ mxl | xml | midi | ... ] File
                                  extension for saving. default="mxl"

  --help                          Show this message and exit.
  ```
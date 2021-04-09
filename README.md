# Tagalog

This repository contains utility code to process labeled text data from the Tagalog labeling software, and shows 
how this data can be used to train NLP models.

## Data processing

- `scripts/json2conll.py`converts a Tagalog JSON file to a CONLL-type file, where every line contains a token and 
  its label, separated by a tab. Takes the path to the Tagalog JSON file as its only argument, and produces a file 
  with the same name and path, but with the extension `.conll`.

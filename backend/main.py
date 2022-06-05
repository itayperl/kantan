from radical_dawg import RadicalDawg
from dict_dawg import DictDawg

from flask import Flask, jsonify
from flask_cors import CORS

import romkan

import json
import functools
import codecs
import argparse
import re
import pathlib

PATTERN_RE = re.compile(r'\[[^\[\]]*\]|.')
DATA_DIR = pathlib.Path(__file__).parent

MAX_RESULTS = 50

app = Flask('kantan')
CORS(app)


print('Creating in-memory database (may take up to 30 seconds)...', end=' ') 

with open(DATA_DIR / 'kradfile-u', 'r') as f:
    rad_dawg = RadicalDawg.from_kradfile(f)

with open(DATA_DIR / 'JMdict_e', 'r') as jmdict:
    dict_dawg = DictDawg.from_jmdict(jmdict)

print('Done!')


@app.get('/')
@app.get('/<pattern>')
def lookup(pattern=''):
    components = []

    # sanity
    if len(pattern) > 40 and pattern.count('[') > 20:
        return jsonify([])

    # romaji => kana
    pattern = re.sub('[-A-Z]+', lambda m: romkan.to_katakana(m.group(0)), pattern)
    pattern = re.sub('[-a-z]+', lambda m: romkan.to_hiragana(m.group(0)), pattern)

    for c in PATTERN_RE.findall(pattern):
        if c[0] == '[' and c[-1] == ']':
            s = rad_dawg.lookup_kanji(''.join(c[1:-1]))
            components.append(s)
        else:
            components.append(set([c]))

    return jsonify(dict_dawg.lookup_word(components)[:MAX_RESULTS])


if __name__ == '__main__':
    main()

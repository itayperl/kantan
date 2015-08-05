from radical_dawg import RadicalDawg
from dict_dawg import DictDawg

from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
import romkan

import json
import functools
import codecs
import argparse
import re

PATTERN_RE = re.compile(r'\[[^\[\]]*\]|.')

MAX_RESULTS = 50

def lookup(rad_dawg, dict_dawg, pattern):
    components = []

    # sanity
    if len(pattern) > 40 and pattern.count('[') > 20:
        return []

    # romaji => kana
    pattern = re.sub('[-A-Z]+', lambda m: romkan.to_katakana(m.group(0)), pattern)
    pattern = re.sub('[-a-z]+', lambda m: romkan.to_hiragana(m.group(0)), pattern)

    for c in PATTERN_RE.findall(pattern):
        if c[0] == '[' and c[-1] == ']':
            s = rad_dawg.lookup_kanji(u''.join(c[1:-1]))
            components.append(s)
        else:
            components.append(set([c]))

    return dict_dawg.lookup_word(components)[:MAX_RESULTS]

def json_service(host, port, handler):

    @Request.application
    def service(request):
        data = handler(request.path[1:])

        response = Response(json.dumps(data), mimetype='application/json')

        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'GET')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')

        return response

    run_simple(host, port, service)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=4000)
    args = parser.parse_args()

    print 'Creating in-memory database (may take up to 30 seconds)...', 

    with codecs.open('kradfile-u', 'r', 'utf-8') as f:
        rad_dawg = RadicalDawg.from_kradfile(f)

    with codecs.open('JMdict_e', 'r', 'utf-8') as jmdict:
        dict_dawg = DictDawg.from_jmdict(jmdict)

    print 'Done!'

    json_service('0.0.0.0', args.port, functools.partial(lookup, rad_dawg, dict_dawg))

if __name__ == '__main__':
    main()

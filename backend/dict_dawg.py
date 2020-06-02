# coding:utf-8
from dawg import Dawg
import re
from collections import defaultdict
import romkan

HIRAGANA = set(''.join(list(romkan.KANROM_H.keys())))

class DictDawg(Dawg):

    @staticmethod
    def ke_pri_order(pri):
        if any(x in pri for x in ('news1', 'ichi1', 'spec1', 'gai1')):
            nf_seq = None

            for p in pri:
                m = re.match('nf(\d\d)', p)
                if m:
                    nf_seq = int(m.group(1))
                    break
            
            if nf_seq:
                return nf_seq
            else:
                # word with no 'nfxx' rating
                return 100

        elif any(x in pri for x in ('news2', 'ichi2', 'spec2', 'gai2')):
            return 200
        else:
            return 300

    @staticmethod
    def from_jmdict(fp):
        current_keb = None
        pris = set()
        keb_to_pri = defaultdict(lambda: 10000)
        max_len = 0

        for line in fp:
            if current_keb is not None:
                # look for ke_pri
                if line.startswith('<ke_pri>'):
                    pris.add(line.replace('<ke_pri>','').replace('</ke_pri>','').strip())
                else:
                    keb_to_pri[current_keb] = min(keb_to_pri[current_keb], DictDawg.ke_pri_order(pris))
                    current_keb = None
            else:
                if line.startswith('<keb>'):
                    current_keb = line.replace('<keb>','').replace('</keb>','').strip()
                    max_len = max(max_len, len(current_keb))
                    pris = set()

        dawg = DictDawg()
        for keb, pri in sorted(keb_to_pri.items()):
            dawg.insert(keb, (keb, keb_to_pri[keb]))
        dawg.finish()

        return dawg

    # word is a list of sets of kanjis
    def lookup_word(self, word):
        results = []

        def dfs(node, word, count, wildcard = False):

            def child_count():
                if node.final:
                    return count + 1
                else:
                    return count

            if node.final and len(word) == 0:
                results.append(self.data[count])

            if len(word) == 0 and not wildcard:
                return

            for label, child in node.edges.items():
                if wildcard and label in HIRAGANA:
                    dfs(child, word, child_count(), wildcard)
                elif len(word) > 0:
                    if ('+' in word[0] or '＋' in word[0]) and label in HIRAGANA:
                        dfs(child, word[1:], child_count(), True)
                    elif label in word[0] or (('.' in word[0] or '。' in word[0]) and label in HIRAGANA):
                        dfs(child, word[1:], child_count(), False)

                count += child.count

        dfs(self.root, word, 0)

        # sort by priority
        return [ x[0] for x in sorted(results, key=lambda x_y: x_y[1]) ]

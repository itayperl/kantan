from dawg import Dawg
import re
from collections import defaultdict

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
                if line.startswith(u'<ke_pri>'):
                    pris.add(line.replace(u'<ke_pri>',u'').replace(u'</ke_pri>',u'').strip())
                else:
                    keb_to_pri[current_keb] = min(keb_to_pri[current_keb], DictDawg.ke_pri_order(pris))
                    current_keb = None
            else:
                if line.startswith(u'<keb>'):
                    current_keb = line.replace(u'<keb>',u'').replace(u'</keb>',u'').strip()
                    max_len = max(max_len, len(current_keb))
                    pris = set()

        dawg = DictDawg()
        for keb, pri in sorted(keb_to_pri.iteritems()):
            dawg.insert(keb, (keb, keb_to_pri[keb]))
        dawg.finish()

        return dawg

    # word is a list of sets of kanjis
    def lookup_word(self, word):
        results = []

        def dfs(node, word, count):
            if len(word) == 0:
                if node.final:
                    results.append(self.data[count])
                return

            for label, child in node.edges.iteritems():
                if label in word[0]:
                    if node.final:
                        child_count = count + 1
                    else:
                        child_count = count

                    dfs(child, word[1:], child_count)

                count += child.count

        dfs(self.root, word, 0)

        # sort by priority
        return [ x[0] for x in sorted(results, key=lambda (x,y): y) ]

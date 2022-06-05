# coding:utf-8
from dawg import Dawg
from collections import defaultdict

RADICALS = (
     '一｜丶ノ乙亅' +
     '二亠人⺅𠆢儿入ハ丷冂冖冫几凵刀刂力勹匕匚十卜卩厂厶又マ九ユ乃' +
     '辶口囗土士夂夕大女子宀寸小⺌尢尸屮山川巛工已巾干幺广廴廾弋弓ヨ彑彡彳忄扌氵犭⺾⻏⻖也亡及久' +
     '⺹心戈戸手支攵文斗斤方无日曰月木欠止歹殳比毛氏气水火灬爪父爻爿片牛犬礻王元井勿尤五屯巴毋' +
     '玄瓦甘生用田疋疒癶白皮皿目矛矢石示禸禾穴立衤世巨冊母罒牙' +
     '瓜竹米糸缶羊羽而耒耳聿肉自至臼舌舟艮色虍虫血行衣西' +
     '臣見角言谷豆豕豸貝赤走足身車辛辰酉釆里舛麦' +
     '金長門隶隹雨青非奄岡免斉' +
     '面革韭音頁風飛食首香品' +
     '馬骨高髟鬥鬯鬲鬼竜韋' +
     '魚鳥鹵鹿麻亀啇黄黒' +
     '黍黹無歯' +
     '黽鼎鼓鼠' +
     '鼻齊' +
     '龠'
)

# radicals represented by a different character in kradfile-u
KRADFILE_RAD_MAP = {
    '并': '丷',
    '滴': '啇',
}

class RadicalDawg(Dawg):

    def __init__(self, sort_key=None):
        super(type(self), self).__init__()

        self._sort_key = sort_key

    @staticmethod
    def from_kradfile(fp):
        rad_frequencies = defaultdict(lambda: 0)
        kanji_to_rads = {}

        for line in fp:
            if line.startswith('#'):
                continue

            k, rads = line.strip().split(' : ')

            kanji_to_rads[k] = set(rads.replace(' ', '')) & set(RADICALS)

            for alt_rad, real_rad in KRADFILE_RAD_MAP.items():
                if alt_rad in rads:
                    kanji_to_rads[k].add(real_rad)

            for ch in kanji_to_rads[k]:
                rad_frequencies[ch] += 1

        # sort in ascending frequency
        ordered_rads = sorted(RADICALS, key=lambda x: rad_frequencies[x])
        rad_to_index = dict((r, ordered_rads.index(r)) for r in ordered_rads)
        rad_sort_key = lambda x: rad_to_index[x]

        # map ordered string of radicals to set of kanjis
        rad_strings = defaultdict(lambda: set())
        for k, rads in kanji_to_rads.items():
            rad_strings[''.join(sorted(rads, key=rad_sort_key))].add(k)

        # build the DAWG
        dawg = RadicalDawg(sort_key=rad_sort_key)
        for rad_str, kanjis in sorted(iter(rad_strings.items()), key=lambda x_y: tuple(map(rad_sort_key, x_y[0]))):
            dawg.insert(rad_str, kanjis)
        dawg.finish()

        return dawg

    def lookup_kanji(self, radicals):
        results = set()

        def dfs(node, radicals, count):
            if len(radicals) == 0 and node.final:
                # all radicals seen - add all of the kanji on this branch
                results.update(self.data[count])

            for label, child in node.edges.items():
                if len(radicals) > 0 and label == radicals[0]:
                    # found another radical
                    child_radicals = radicals[1:]
                else:
                    child_radicals = radicals
                
                if node.final:
                    child_count = count + 1
                else:
                    child_count = count

                dfs(child, child_radicals, child_count)

                count += child.count

        dfs(self.root, ''.join(sorted(radicals, key=self._sort_key)), 0)

        return results

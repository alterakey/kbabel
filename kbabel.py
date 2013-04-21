# -*- coding: utf-8 -*-
# akk.py: Automatic Kana-to-Kanji conversion
from __future__ import with_statement
import re
import sys
from kanadb import table

re_table = []

normalize_re = {
    u'a':u'あ', u'i':u'い', u'u':u'う', u'e':u'え', u'o':u'お',
    u'k':u'[かきくけこ]',
    u'g':u'[がぎぐげご]',
    u's':u'[さしすせそ]',
    u'z':u'[ざじずぜぞ]',
    u'j':u'じ',
    u't':u'[たちつてと]',
    u'd':u'[だぢづでど]',
    u'n':u'[なにぬねの]',
    u'h':u'[はひふへほ]',
    u'b':u'[ばびぶべぼ]',
    u'p':u'[ぱぴぷぺぽ]',
    u'm':u'[まみむめも]',
    u'y':u'[やゆよ]',
    u'r':u'[らりるれろ]',
    u'w':u'[わをん]',
    u'/':u'・',
    u'T':u'っ',
    u'c':u'(ちゃ|ちゅ|ちょ)'
}

for t,v in table.iteritems():
    patlen = 0
    try:
        body, suffix = t[:-1], t[-1]
        t = '%s(%s)' % (body, normalize_re[suffix])
        v = r'%s\1' % v
        patlen = (suffix == 'c' and 2 or 1)
    except KeyError:
        body = t
        # Boost priority for non-suffixed bodies (#463)
        patlen = 0.5

    patlen += len(body)

    re_table.append((patlen, re.compile(t), t, v))

re_table.sort(key=lambda(v): v[0], reverse=True)

for t in re_table:
    patlen, pattern, repl = t[0], t[2], t[3]
    if repl != u'':
        sys.stderr.write((u'%u: %s -> %s\n' % (patlen, pattern, repl or u'(preserve)')).encode('UTF-8'))

re_target = re.compile('.*')
re_repl = re.compile('\|(\d+)\|');

class SimpleKanji(object):
    def __init__(self, key, kanji):
        self.key = key
        self.kanji = kanji

    def get(self):
        return u'%s' % (self.kanji)

for l in sys.stdin:
    l = unicode(l, 'utf-8')
    o = l
    queue = []
    if re_target.match(l):
        for r in re_table:
            def mark(m):
                key = m.group(0)
                if r[3]:
                    kanji = r[1].sub(r[3], key)
                else:
                    kanji = key
                queue.append([SimpleKanji(key, kanji).get()])
                return '|%u|' % (len(queue) - 1)
            o = r[1].sub(mark, o)

        def repl(m):
            return queue[int(m.group(1))][0]
        o = re_repl.sub(repl, o)
    sys.stdout.write(o.encode('utf-8'))

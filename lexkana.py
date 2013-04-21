# -*- coding: utf-8 -*-
# lexkana.py: Kana lexer
# Copyright (C) 2013  Takahiro Yoshimura <altakey@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import with_statement
import re
import unicodedata
import sys
from kanadb import table

re_exclude = re.compile(u'\s//\s')

filenames = sys.argv[1:]
if len(filenames) == 0:
    print "usage: %s <hiragana plain text file> ... " % sys.argv[0]
    sys.exit(1)

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

for key, value in table.items():
    if value == u'':
        del table[key]

for t,v in table.iteritems():
    patlen = 0
    try:
        body, suffix = t[:-1], t[-1]
        t = '(%s)(%s)' % (body, normalize_re[suffix])
        patlen = (suffix == 'c' and 2 or 1)
    except KeyError:
        body = t
        # Boost priority for non-suffixed bodies (#463)
        patlen = 0.5

    patlen += len(body)

    re_table.append((patlen, re.compile(t), t, v))

re_table.sort(key=lambda(v): v[0], reverse=True)

for fn in filenames:
    with open(fn, 'rb') as f:
        print "lexing %s" % fn
        for l in (unicode(l, 'utf-8') for l in f):
            if re_exclude.search(l):
                continue
            for r in re_table:
                l = r[1].sub(u'*', l)
            run = []
            for u in l:
                try:
                    name = unicodedata.name(u)
                    if 'KATAKANA' in name or 'HIRAGANA' in name:
                        run.append(u)
                        continue
                except ValueError:
                    pass
                if len(run) > 0:
                    k = ''.join(run)
                    if k not in table:
                        table[k] = ''
                    run = []

keys = [x for x in table]

re_re = re.compile('^\[');

def key_len(s):
    o = len(s)
    if re_re.match(s):
        o = 1
    return o

keys.sort()
keys.sort(key=key_len, reverse=True)

with open('kanadb.py', 'wb') as f:
    f.write("""\
# -*- coding: utf-8 -*-

table = {
""")
    for e in keys:
        f.write("""\
    u'%s':%s,
""" % (e.encode('utf-8'), table[e] is None and 'None' or ("u'%s'" % table[e].encode('utf-8'))))
    f.write("""\
}
""")

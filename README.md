kbabel: Automatic Kana-Kanji Conversion Core
=============================================

Copyright (C) 2013 Takahiro Yoshimura <altakey@gmail.com>.  All rights reserved.

0. USAGE
=========

    $ cat test/corpse.txt

    わがはいはねこである。なまえはまだない。

    　どこでうまれたかとんとけんとうがつかぬ。なんでもうすぐらいじめじ
    めしたところでニャーニャーないていたことだけはきおくしている。わが
    はいはここではじめてにんげんというものをみた。しかもあとできくとそ
    れはしょせいというにんげんのなかでいちばんどうあくなしゅぞくであっ
    たそうだ。このしょせいというのはときどきわれわれをつかまえてにてく
    うというはなしである。....

    $ cp test/kanadb.py .
    $ python ./kbabel.py < test/corpse.txt
    ....
    吾輩は猫である。名前はまだない。

    　どこで生れたかとんと見当がつかぬ。何でも薄暗いじめじめした所で
    ニャーニャー泣いていたことだけは記憶している。吾輩はここではじめて
    人間と云う者をみた。しかも後で聞くとそれは書生という人間の中で一番
    獰悪な種族であったそうだ。この書生というのは時々我々を捕えて煮て食
    うという話である。...

    $ cat kanadb.py

    # -*- coding: utf-8 -*-

    table = {
	u'いっこくのゆうよ':u'一刻の猶予',
	u'いっそうらんぼう':u'一層乱暴',
	u'やどなしのこねこ':u'宿なしの子猫',
	u'かおのまんなか':u'顔の真中',...


1. USE CASES
============

 * Speedily logging meeting in hiragana-only mode, translate it later

You name it :-)

2. BUGS
========

 * Creating kanadb.py tend to be tedious, esp. for the first time.
 * Extremely hackish.
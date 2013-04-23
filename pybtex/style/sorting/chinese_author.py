# -*- coding: utf-8 -*-
# Copyright (c) 2006, 2007, 2008, 2009, 2010, 2011, 2012  Andrey Golovizin
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from pybtex.style.sorting import BaseSortingStyle
import pinyin
import re
import os,sys
wordfile = re.sub(r"[^/\\]*$", "word.data", __file__)
if not os.path.exists(wordfile):
    wordfile = re.sub(r"[^/\\]*$", "word.data", os.path.abspath(sys.argv[0]))
if not os.path.exists(wordfile):
    wordfile = "word.data"
#print "Data File: " + os.path.abspath(wordfile)
pymod = pinyin.PinYin(wordfile)
pymod.load_word()


class SortingStyle(BaseSortingStyle):
    name = 'chinese_author'

    def sorting_key(self, entry):
        if entry.type in ('book', 'inbook'):
            author_key = self.author_editor_key(entry)
        else:
            author_key = self.persons_key(entry.persons['author'])
        return (author_key, entry.fields.get('year', ''), entry.fields.get('title', ''))

    def persons_key(self, persons):
        return '   '.join(self.person_key(person) for person in persons)

    def isansi(selft, string):
        for ch in string:
            if ord(ch) >= 256:
                return False
        return True

    def hanzi2pinyin(self, hanzi):
        assert(len(hanzi) == 1)
        #print "xxxx", pymod.hanzi2pinyin("段")
        py = pymod.hanzi2pinyin(hanzi)[0]
        assert(len(py) >= 2 and len(py) <= 6)
        # 每一个汉字对应一个7位字符串, 其中6位为拼音, 少于6位则左对齐, 以空格填充;
        # 第7位为数字, 表示汉字的音调
        # 前面加入zz表示排到所有英文的最后面
        word = "zz" + py[0:-1].ljust(6) + py[-1]
        return unicode(word)

    def proc_hanzi(self, string):
        py = u""
        for ch in string:
            if ord(ch) >= 256:
                py += self.hanzi2pinyin(ch)
            else:
                py += ch
        return py

    def proc_accent(self, name):
        # ref. lshort p.22
        # first delete accent with two chars
        acname = name
        pat = r"""\\`|\\\'|\\^|\\~|\\=|\\.|\\\"|\\c |\\u |\\v |\\H |\\d |\\b |\\t """
        acname = re.sub(unicode(pat), u"", acname)
        # delete two consecutive chars
        #acname = acname.replace("\\oe", "oe")
        #acname = acname.replace("\\OE", "OE")
        #acname = acname.replace("\\ae", "ae")
        #acname = acname.replace("\\AE", "AE")
        acname = acname.replace(u"\\aa", u"a")
        # delete singe char
        acname = acname.replace(u"\\", u"")
        # delete {}
        acname = re.sub(u"[{}]", u"", acname);
        # something more
        return acname

    def person_key(self, person):
        name = '  '.join((
            ' '.join(person.prelast() + person.last()),
            ' '.join(person.first() + person.middle()),
            ' '.join(person.lineage()),
        )).lower()

        name = unicode(name)
        # process the accent
        acname = self.proc_accent(name)
        # process chinese character
        hanname = self.proc_hanzi(acname)
        #print (name + "---" + acname + u"---" + hanname).encode('utf-8')
        return hanname

    def author_editor_key(self, entry):
        if entry.persons.get('author'):
            return self.persons_key(entry.persons['author'])
        elif entry.persons.get('editor'):
            return self.persons_key(entry.persons['editor'])

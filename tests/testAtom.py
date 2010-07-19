# (C) Copyright 2003-2005 Nuxeo SARL <http://nuxeo.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.

import unittest
from testBlog import TestBlog
from lxml import etree
from StringIO import StringIO

BLOGGER_POST_REQUEST = """\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<entry xmlns="http://purl.org/atom/ns#">
  <title mode="escaped" type="text/plain">atom test</title>
  <issued>2004-04-12T06:07:20Z</issued>
  <generator url="http://www.yoursitesurlhere.com">Your client's name here.</generator>
  <content type="application/xhtml+xml">
    <div xmlns="http://www.w3.org/1999/xhtml">Testing the Atom API</div>
  </content>
</entry>
"""
TYPEPAD_POST_REQUEST = """\
<?xml version="1.0" encoding="utf-8"?>
<entry xmlns="http://purl.org/atom/ns#" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <title>Trip to the Lake</title>
  <dc:subject>Vacation</dc:subject>
  <content type="application/xhtml+xml" mode="xml"><div xmlns="http://www.w3.org/1999/xhtml"><img src="http://example.typepad.com/photos/vacation/lake-thumb.jpg" /> Here is a picture of me at the lake.</div></content>
</entry>
"""

class TestAtom(TestBlog):

    def testAtomPost(self):
        doc = self._createBlog()
        proxy = self.ws.blog

        request = self.portal.REQUEST
        request.PARENTS = [proxy]
        request.BODY = BLOGGER_POST_REQUEST
        doc.atomPost(request)

    def testBlogAtomExport(self):
        self._createBlog()
        blog = self.ws.blog
        doc = blog.getContent()

        TITLE = u"Blog d'Arnaud Lef\xe8vre"
        doc.edit(**{"Title": TITLE})
        atom = blog.exportatom()
        # XXX: we need StringIO because of a bug in lxml
        entry_element = etree.parse(StringIO(atom))
        title = entry_element.xpath("/atom:feed/atom:title/text()",
            namespaces={'atom': 'http://purl.org/atom/ns#'})[0]
        self.assertEquals(TITLE.encode('utf-8'), title)

    def testBlogEntryAtomExport(self):
        self._createBlog()
        blog = self.ws.blog
        blog.invokeFactory(type_name='BlogEntry', id='blogentry')
        entry = blog.blogentry
        self.assert_(entry.exportatom())

        TITLE = u"Entr\xe9e du blog d'Arnaud Lef\xe8vre"
        entry.getContent().edit(**{"Title": TITLE})
        atom = entry.exportatom()
        # XXX: we need StringIO because of a bug in lxml
        entry_element = etree.parse(StringIO(atom))
        title = entry_element.xpath("/atom:entry/atom:title/text()",
            namespaces={'atom': 'http://purl.org/atom/ns#'})[0]
        self.assertEquals(TITLE.encode('utf-8'), title)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(TestAtom),
        ))

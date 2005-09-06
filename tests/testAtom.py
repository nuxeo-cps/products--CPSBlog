# $Id: testBlog.py 25357 2005-08-01 20:10:23Z fguillaume $

import unittest
from testBlog import TestBlog

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

    def testAtomExport(self):
        doc = self._createBlog()
        proxy = self.ws.blog
        doc = proxy.getContent()
        # There is a problem in the live site with non-ascii characters in
        # blog titles, but the test doesn't catch it.
        doc.edit(**{"Title": "Blog d'Arnaud Lefèvre"})
        self.assert_(proxy.exportatom())


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(TestAtom),
        ))

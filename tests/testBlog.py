# $Id$

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
import CPSBlogTestCase


class TestBlog(CPSBlogTestCase.CPSBlogTestCase):

    def afterSetUp(self):
        self.doc_type = 'Blog'
        self.doc_id = self.doc_type.lower()
        self.login('manager')
        self.ws = self.portal.workspaces


    def beforeTearDown(self):
        self.logout()


    def _createBlog(self):
        self.ws.invokeFactory(type_name = self.doc_type,
                              id = self.doc_id)
        return getattr(self.ws, self.doc_id).getContent()


    def testAddBlog(self):
        """Test creation of Blog instance in root of workspaces.
        """
        self.assertEqual(len([o for o in self.ws.contentValues()
                              if o.getContent().meta_type == self.doc_type]), 0)
        self.ws.invokeFactory(type_name = self.doc_type,
                              id = self.doc_id)
        self.assertEqual(len([o for o in self.ws.contentValues()
                              if o.getContent().meta_type == self.doc_type]), 1)
        self.assert_(hasattr(self.ws, self.doc_id))

        doc = getattr(self.ws, self.doc_id).getContent()
        self.assertEqual(doc.title, '')


    def testRemoveBlog(self):
        """Test removal of Blog instance in root of workspaces.
        """
        doc = self._createBlog()
        self.assertEqual(len([o for o in self.ws.contentValues()
                              if o.getContent().meta_type == self.doc_type]), 1)
        self.ws._delObject(self.doc_id)
        self.assertEqual(len([o for o in self.ws.contentValues()
                              if o.getContent().meta_type == self.doc_type]), 0)
        self.failIf(hasattr(self.ws, self.doc_id))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBlog))
    return suite

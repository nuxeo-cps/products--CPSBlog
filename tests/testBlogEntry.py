# $Id$

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
import CPSBlogTestCase


class TestBlogEntry(CPSBlogTestCase.CPSBlogTestCase):

    def afterSetUp(self):
        self.doc_type = 'BlogEntry'
        self.doc_id = self.doc_type.lower()
        self.login('manager')
        self.ws = self.portal.workspaces


    def beforeTearDown(self):
        self.logout()


    def _createBlog(self):
        self.ws.invokeFactory(type_name='Blog', id='blog')
        return getattr(self.ws, 'blog').getContent()


    def testAddBlogEntry(self):
        """Test creation of BlogEntry instance.
        """
        blog = self._createBlog()

        self.assertEqual(len(blog.objectIds()), 0)
        blog.invokeFactory(type_name=self.doc_type, id=self.doc_id)
        self.assertEqual(len(blog.objectIds()), 1)

        self.assert_(hasattr(blog, self.doc_id))

        blogentry = getattr(blog, self.doc_id).getContent()

        self.assertEqual(blogentry.meta_type, self.doc_type)
        self.assertEqual(blogentry.title, '')


    def testRemoveBlogEntry(self):
        """Test removal of BlogEntry instance.
        """
        blog = self._createBlog()
        blog.invokeFactory(type_name=self.doc_type, id=self.doc_id)
        self.assertEqual(len(blog.objectIds()), 1)

        blog._delObject(self.doc_id)

        self.assertEqual(len(blog.objectIds()), 0)
        self.failIf(hasattr(blog, self.doc_id))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBlogEntry))
    return suite

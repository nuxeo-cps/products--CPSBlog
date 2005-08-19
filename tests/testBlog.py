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
        self.ws.invokeFactory(type_name=self.doc_type, id=self.doc_id)
        return getattr(self.ws, self.doc_id).getContent()

    def testAddBlog(self):
        # Test creation of Blog instance in root of workspaces.
        self.assertEqual(len([o for o in self.ws.contentValues()
                              if o.getContent().meta_type == self.doc_type]), 0)

        doc = self._createBlog()

        self.assertEqual(len([o for o in self.ws.contentValues()
                              if o.getContent().meta_type == self.doc_type]), 1)
        self.assertEqual(doc.title, '')


    def testRemoveBlog(self):
        # Test removal of Blog instance in root of workspaces.
        doc = self._createBlog()
        self.assertEqual(len([o for o in self.ws.contentValues()
                              if o.getContent().meta_type == self.doc_type]), 1)
        self.ws._delObject(self.doc_id)
        self.assertEqual(len([o for o in self.ws.contentValues()
                              if o.getContent().meta_type == self.doc_type]), 0)
        self.failIf(hasattr(self.ws, self.doc_id))


class TestBlogCategories(CPSBlogTestCase.CPSBlogTestCase):

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

    def testAddCategory(self):
        blog = self._createBlog()

        self.assertEqual(len(blog.categories), 0)

        catdef = {'title': 'Title',
                  'description': 'Description',
                  'urls_to_ping': ('http://nuxeo.com',),
                  'accept_pings': True,
                 }
        catid = blog.addCategory(**catdef)

        self.assertEqual(len(blog.categories), 1)
        self.assert_(blog.categories.has_key(catid))

        for k in catdef.keys():
            self.assertEqual(blog.categories[catid][k], catdef[k])


    def testRemoveCategory(self):
        blog = self._createBlog()

        catdef = {'title': 'Title',
                  'description': 'Description',
                  'urls_to_ping': ('http://nuxeo.com',),
                  'accept_pings': True,
                 }
        catid = blog.addCategory(**catdef)

        blog.removeCategory(catid)
        self.assertEqual(len(blog.categories), 0)

    def testGetCategory(self):
        blog = self._createBlog()

        catdef = {'title': 'Title',
                  'description': 'Description',
                  'urls_to_ping': ('http://nuxeo.com',),
                  'accept_pings': True,
                 }

        catid = blog.addCategory(**catdef)

        for k in catdef.keys():
            self.assertEqual(blog.categories[catid][k], catdef[k])
        self.assertEqual(blog.getCategory(catid+1), None)

    def testGetSortedCategories(self):
        blog = self._createBlog()

        ids = [23, 45, 12, 32, 89, 76, 54, 43, 44, 31]
        catdef = {'title': 'Title',
                  'description': 'Description',
                  'urls_to_ping': ('http://nuxeo.com',),
                  'accept_pings': True,
                 }
        for i in ids:
            category = catdef.copy()
            category['title'] = str(i)
            catid = blog.addCategory(**category)

        sorted_cats = [int(cat['title']) for cat in blog.getSortedCategories()]
        ids.sort()
        self.assertEqual(sorted_cats, ids)

    def testUpdateCategory(self):
        blog = self._createBlog()

        self.assertEqual(len(blog.categories), 0)

        catdef = {'title': 'Title',
                  'description': 'Description',
                  'urls_to_ping': ('http://nuxeo.com',),
                  'accept_pings': True,
                 }
        catid = blog.addCategory(**catdef)

        category = {'title': 'update',
                    'description': 'update',
                    'urls_to_ping': ('http://indesko.com',),
                    'accept_pings': False,
                   }
        blog.updateCategory(catid, category)

        for k in category.keys():
            self.assertEqual(blog.categories[catid][k], category[k])

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(TestBlog),
        unittest.makeSuite(TestBlogCategories),
        ))

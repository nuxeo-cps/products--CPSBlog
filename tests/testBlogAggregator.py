# $Id: testBlog.py 26028 2005-08-19 16:15:09Z sfermigier $

import unittest
import CPSBlogTestCase

class TestBlogAggregator(CPSBlogTestCase.CPSBlogTestCase):

    def afterSetUp(self):
        self.doc_type = 'BlogAggregator'
        self.doc_id = self.doc_type.lower()
        self.login('manager')
        self.ws = self.portal.workspaces

    def beforeTearDown(self):
        self.logout()

    def _createBlogAggregator(self):
        self.ws.invokeFactory(type_name=self.doc_type, id=self.doc_id)
        return getattr(self.ws, self.doc_id).getContent()

    def testAddBlogAggregator(self):
        self.assertEqual(len([o for o in self.ws.contentValues()
                              if o.getContent().meta_type == self.doc_type]), 0)

        doc = self._createBlogAggregator()

        self.assertEqual(len([o for o in self.ws.contentValues()
                              if o.getContent().meta_type == self.doc_type]), 1)
        self.assertEqual(doc.title, '')

    def testRemoveBlogAggregator(self):
        # Test removal of Blog instance in root of workspaces.
        doc = self._createBlogAggregator()
        self.assertEqual(len([o for o in self.ws.contentValues()
                              if o.getContent().meta_type == self.doc_type]), 1)
        self.ws._delObject(self.doc_id)
        self.assertEqual(len([o for o in self.ws.contentValues()
                              if o.getContent().meta_type == self.doc_type]), 0)
        self.failIf(hasattr(self.ws, self.doc_id))

    def testBuildQuery(self):
        doc = self._createBlogAggregator()
        query = doc._buildQuery()
        self.assertEquals(query, {'portal_type': 'BlogEntry'})

    def testGetSearchResults(self):
        doc = self._createBlogAggregator()
        proxy = getattr(self.ws, self.doc_id)
        self.assertEquals(doc.getSearchResults(proxy), [])

def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(TestBlogAggregator),
        ))

# $Id$

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
import CPSBlogTestCase


class TestBlogEntryCreation(CPSBlogTestCase.CPSBlogTestCase):

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


class TestBlogEntry(CPSBlogTestCase.CPSBlogTestCase):

    def afterSetUp(self):
        self.doc_type = 'BlogEntry'
        self.doc_id = self.doc_type.lower()
        self.login('manager')
        self.ws = self.portal.workspaces
        self.ws.invokeFactory(type_name='Blog', id='blog')
        self.ws.blog.invokeFactory(type_name=self.doc_type, id=self.doc_id)
        self.bentry = getattr(self.ws.blog, self.doc_id).getContent()

    def beforeTearDown(self):
        self.logout()

    def testAddTrackback(self):
        bentry = self.bentry

        self.assertEqual(len(bentry.trackbacks), 0)

        tb_id = bentry.addTrackback(title='title', excerpt='excerpt',
                                    url='localhost', blog_name='test blog')
        self.assertEqual(len(bentry.trackbacks), 1)

        self.assertEqual(bentry.trackbacks[tb_id].title, 'title')
        self.assertEqual(bentry.trackbacks[tb_id].excerpt, 'excerpt')
        self.assertEqual(bentry.trackbacks[tb_id].url, 'localhost')
        self.assertEqual(bentry.trackbacks[tb_id].blog_name, 'test blog')

    def testRemoveTrackback(self):
        bentry = self.bentry
        self.testAddTrackback()
        self.assertEqual(len(bentry.trackbacks), 1)

        bentry.removeTrackback(bentry.trackbacks.keys()[0])
        self.assertEqual(len(bentry.trackbacks), 0)

        self.assertRaises(KeyError, bentry.removeTrackback, -1)

    def testRemoveTrackbacks(self):
        bentry = self.bentry
        tb_ids = []
        kw = {'title' : 'title',
              'excerpt' : 'excerpt',
              'url' : 'url',
              'blog_name' : 'blog_name'
              }
        for i in range(10):
            tb_id = bentry.addTrackback(**kw)
            tb_ids.append(tb_id)

        self.assertEqual(len(bentry.trackbacks), 10)

        bentry.removeTrackbacks(tb_ids)
        self.assertEqual(len(bentry.trackbacks), 0)

    def testGetTrackback(self):
        bentry = self.bentry
        self.testAddTrackback()
        tb_id = bentry.trackbacks.keys()[0]

        self.assertEqual(bentry.trackbacks[tb_id].title,
                         bentry.getTrackback(tb_id).title)
        self.assertEqual(bentry.trackbacks[tb_id].excerpt,
                         bentry.getTrackback(tb_id).excerpt)
        self.assertEqual(bentry.trackbacks[tb_id].url,
                         bentry.getTrackback(tb_id).url)
        self.assertEqual(bentry.trackbacks[tb_id].blog_name,
                         bentry.getTrackback(tb_id).blog_name)

        self.assertEqual(bentry.getTrackback(-1, None), None)
        self.assertEqual(bentry.getTrackback(-1), None)

    def testEditTrackback(self):
        bentry = self.bentry
        self.testAddTrackback()
        tb_id = bentry.trackbacks.keys()[0]
        kw = {'title' : 'edit title',
              'excerpt' : 'edit excerpt',
              'url' : 'edit url',
              'blog_name' : 'edit blog_name'
              }

        bentry.editTrackback(tb_id, **kw)
        self.assertEqual(bentry.getTrackback(tb_id).title, kw['title'])
        self.assertEqual(bentry.getTrackback(tb_id).excerpt, kw['excerpt'])
        self.assertEqual(bentry.getTrackback(tb_id).url, kw['url'])
        self.assertEqual(bentry.getTrackback(tb_id).blog_name, kw['blog_name'])

    def testGetSortedTrackbacks(self):
        from DateTime import DateTime
        bentry = self.bentry
        dates = []
        kw = {'title' : 'title',
              'excerpt' : 'excerpt',
              'url' : 'url',
              'blog_name' : 'blog_name'
              }
        for i in range(10):
            tb_id = bentry.addTrackback(**kw)
            date = DateTime() + 1
            bentry.getTrackback(tb_id).created = date
            dates.append(date)

        dates.reverse()
        self.assertEqual([tb.created for tb in bentry.getSortedTrackbacks()],
                         dates)

    def testCountTrackbacks(self):
        kw = {'title' : 'title',
              'excerpt' : 'excerpt',
              'url' : 'url',
              'blog_name' : 'blog_name'
              }
        bentry = self.bentry

        self.assertEqual(bentry.countTrackbacks(), 0)
        bentry.addTrackback(**kw)
        self.assertEqual(bentry.countTrackbacks(), 1)
        bentry.addTrackback(**kw)
        self.assertEqual(bentry.countTrackbacks(), 2)


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(TestBlogEntryCreation),
        unittest.makeSuite(TestBlogEntry),
        ))
    return suite

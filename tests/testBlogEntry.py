# $Id$

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
import CPSBlogTestCase
import xml.dom
import xml.dom.minidom
from DateTime import DateTime
from Products.CPSBlog.BlogEntry import SUMMARY_MAX_LENGTH

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

    def testTbpingGET(self):
        bentry = self.bentry
        request = self.app.REQUEST
        request.set('REQUEST_METHOD', 'GET')
        request.set('PARENTS', [bentry])
        result = bentry.tbping(request)

        self.assert_('<error>1</error>' in result, result)
        self.assert_("GET method requires correct '__mode' parameter" in result,
                     result)

        request.form['__mode'] = 'rss'
        result = bentry.tbping(request)
        self.assert_('<error>0</error>' in result, result)

        doc = xml.dom.minidom.parseString(result)
        self.assertEqual(len(doc.getElementsByTagName('item')), 0)

        kw = {'title' : 'title',
              'excerpt' : 'excerpt',
              'url' : 'url',
              'blog_name' : 'blog_name'
              }
        bentry.addTrackback(**kw)
        result = bentry.tbping(request)
        doc = xml.dom.minidom.parseString(result)
        self.assertEqual(len(doc.getElementsByTagName('item')), 1)

        bentry.addTrackback(**kw)
        result = bentry.tbping(request)
        doc = xml.dom.minidom.parseString(result)
        self.assertEqual(len(doc.getElementsByTagName('item')), 2)

    def testTbpingPOST(self):
        bentry = self.bentry
        request = self.app.REQUEST

        self.assertEqual(bentry.countTrackbacks(), 0)

        bentry.accept_trackback_pings = 0
        request.set('REQUEST_METHOD', 'POST')
        request.set('PARENTS', [bentry])
        request.form['title'] = 'title'
        request.form['excerpt'] = 'excerpt'
        request.form['url'] = 'http://localhost'
        request.form['blog_name'] = 'test blog'
        result = bentry.tbping(request)
        self.assert_('<error>1</error>' in result, result)
        self.assert_(
            '<message>Posting of trackbacks is not allowed at the moment</message>' in result,
            result)

        bentry.accept_trackback_pings = 1
        result = bentry.tbping(request)
        self.assert_('<error>0</error>' in result, result)
        self.assertEqual(bentry.countTrackbacks(), 1)
        tb = bentry.getSortedTrackbacks()[0]
        self.assertEqual(tb.title, 'title')
        self.assertEqual(tb.excerpt, 'excerpt')
        self.assertEqual(tb.url, 'http://localhost')
        self.assertEqual(tb.blog_name, 'test blog')


    def testAddDispatchTrackback(self):
        bentry = self.bentry

        self.assertEqual(len(bentry.dispatch_trackbacks), 0)

        tb_id = bentry.addDispatchTrackback(trackback_url='http://localhost')
        self.assertEqual(len(bentry.dispatch_trackbacks), 1)

        self.assertEqual(bentry.dispatch_trackbacks[tb_id].trackback_url,
                         'http://localhost')
        self.assertEqual(bentry.dispatch_trackbacks[tb_id].sent, False)
        self.assert_(isinstance(bentry.dispatch_trackbacks[tb_id].send_result, tuple))
        self.assertEqual(bentry.dispatch_trackbacks[tb_id].send_result, ())

        # check that trackback with the same url is not added
        tb_id = bentry.addDispatchTrackback(trackback_url='http://localhost')
        self.assertEqual(len(bentry.dispatch_trackbacks), 1)

    def testGetDispatchTrackback(self):
        bentry = self.bentry
        self.testAddDispatchTrackback()
        tb_id = bentry.dispatch_trackbacks.keys()[0]


        self.assertEqual(bentry.dispatch_trackbacks[tb_id].trackback_url,
                         bentry.getDispatchTrackback(tb_id).trackback_url)
        self.assertEqual(bentry.dispatch_trackbacks[tb_id].sent,
                         bentry.getDispatchTrackback(tb_id).sent)

        self.assertEqual(bentry.getDispatchTrackback(-1, None), None)
        self.assertEqual(bentry.getDispatchTrackback(-1), None)

    def testGetSortedDispatchTrackbacks(self):
        bentry = self.bentry
        dates = []
        for i in range(10):
            tb_id = bentry.addDispatchTrackback('http://localhost%d' % i)
            date = DateTime() + 1
            bentry.getDispatchTrackback(tb_id).created = date
            dates.append(date)

        dates.reverse()
        self.assertEqual(
            [tb.created for tb in bentry.getSortedDispatchTrackbacks()],
            dates)

    def testGetEntrySummary(self):
        bentry = self.bentry
        text = "Summary test.  Second line."
        html = "<p>Summary test.</p>&nbsp;&nbsp;Second line.<br/>"
        bentry.content = html
        self.assertEqual(text, bentry.getEntrySummary())

        kw = {'Description' : 'Description Test'}
        bentry.edit(**kw)
        self.assertEqual(bentry.Description(), bentry.getEntrySummary())

        kw = {'Description' : '',
              'content' : 'T' * (SUMMARY_MAX_LENGTH + 10)}
        bentry.edit(**kw)
        res_str = 'T' * SUMMARY_MAX_LENGTH + ' ...'
        self.assertEqual(res_str, bentry.getEntrySummary())


def test_suite():
    return unittest.TestSuite((
        unittest.makeSuite(TestBlogEntryCreation),
        unittest.makeSuite(TestBlogEntry),
        ))
    return suite

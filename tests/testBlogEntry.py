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
        self.login('manager')
        self.ws = self.portal.workspaces

    def beforeTearDown(self):
        self.logout()

    def _createBlog(self):
        self.ws.invokeFactory(type_name='Blog', id='blog')
        return self.ws.blog

    def testAddBlogEntry(self):
        # Test creation of BlogEntry instance.
        blog = self._createBlog()
        self.assert_('blogentry' not in blog.objectIds())

        blog.invokeFactory(type_name='BlogEntry', id='blogentry')
        self.assert_('blogentry' in blog.objectIds())
        self.assert_(hasattr(blog, 'blogentry'))

        blogentry = getattr(blog, 'blogentry').getContent()
        self.assertEqual(blogentry.meta_type, 'BlogEntry')
        self.assertEqual(blogentry.title, '')

    def testRemoveBlogEntry(self):
        # Test removal of BlogEntry instance.
        blog = self._createBlog()
        blog.invokeFactory(type_name='BlogEntry', id='blogentry')
        self.assert_('blogentry' in blog.objectIds())

        blog._delObject('blogentry')
        self.failIf('blogentry' in blog.objectIds())
        self.failIf(hasattr(blog, 'blogentry'))


class TestBlogEntry(CPSBlogTestCase.CPSBlogTestCase):

    def afterSetUp(self):
        self.login('manager')
        self.ws = self.portal.workspaces
        self.ws.invokeFactory(type_name='Blog', id='blog')
        self.blog = self.ws.blog
        self.blog.invokeFactory(type_name='BlogEntry', id='blogentry')
        self.blogentry_proxy = getattr(self.ws.blog, 'blogentry')
        self.blogentry = self.blogentry_proxy.getContent()

    def beforeTearDown(self):
        self.logout()

    def testExportRss(self):
        feed = self.blog.exportrss()
        xml.dom.minidom.parseString(feed)

        kw = {'content': "toto<br>"}
        self.blogentry.edit(proxy=self.blogentry_proxy, **kw)
        feed = self.blog.exportrss()
        xml.dom.minidom.parseString(feed)

    def testExportAtom(self):
        feed = self.blog.exportatom()
        xml.dom.minidom.parseString(feed)

        kw = {'Title': "titi<em>toto</em>",
              'Description': "<p>toto</p>",
              'content': "toto<br>",
             }
        self.blogentry.edit(proxy=self.blogentry_proxy, **kw)
        feed = self.blog.exportatom()
        xml.dom.minidom.parseString(feed)

    def testAddTrackback(self):
        blogentry = self.blogentry

        self.assertEqual(len(blogentry.trackbacks), 0)

        tb_id = blogentry.addTrackback(title='title', excerpt='excerpt',
            url='http://toto.com/titi', blog_name='test blog')

        self.assertEqual(len(blogentry.trackbacks), 1)

        tb = blogentry.getTrackback(tb_id)
        self.assertEqual(tb.title, 'title')
        self.assertEqual(tb.excerpt, 'excerpt')
        self.assertEqual(tb.url, 'http://toto.com/titi')
        self.assertEqual(tb.blog_name, 'test blog')

    def testAddSpamTrackback(self):
        blogentry = self.blogentry
        self.assertEqual(len(blogentry.trackbacks), 0)
        tb_id = blogentry.addTrackback(title='title', excerpt='excerpt',
            url='http://toto.com/', blog_name='test blog')
        self.assertEqual(len(blogentry.trackbacks), 0)

    def testRemoveTrackback(self):
        blogentry = self.blogentry
        self.testAddTrackback()
        self.assertEqual(len(blogentry.trackbacks), 1)

        blogentry.removeTrackback(blogentry.trackbacks.keys()[0])
        self.assertEqual(len(blogentry.trackbacks), 0)

        self.assertRaises(KeyError, blogentry.removeTrackback, -1)

    def testRemoveTrackbacks(self):
        blogentry = self.blogentry
        tb_ids = []
        kw = {'title': 'title',
              'excerpt': 'excerpt',
              'url': 'http://toto.com/toto',
              'blog_name': 'blog_name'
              }
        for i in range(10):
            tb_id = blogentry.addTrackback(**kw)
            tb_ids.append(tb_id)

        self.assertEqual(len(blogentry.trackbacks), 10)

        blogentry.removeTrackbacks(tb_ids)
        self.assertEqual(len(blogentry.trackbacks), 0)

    def testGetTrackback(self):
        blogentry = self.blogentry
        self.testAddTrackback()
        tb_id = blogentry.trackbacks.keys()[0]

        self.assertEqual(blogentry.trackbacks[tb_id].title,
                         blogentry.getTrackback(tb_id).title)
        self.assertEqual(blogentry.trackbacks[tb_id].excerpt,
                         blogentry.getTrackback(tb_id).excerpt)
        self.assertEqual(blogentry.trackbacks[tb_id].url,
                         blogentry.getTrackback(tb_id).url)
        self.assertEqual(blogentry.trackbacks[tb_id].blog_name,
                         blogentry.getTrackback(tb_id).blog_name)

        self.assertEqual(blogentry.getTrackback(-1, None), None)
        self.assertEqual(blogentry.getTrackback(-1), None)

    def testEditTrackback(self):
        blogentry = self.blogentry
        self.testAddTrackback()
        tb_id = blogentry.trackbacks.keys()[0]
        kw = {'title': 'edit title',
              'excerpt': 'edit excerpt',
              'url': 'edit url',
              'blog_name': 'edit blog_name'
              }

        blogentry.editTrackback(tb_id, **kw)
        tb = blogentry.getTrackback(tb_id)
        self.assertEqual(tb.title, kw['title'])
        self.assertEqual(tb.excerpt, kw['excerpt'])
        self.assertEqual(tb.url, kw['url'])
        self.assertEqual(tb.blog_name, kw['blog_name'])

    def testGetSortedTrackbacks(self):
        blogentry = self.blogentry
        dates = []
        kw = {'title': 'title',
              'excerpt': 'excerpt',
              'url': 'http://toto.com/toto',
              'blog_name': 'blog_name'
              }
        for i in range(10):
            tb_id = blogentry.addTrackback(**kw)
            date = DateTime() + 1
            blogentry.getTrackback(tb_id).created = date
            dates.append(date)

        dates.reverse()
        self.assertEqual([tb.created for tb in blogentry.getSortedTrackbacks()],
                         dates)

    def testCountTrackbacks(self):
        kw = {'title': 'title',
              'excerpt': 'excerpt',
              'url': 'http://toto.com/toto',
              'blog_name': 'blog_name'
              }
        blogentry = self.blogentry

        self.assertEqual(blogentry.countTrackbacks(), 0)
        blogentry.addTrackback(**kw)
        self.assertEqual(blogentry.countTrackbacks(), 1)
        blogentry.addTrackback(**kw)
        self.assertEqual(blogentry.countTrackbacks(), 2)

    def testTbpingGET(self):
        blogentry = self.blogentry
        request = self.app.REQUEST
        request.set('REQUEST_METHOD', 'GET')
        request.set('PARENTS', [blogentry])
        result = blogentry.tbping(request)

        self.assert_('<error>1</error>' in result, result)
        self.assert_("GET method requires correct '__mode' parameter" in result,
                     result)

        request.form['__mode'] = 'rss'
        result = blogentry.tbping(request)
        self.assert_('<error>0</error>' in result, result)

        doc = xml.dom.minidom.parseString(result)
        self.assertEqual(len(doc.getElementsByTagName('item')), 0)

        kw = {'title': 'title',
              'excerpt': 'excerpt',
              'url': 'http://toto.com/toto',
              'blog_name': 'blog_name'
              }
        blogentry.addTrackback(**kw)
        result = blogentry.tbping(request)
        doc = xml.dom.minidom.parseString(result)
        self.assertEqual(len(doc.getElementsByTagName('item')), 1)

        blogentry.addTrackback(**kw)
        result = blogentry.tbping(request)
        doc = xml.dom.minidom.parseString(result)
        self.assertEqual(len(doc.getElementsByTagName('item')), 2)

    def testTbpingPOST(self):
        blogentry = self.blogentry
        request = self.app.REQUEST

        self.assertEqual(blogentry.countTrackbacks(), 0)

        blogentry.accept_trackback_pings = 0
        request.set('REQUEST_METHOD', 'POST')
        request.set('PARENTS', [blogentry])
        request.form['title'] = 'title'
        request.form['excerpt'] = 'excerpt'
        request.form['url'] = 'http://toto.com/toto'
        request.form['blog_name'] = 'test blog'
        result = blogentry.tbping(request)
        self.assert_('<error>1</error>' in result, result)
        self.assert_(
            '<message>Posting of trackbacks is not allowed at the moment</message>' in result,
            result)

        blogentry.accept_trackback_pings = 1
        result = blogentry.tbping(request)
        self.assert_('<error>0</error>' in result, result)
        self.assertEqual(blogentry.countTrackbacks(), 1)
        tb = blogentry.getSortedTrackbacks()[0]
        self.assertEqual(tb.title, 'title')
        self.assertEqual(tb.excerpt, 'excerpt')
        self.assertEqual(tb.url, 'http://toto.com/toto')
        self.assertEqual(tb.blog_name, 'test blog')


    def testAddDispatchTrackback(self):
        blogentry = self.blogentry

        self.assertEqual(len(blogentry.dispatch_trackbacks), 0)

        tb_id = blogentry.addDispatchTrackback(trackback_url='http://localhost')
        self.assertEqual(len(blogentry.dispatch_trackbacks), 1)

        self.assertEqual(blogentry.dispatch_trackbacks[tb_id].trackback_url,
                         'http://localhost')
        self.assertEqual(blogentry.dispatch_trackbacks[tb_id].sent, False)
        self.assert_(isinstance(blogentry.dispatch_trackbacks[tb_id].send_result, tuple))
        self.assertEqual(blogentry.dispatch_trackbacks[tb_id].send_result, ())

        # check that trackback with the same url is not added
        tb_id = blogentry.addDispatchTrackback(trackback_url='http://localhost')
        self.assertEqual(len(blogentry.dispatch_trackbacks), 1)

    def testGetDispatchTrackback(self):
        blogentry = self.blogentry
        self.testAddDispatchTrackback()
        tb_id = blogentry.dispatch_trackbacks.keys()[0]


        self.assertEqual(blogentry.dispatch_trackbacks[tb_id].trackback_url,
                         blogentry.getDispatchTrackback(tb_id).trackback_url)
        self.assertEqual(blogentry.dispatch_trackbacks[tb_id].sent,
                         blogentry.getDispatchTrackback(tb_id).sent)

        self.assertEqual(blogentry.getDispatchTrackback(-1, None), None)
        self.assertEqual(blogentry.getDispatchTrackback(-1), None)

    def testGetSortedDispatchTrackbacks(self):
        blogentry = self.blogentry
        dates = []
        for i in range(10):
            tb_id = blogentry.addDispatchTrackback('http://localhost%d' % i)
            date = DateTime() + 1
            blogentry.getDispatchTrackback(tb_id).created = date
            dates.append(date)

        dates.reverse()
        self.assertEqual(
            [tb.created for tb in blogentry.getSortedDispatchTrackbacks()],
            dates)

    def testGetEntrySummary(self):
        blogentry = self.blogentry
        blogentry_proxy = self.blogentry_proxy
        text = "Summary test.  Second line."
        html = "<p>Summary test.</p>&nbsp;&nbsp;Second line.<br/>"
        blogentry.content = html
        self.assertEqual(text, blogentry.getSummary())

        kw = {'Description': 'Description Test'}
        blogentry.edit(proxy=blogentry_proxy, **kw)
        self.assertEqual(blogentry.Description(), blogentry.getSummary())

        kw = {'Description': '',
              'content': 'T' * (SUMMARY_MAX_LENGTH + 10)}
        blogentry.edit(proxy=blogentry_proxy, **kw)
        res_str = 'T' * SUMMARY_MAX_LENGTH + ' ...'
        self.assertEqual(res_str, blogentry.getSummary())


def test_suite():
    suite = unittest.TestSuite((
        unittest.makeSuite(TestBlogEntryCreation),
        unittest.makeSuite(TestBlogEntry),
        ))
    return suite

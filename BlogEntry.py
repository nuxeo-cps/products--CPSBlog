# (C) Copyright 2004 Nuxeo SARL <http://nuxeo.com>
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
#
# $Id$

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.CPSDocument.CPSDocument import CPSDocument
from Products.CMFCore.permissions import View, ModifyPortalContent
from zLOG import LOG, DEBUG
from BTrees.IOBTree import IOBTree
from Trackback import Trackback, DispatchTrackback
import random
import re

factory_type_information = {}

class BlogEntry(CPSDocument):
    """BlogEntry that contain blog post"""

    portal_type = meta_type = 'BlogEntry'

    security = ClassSecurityInfo()

    def __init__(self, id, **kw):
        CPSDocument.__init__(self, id, **kw)
        self.trackbacks = IOBTree()
        self.dispatch_trackbacks = IOBTree()

    def _generateId(self, data):
        id = int(random.random() * 100000)
        while id in data.keys():
            id = int(random.random() * 100000)
        return id

    def _generateTrackbackId(self):
        return self._generateId(self.trackbacks)

    security.declareProtected(ModifyPortalContent, 'addTrackback')
    def addTrackback(self, title='', excerpt='', url='', blog_name=''):
        trackback_id = self._generateTrackbackId()
        trackback = Trackback(trackback_id, title, excerpt, url, blog_name)
        self.trackbacks[trackback_id] = trackback
        return trackback_id

    security.declareProtected(ModifyPortalContent, 'removeTrackback')
    def removeTrackback(self, trackback_id):
        if trackback_id not in self.trackbacks.keys():
            raise KeyError, "Trackback ID %d doesn't exist" % trackback_id
        del self.trackbacks[trackback_id]

    security.declareProtected(ModifyPortalContent, 'removeTrackbacks')
    def removeTrackbacks(self, ids):
        for trackback_id in ids:
            self.removeTrackback(trackback_id)

    security.declareProtected(ModifyPortalContent, 'editTrackback')
    def editTrackback(self, trackback_id, title='', excerpt='',
                      url='', blog_name=''):
        trackback = Trackback(trackback_id, title, excerpt, url, blog_name)
        self.trackbacks[trackback_id] = trackback

    security.declareProtected(View, 'getTrackback')
    def getTrackback(self, trackback_id, default=None):
        return self.trackbacks.get(trackback_id, default)

    security.declareProtected(View, 'getSortedTrackbacks')
    def getSortedTrackbacks(self):
        """Returns trakbacks sorted on creation date in reverse order."""
        t = [(v.created, v) for k, v in self.trackbacks.items()]
        t.sort()
        t.reverse()
        return [v[1] for v in t]

    security.declareProtected(View, 'countTrackbacks')
    def countTrackbacks(self):
        return len(self.trackbacks)

    security.declareProtected(ModifyPortalContent, 'addDispatchTrackback')
    def addDispatchTrackback(self, trackback_url):
        # we do not add trackback if it was added earlier
        for k in self.dispatch_trackbacks.keys():
            if self.dispatch_trackbacks[k].trackback_url == trackback_url:
                return 0
        tb_id = self._generateId(self.dispatch_trackbacks)
        tb = DispatchTrackback(tb_id, trackback_url)
        self.dispatch_trackbacks[tb_id] = tb
        return tb_id

    security.declareProtected(ModifyPortalContent, 'addDispatchTrackbacks')
    def addDispatchTrackbacks(self, context):
        """Adds trackbacks and sends pings."""
        # dispatch_trackback_urls is String List Field from schema definition
        for tb_url in self.dispatch_trackback_urls:
            self.addDispatchTrackback(tb_url)
        return self.sendTrackbacks(context=context)

    security.declareProtected(View, 'getDispatchTrackback')
    def getDispatchTrackback(self, trackback_id, default=None):
        return self.dispatch_trackbacks.get(trackback_id, default)

    security.declareProtected(View, 'getSortedDispatchTrackbacks')
    def getSortedDispatchTrackbacks(self):
        """Returns dispatch trakbacks sorted on creation date in
        reverse order."""
        items = [(v.created, v) for k, v in self.dispatch_trackbacks.items()]
        items.sort()
        items.reverse()
        return [t[1] for t in items]

    security.declareProtected(ModifyPortalContent, 'sendTrackbacks')
    def sendTrackbacks(self, context):
        """Iterates over dispatching trackbacks and sends pings."""
        DESCRIPTION_MAX_LENGTH = 200
        result = []

        blog_proxy = context.getBlogProxy()
        blog_entry = context.getContent()

        def strip_html(text):
            # stripping of html tags based on simple regexp
            return re.sub("<[^>]+>", '', text)

        for k, trackback in self.dispatch_trackbacks.items():
            if not trackback.sent:
                if len(blog_entry.Description()) > 0:
                    excerpt = strip_html(context.description)
                else:
                    excerpt = strip_html(blog_entry.content)
                    if len(excerpt) > DESCRIPTION_MAX_LENGTH:
                        excerpt = excerpt[:DESCRIPTION_MAX_LENGTH]
                        i = excerpt.rfind(' ')
                        if i > 0:
                            excerpt = excerpt[:i]
                        excerpt += '...'

                params = {'title' : context.Title(),
                          'excerpt' : excerpt,
                          'url' : context.absolute_url(),
                          'blog_name' : blog_proxy.Title(),
                          }
                error_code, msg = trackback.send(**params)
                result.append({'trackback_url' : trackback.trackback_url,
                               'error' : error_code,
                               'message' : msg})
        return result

    security.declarePrivate('tbresult')
    def tbresult(self, context, **kw):
        return context.trackback_results(REQUEST=context.REQUEST, **kw)

    security.declarePrivate('handlePostTrackbackPing')
    def handlePostTrackbackPing(self, context, REQUEST):
        res_kw = {'error' : 0,
                  'message' : '',
                  }

        if not self.accept_trackback_pings:
            res_kw['error'] = 1
            res_kw['message'] = "Posting of trackbacks is not allowed at the moment"
            return self.tbresult(context, **res_kw)

        url = REQUEST.form.get('url')
        if url is None:
            res_kw['error'] = 1
            res_kw['message'] = "'url' parameter is required"
        else:
            kw = {'title' : url,
                  'excerpt' : '',
                  'url' : url,
                  'blog_name' : ''
                  }
            for k in ('title', 'excerpt', 'blog_name'):
                kw[k] = REQUEST.form.get(k, kw[k])

            self.addTrackback(**kw)

        return self.tbresult(context, **res_kw)

    security.declarePrivate('handleGetTrackbackPings')
    def handleGetTrackbackPings(self, context, REQUEST):
        res_kw = {'error' : 0,
                  'list_trackbacks' : True,
                  }
        return self.tbresult(context, **res_kw)

    security.declarePublic('tbping')
    def tbping(self, context, REQUEST=None):
        """context parameter must be blog entry proxy"""
        if REQUEST is not None:
            reqmethod = REQUEST['REQUEST_METHOD'].lower()

            if reqmethod == 'get':
                if REQUEST.form.get('__mode') == 'rss':
                    return self.handleGetTrackbackPings(context, REQUEST)
                else:
                    kw = {'error' : 1,
                          'message' : "GET method requires correct '__mode' parameter",
                          }
                    return self.tbresult(context, **kw)
            elif reqmethod == 'post':
                return self.handlePostTrackbackPing(context, REQUEST)

    security.declarePublic('start')
    def start(self):
        """Return start time as a string"""
        return self.created()

    security.declarePublic('end')
    def end(self):
        """Return end time as a string"""
        return self.created()


InitializeClass(BlogEntry)

def addBlogEntry(container, id, REQUEST=None, **kw):
    """Factory method"""
    ob = BlogEntry(id, **kw)
    container._setObject(id, ob)

    if REQUEST:
        ob = container._getOb(id)
        LOG(log_key, DEBUG, "object = %s" % ob)
        REQUEST.RESPONSE.redirect(ob.absolute_url() + '/manage_main')

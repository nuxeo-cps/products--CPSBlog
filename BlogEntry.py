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
from Trackback import Trackback
import random

factory_type_information = {}

class BlogEntry(CPSDocument):
    """BlogEntry that contain blog post"""

    portal_type = meta_type = 'BlogEntry'

    security = ClassSecurityInfo()

    def __init__(self, id, **kw):
        CPSDocument.__init__(self, id, **kw)
        self.trackbacks = IOBTree()

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

    security.declarePrivate('tbresult')
    def tbresult(self, context, **kw):
        return context.trackback_results(REQUEST=context.REQUEST, **kw)

    security.declarePrivate('handlePostTrackbackPing')
    def handlePostTrackbackPing(self, context, REQUEST):
        res_kw = {'error' : 0,
                  'message' : '',
                  }

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

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
from Products.CPSCore.EventServiceTool import getEventService
from Products.CPSBlog.AtomAware import AtomAware
from DateTime import DateTime
import random
import re

SUMMARY_MAX_LENGTH = 400
factory_type_information = {}

class BlogEntry(AtomAware, CPSDocument):
    """BlogEntry that contain blog post"""

    portal_type = meta_type = 'BlogEntry'

    security = ClassSecurityInfo()

    def __init__(self, id, **kw):
        CPSDocument.__init__(self, id, **kw)
        self.trackbacks = IOBTree()
        self.dispatch_trackbacks = IOBTree()

    # FIXME: "data" is not a suitable name for a parameter
    def _generateId(self, data):
        id = int(random.random() * 100000)
        while id in data.keys():
            id = int(random.random() * 100000)
        return id

    def _generateTrackbackId(self):
        return self._generateId(self.trackbacks)

    security.declareProtected(ModifyPortalContent, 'addTrackback')
    def addTrackback(self, context=None, title='', excerpt='', url='',
                     blog_name=''):
        trackback_id = self._generateTrackbackId()
        trackback = Trackback(trackback_id, title, excerpt, url, blog_name)
        
        # Silently ignore spam trackbacks
        if trackback.isSpam():
            return

        blog_proxy = self.getBlogProxy()
        self.trackbacks[trackback_id] = trackback
        LOG('TrackBack', DEBUG, "new trackback for %s" % blog_proxy)
        evtool = getEventService(self)
        ev_infos = {'tb_id': trackback_id,
                    'tb_title': title,
                    'tb_excerpt': excerpt,
                    'tb_url': url,
                    'tb_blog_name': blog_name,
                    'post_url': context and context.absolute_url() or '',
                    'post_title': context and context.Title() or ''
                    }
        evtool.notifyEvent('new_trackback', blog_proxy, ev_infos)
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
        """Return trakbacks sorted on creation date in reverse order."""
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
        """Add trackbacks and sends pings."""
        # dispatch_trackback_urls is String List Field from schema definition
        for tb_url in self.dispatch_trackback_urls:
            self.addDispatchTrackback(tb_url)
        return self.sendTrackbacks(context=context)

    security.declareProtected(View, 'getDispatchTrackback')
    def getDispatchTrackback(self, trackback_id, default=None):
        return self.dispatch_trackbacks.get(trackback_id, default)

    security.declareProtected(View, 'getSortedDispatchTrackbacks')
    def getSortedDispatchTrackbacks(self):
        """Return dispatch trakbacks sorted on creation date in
        reverse order."""
        items = [(v.created, v) for k, v in self.dispatch_trackbacks.items()]
        items.sort()
        items.reverse()
        return [t[1] for t in items]

    security.declareProtected(ModifyPortalContent, 'sendTrackbacks')
    def sendTrackbacks(self, context):
        """Iterate over dispatching trackbacks and sends pings."""
        result = []

        blog_proxy = context.getBlogProxy()
        blog_entry = context.getContent()

        def stripHtml(text):
            # stripping of html tags based on simple regexp
            return re.sub("<[^>]+>", '', text)

        for trackback in self.dispatch_trackbacks.values():
            if not trackback.sent:
                excerpt = self.getSummary()
                
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

            self.addTrackback(context=context, **kw)

        return self.tbresult(context, **res_kw)

    security.declarePrivate('handleGetTrackbackPings')
    def handleGetTrackbackPings(self, context, REQUEST):
        res_kw = {'error' : 0,
                  'list_trackbacks' : True,
                  }
        return self.tbresult(context, **res_kw)

    security.declarePublic('tbping')
    def tbping(self, REQUEST=None):
        """Handle trackback ping.

        This method is meant to be called only via web.
        """

        if REQUEST is not None:
            # REQUEST.PARENTS[0] is our blog entry proxy
            context = REQUEST.PARENTS[0]
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
        return self.effective()

    security.declarePublic('end')
    def end(self):
        """Return end time as a string"""
        return self.effective()

    security.declareProtected(View, 'getEntrySummary')
    def getSummary(self, length=200):
        """Return summary text or from 'Description' field or as computed
        text of length SUMMARY_MAX_LENGTH from 'content' field."""

        def stripHtml(text):
            # stripping of html tags based on simple regexp
            return re.sub("<[^>]+>", '', text)

        def nbsp_to_space(text):
            return re.sub('&nbsp;', ' ', text)

        if len(self.Description()) > 0:
            summary = stripHtml(self.Description())
        else:
            summary = stripHtml(self.content)
            if len(summary) > length:
                summary = summary[:length]
                i = summary.rfind(' ')
                if i > 0:
                    summary = summary[:i]
                summary += ' ...'

        summary = nbsp_to_space(summary)
        return summary

    def atomEdit(self, REQUEST, **kw):
        """Handle ATOM POST to add or update an entry"""
        LOG('CPSBlog', DEBUG, 'Got something in atomEdit!')
        context = REQUEST.PARENTS[0]
        response = REQUEST.RESPONSE
        
        LOG('CPSBlog', DEBUG, 'atomEdit Entry : %s' % context)
        
        #return 'la reponse: %s' % str(REQUEST.BODY)
        
        infos = self._parseAtomXmlEntry(xmlString = REQUEST.BODY)
        self.edit(**infos)
        context.setEffectiveDate(DateTime(infos['EffectiveDate']))
        #newob.setEffectiveDate(DateTime(infos['EffectiveDate']))
        
        result = context.atomEntry()
        response.setStatus(200)
        response.setHeader('Location', context.absolute_url())
        response.setHeader('Content-Type', 'application/atom+xml')
        response.setBody(result)
        return result
        


InitializeClass(BlogEntry)

def addBlogEntry(container, id, REQUEST=None, **kw):
    """Factory method"""
    ob = BlogEntry(id, **kw)
    container._setObject(id, ob)

    if REQUEST:
        ob = container._getOb(id)
        LOG(log_key, DEBUG, "object = %s" % ob)
        REQUEST.RESPONSE.redirect(ob.absolute_url() + '/manage_main')

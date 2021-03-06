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
# $Id: Blog.py 25927 2005-08-17 22:57:00Z ebarroca $

from zLOG import LOG, DEBUG, TRACE
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CPSUtil.html import sanitize
from lxml import etree
from StringIO import StringIO
from Acquisition import aq_parent, aq_inner
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName

class AtomMixin:
    """Define common attributes / method of an AtomAware Ressource"""

    def parseAtomXmlEntry(self, xml_string, title_tags=None, body_tags=None):
        title_tags = ('b', 'a', 'em', 'strong')
        body_tags = ('p', 'br', 'span', 'div', 'ul', 'ol', 'li',
                    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a',
                    'em', 'strong', 'i', 'd', 'dl', 'dd', 'dd',
                    'table', 'tr', 'td', 'b', 'img')

        body = StringIO(xml_string)
        tbody = etree.parse(body)
        info = {}
        ns = {'a': 'http://purl.org/atom/ns#',
              'ab': 'http://purl.org/atom-blog/ns#',
              'dc': 'http://purl.org/dc/elements/1.1/',
              'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
              'wsu': 'http://schemas.xmlsoap.org/ws/2002/07/utility',
              'wsse': 'http://schemas.xmlsoap.org/ws/2002/07/secext',
              'xmlns': 'http://schemas.xmlsoap.org/wsdl/http/'}

        xtitle = tbody.xpath('//a:entry/a:title', namespaces=ns)
        xcontent = tbody.xpath('//a:entry/a:content', namespaces=ns)
        xcategories = tbody.xpath('//a:entry/dc:subject', namespaces=ns)
        xissued = tbody.xpath('//a:entry/a:issued', namespaces=ns)
        xdraft = tbody.xpath('//a:entry/ab:draft', namespaces=ns)

        if xtitle:
            info['Title'] = sanitize(xtitle[0].text, tags_to_keep=title_tags)
        if xcontent:
            info['content'] = sanitize(xcontent[0].text, tags_to_keep=body_tags)
        if xissued:
            info['CreationDate'] = DateTime(xissued[0].text)
            info['EffectiveDate'] = info['CreationDate']
        if xdraft:
            if xdraft[0].text == 'true':
                info['publish'] = False
            else:
                info['publish'] = True
        else:
            info['publish'] = True

        info['Subject'] = []
        for category in xcategories:
            info['Subject'].append(category.text)

        return info

class AtomAware(AtomMixin):
    """AtomAware base class"""

    security = ClassSecurityInfo()

    security.declareProtected(ModifyPortalContent, 'atom')
    def atom(self, REQUEST, **kw):
        """Handle ATOM commands"""

        #mtool = getToolByName(self, 'portal_membership')
        #if mtool.isAnonymousUser():
        #    response = REQUEST.RESPONSE
        #response.setStatus(401)
	    #return response

        if REQUEST['REQUEST_METHOD'] == 'POST':
            response = self.atomPost(REQUEST, **kw)
        # FIXME what do we do here ???
        elif REQUEST['REQUEST_METHOD'] == 'GET':
            response = REQUEST
        elif REQUEST['REQUEST_METHOD'] == 'DELETE':
            response = self.atomDelete(REQUEST, *kw)
        return response

InitializeClass(AtomAware)

class AtomAwareEntry(AtomAware):
    """Class that add some Atom capacity to documents (entries)"""

    security = ClassSecurityInfo()

    security.declarePrivate('atomPost')
    def atomPost(self, REQUEST, **kw):
        """Handle ATOM POST to add or update an entry"""
        LOG('CPSBlog', DEBUG, 'Got something in atomEdit!')
        context = REQUEST.PARENTS[0]
        response = REQUEST.RESPONSE

        LOG('CPSBlog', DEBUG, 'atomEdit Entry : %s' % context)

        info = self.parseAtomXmlEntry(REQUEST.BODY)
        self.edit(**info)
        context.setEffectiveDate(info['EffectiveDate'])

        # Manage the workflow
        wftool = getToolByName(context, 'portal_workflow')
        if info['publish'] and wftool.getInfoFor(context, 'review_state') == 'work':
            wftool.doActionFor(context, 'publish', comment='')
        elif wftool.getInfoFor(context, 'review_state') == 'published' and not info['publish']:
            wftool.doActionFor(context, 'unpublish', comment='')

        result = context.atomEntry()
        response.setStatus(200)
        response.setHeader('Location', context.absolute_url())
        response.setHeader('Content-Type', 'application/atom+xml')
        response.setBody(result)
        return response

    security.declarePrivate('atomDelete')
    def atomDelete(self, REQUEST, **kw):
        """Handle a DELETE"""
        response = REQUEST.RESPONSE
        context = REQUEST.PARENTS[0]
        parent = aq_parent(aq_inner(context))
        parent.manage_delObjects(context.getId())
        response.setStatus(204)
        return response

InitializeClass(AtomAwareEntry)

class AtomAwareCollection(AtomAware):
    """Add some Atom capacity to collections (folders / folderish)"""

    security = ClassSecurityInfo()

    security.declarePrivate('atomPost')
    def atomPost(self, REQUEST, **kw):
        """Post something to CPSBlog"""
        LOG('CPSBlog', TRACE, 'Got something in atomPost : %s !' % REQUEST.PARENTS[0])
        context = REQUEST.PARENTS[0]
        response = REQUEST.RESPONSE
        info = self.parseAtomXmlEntry(REQUEST.BODY)
        effective_date = info['EffectiveDate']
        #language = context.translation_service.getSelectedLanguage()
        #lang = 'en'
        # TODO add language support
        # FIXME: the date should be in the computeId parameter
        entry_id = DateTime().strftime('%Y_%m_%d') + '_' \
                   + self.computeId(info['Title'])

        # Create the new post and set the effective date
        wftool = getToolByName(self, 'portal_workflow')
        newid = wftool.invokeFactoryFor(context, 'BlogEntry', entry_id, **info)
        newob = getattr(context, newid)
        newob.setEffectiveDate(effective_date)
        newob.getEditableContent().setEffectiveDate(effective_date)

        LOG('CPSBlog', DEBUG, 'New Entry "%s" Created !' % newid)

        # Publish directly if not draft
        if info['publish']:
            wftool.doActionFor(newob, 'publish', comment='')

        response.setStatus(201)
        response.setHeader('Location', context.absolute_url() + "/" + newid)
        response.setHeader('Content-Type', 'application/atom+xml')
        response.setBody(newob.atomEntry(entry=newob))
        return response

InitializeClass(AtomAwareCollection)

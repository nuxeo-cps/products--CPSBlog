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
from Products.CMFCore.CMFCorePermissions import View
from Products.CMFCore.PortalContent import PortalContent
from Products.CMFCore.CMFCatalogAware import CMFCatalogAware
from Products.BTreeFolder2.CMFBTreeFolder import CMFBTreeFolder
from Products.CPSDocument.CPSDocument import CPSDocumentMixin
from Products.CMFDefault.DublinCore import DefaultDublinCoreImpl


factory_type_information = {}

class Blog(CPSDocumentMixin, CMFCatalogAware, CMFBTreeFolder,
           PortalContent, DefaultDublinCoreImpl):
    """Blog that can contain lots of blog entries."""

    portal_type = meta_type = 'Blog'

    security = ClassSecurityInfo()

    def __init__(self, id, **kw):
        self.id = id
        CMFBTreeFolder.__init__(self, id)
        DefaultDublinCoreImpl.__init__(self)

    security.declarePublic('start')
    def start(self):
        """Return start time as a string"""
        return self.created()

    security.declarePublic('end')
    def end(self):
        """Return end time as a string"""
        return self.created()


InitializeClass(Blog)

def addBlogInstance(container, id, REQUEST=None, **kw):
    """Factory method"""
    ob = Blog(id, **kw)
    container._setObject(id, ob)

    if REQUEST:
        ob = container._getOb(id)
        LOG(log_key, DEBUG, "object = %s" % ob)
        REQUEST.RESPONSE.redirect(ob.absolute_url() + '/manage_main')

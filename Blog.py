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
from zLOG import LOG, DEBUG, TRACE
from BTrees.IOBTree import IOBTree
from Products.CMFCore.permissions import View, ModifyPortalContent
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CPSBlog.AtomAware import AtomAwareCollection
import random

factory_type_information = {}

class Blog(AtomAwareCollection, CPSDocument):
    """Blog that can contain lots of blog entries."""

    portal_type = meta_type = 'Blog'

    security = ClassSecurityInfo()

    def __init__(self, id, **kw):
        CPSDocument.__init__(self, id, **kw)
        self.categories = IOBTree()

    def _generateId(self):
        id = int(random.random() * 100000)
        while id in self.categories.keys():
            id = int(random.random() * 100000)
        return id

    security.declareProtected(ModifyPortalContent, 'addCategory')
    def addCategory(self, title='', description='', urls_to_ping=(),
                    accept_pings=False):
        """Add category to blog, auto generates id of category """
        catid = self._generateId()

        category = {'id': catid,
                    'title': title,
                    'description': description,
                    'urls_to_ping': urls_to_ping,
                    'accept_pings': accept_pings
                    }
        self.categories.insert(catid, category)
        return catid

    security.declareProtected(ModifyPortalContent, 'removeCategory')
    def removeCategory(self, catid):
        """Remove category."""
        if self.categories.has_key(catid):
            del self.categories[catid]

    security.declareProtected(View, 'getCategory')
    def getCategory(self, catid):
        """Return category by id."""
        return self.categories.get(catid, None)

    security.declareProtected(View, 'getCategoryByTitle')
    def getCategoryByTitle(self, title):
        """Return category by title."""
        for catdef in self.getSortedCategories():
            if catdef['title'] == title:
                return catdef
        return None

    security.declareProtected(View, 'getSortedCategories')
    def getSortedCategories(self):
        """Return categories sorted by title."""
        t = [(v['title'].lower(), k) for k, v in self.categories.items()]
        t.sort()
        return [self.categories.get(v[1]) for v in t]

    security.declareProtected(ModifyPortalContent, 'updateCategory')
    def updateCategory(self, catid, catdef):
        """Update category by id."""
        if self.categories.has_key(catid):
            d = self.categories[catid].copy()
            d.update(catdef)
            self.categories[catid] = d


InitializeClass(Blog)

def addBlog(container, id, REQUEST=None, **kw):
    """Factory method"""
    ob = Blog(id, **kw)
    container._setObject(id, ob)

    if REQUEST is not None:
        ob = container._getOb(id)
        REQUEST.RESPONSE.redirect(ob.absolute_url() + '/manage_main')

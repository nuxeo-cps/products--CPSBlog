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
# $id$

from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.CPSDocument.CPSDocument import CPSDocument
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2Base
from Products.CMFCore.CMFCorePermissions import View


factory_type_information = ()

class Blog(CPSDocument, BTreeFolder2Base):
    """Blog that can contain lots of blog entries."""

    portal_type = meta_type = 'Blog'

    security = ClassSecurityInfo()

    #security.declareProtected(View, '')

InitializeClass(Blog)

def addBlogInstance(container, id, REQUEST=None, **kw):
    """Factory method"""
    ob = Blog(id, **kw)
    container._setObject(id, ob)

    if REQUEST:
        ob = container._getOb(id)
        LOG(log_key, DEBUG, "object = %s" % ob)
        REQUEST.RESPONSE.redirect(ob.absolute_url() + '/manage_main')

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
from zLOG import LOG, DEBUG

factory_type_information = {}

class Blog(CPSDocument):
    """Blog that can contain lots of blog entries."""

    portal_type = meta_type = 'Blog'

    security = ClassSecurityInfo()

InitializeClass(Blog)

def addBlog(container, id, REQUEST=None, **kw):
    """Factory method"""
    ob = Blog(id, **kw)
    container._setObject(id, ob)

    # FIXME: if REQUEST != None, this will brake
    # This is not covered by the tests by the way.
    # Is it useful to be able to add object from the ZMI, BTW ?
    if REQUEST:
        ob = container._getOb(id)
        LOG(log_key, DEBUG, "object = %s" % ob)
        REQUEST.RESPONSE.redirect(ob.absolute_url() + '/manage_main')

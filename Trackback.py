# (C) Copyright 2005 Nuxeo SARL <http://nuxeo.com>
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

from Acquisition import Implicit
from AccessControl import ClassSecurityInfo
from Globals import Persistent
from DateTime import DateTime
import Globals

class Trackback(Persistent, Implicit):
    security = ClassSecurityInfo()

    security.setDefaultAccess('allow')

    def __init__(self, id, title, excerpt, url, blog_name):
        self.id = id
        self.title = title
        self.excerpt = excerpt
        self.url = url
        self.blog_name = blog_name
        self.created = DateTime()

Globals.InitializeClass(Trackback)
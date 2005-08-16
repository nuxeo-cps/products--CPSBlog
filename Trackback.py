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
from Products.CPSBlog.utils import post_trackback
import urlparse

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

    def isSpam(self):
        """Is this trackback spam (based on heuristics)?

        Heuristics used:
          - Top levels URL are probably spam
          - (That's all for now)
        """
        path = urlparse.urlparse(self.url)[2]
        if path in ("/", ""):
            return True
        return False

Globals.InitializeClass(Trackback)

class DispatchTrackback(Persistent, Implicit):
    security = ClassSecurityInfo()

    security.setDefaultAccess('allow')

    def __init__(self, id, trackback_url):
        self.id = id
        self.trackback_url = trackback_url
        self.sent = False
        self.created = DateTime()
        self.send_result = ()

    def send(self, title, excerpt, url, blog_name):
        err, msg = post_trackback(self.trackback_url, title=title,
                                  excerpt=excerpt, url=url,
                                  blog_name=blog_name)
        if not err:
            self.sent = True

        self.send_result = (err, msg)

        return err, msg

Globals.InitializeClass(DispatchTrackback)

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
""" Init """

from Products.CPSBlog.Blog import Blog, addBlogInstance, \
     factory_type_information as blog_fti
from Products.CPSBlog.BlogEntry import BlogEntry, addBlogEntryInstance, \
     factory_type_information as blogentry_fti
from Products.CPSBlog.BlogCalendarBox import BlogCalendarBox, \
     addBlogCalendarBox, factory_type_information as blogcalendarbox_fti
from Products.CMFCore.utils import ContentInit
from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFCore.CMFCorePermissions import AddPortalContent
from zLOG import LOG, INFO, DEBUG
from AccessControl import ModuleSecurityInfo
import Products.CPSBlog.permissions
import BlogAggregator

logKey = 'CPSBlog.__init__'

contentClasses = (
    Blog,
    BlogEntry,
    BlogCalendarBox,
    BlogAggregator.BlogAggregator,
    )

contentConstructors = (
    addBlogInstance,
    addBlogEntryInstance,
    addBlogCalendarBox,
    BlogAggregator.addBlogAggregator,
    )

fti = (blog_fti, blogentry_fti, blogcalendarbox_fti[0],
       BlogAggregator.factory_type_information)

registerDirectory('skins', globals())

# allow to use Batch from page templates
ModuleSecurityInfo('Products.CPSBlog.CPSBatch').declarePublic('Batch')

def initialize(registrar):
    ContentInit('CPSBlog Types',
                content_types = contentClasses,
                permission = AddPortalContent,
                extra_constructors = contentConstructors,
                fti = fti,
                ).initialize(registrar)

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
"""BlogCalendarBox"""
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo

from Products.CMFCore.CMFCorePermissions import View, ModifyPortalContent
from Products.CPSDefault.BaseBox import BaseBox

from zLOG import LOG, DEBUG

factory_type_information = (
    {'id': 'Blog Calendar Box',
     'title': 'portal_type_BlogCalendarBox_title',
     'description': 'portal_type_BlogCalendarBox_description',
     'meta_type': 'Blog Calendar Box',
     'icon': 'box.png',
     'product': 'CPSBlog',
     'factory': 'addBlogCalendarBox',
     'immediate_view': 'blogcalendarbox_edit_form',
     'filter_content_types': 0,
     'actions': ({'id': 'view',
                  'name': 'View',
                  'action': 'basebox_view',
                  'permissions': (View,)},
                 {'id': 'edit',
                  'name': 'Edit',
                  'action': 'blogcalendarbox_edit_form',
                  'permissions': (ModifyPortalContent,)},
                 ),
     # additionnal cps stuff
     'cps_is_portalbox': 1,
     },
    )


class BlogCalendarBox(BaseBox):
    """A box displaying Blog Calendar objects."""
    meta_type = 'Blog Calendar Box'
    portal_type = 'Blog Calendar Box'

    security = ClassSecurityInfo()

    _properties = BaseBox._properties + (
        {'id': 'events_in', 'type': 'text', 'mode': 'w',
         'label': 'location of events to be shown'},
        )

    events_in = None
    event_types = []

    def __init__(self, id, **kw):
        BaseBox.__init__(self, id, provider='cpsblog',
                         category='blogcalendarbox', **kw)

    def edit(self, **kw):
        self.events_in = self.REQUEST.form.get('events_in') or \
                         kw.get('events_in')
        if not self.events_in:
            self.events_in = None
        self.event_types = self.REQUEST.form.get('event_types') or \
                           kw.get('event_types')
        if not self.event_types:
            #necessary as the edit form does an inclusion test and
            #thus needs event_types to be a sequence, even if empty
            self.event_types = []
        BaseBox.edit(self, **kw)


InitializeClass(BlogCalendarBox)


def addBlogCalendarBox(dispatcher, id, REQUEST=None, **kw):
    """Add an Blog Calendar Box."""
    ob = BlogCalendarBox(id, **kw)
    dispatcher._setObject(id, ob)
    ob = getattr(dispatcher, id)
    ob.manage_permission(View, ('Anonymous',), 1)
    if REQUEST is not None:
        url = dispatcher.DestinationURL()
        REQUEST.RESPONSE.redirect('%s/manage_main' % url)

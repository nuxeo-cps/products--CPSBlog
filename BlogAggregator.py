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

from Acquisition import aq_base
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.CMFCore.CMFCorePermissions import View
from Products.CPSDocument.CPSDocument import CPSDocument
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime

factory_type_information = {}

class BlogAggregator(CPSDocument):
    """BlogAggregator that makes catalog searches about blog entries."""

    portal_type = meta_type = 'BlogAggregator'

    security = ClassSecurityInfo()

    security.declareProtected('View', 'getSearchResults')
    def getSearchResults(self, context):
        """Get sorted search result of blog entries."""
        query = self._buildQuery()

        sort_by, direction = None, 'asc'
        if self.sort_by:
            sort_by, direction = self.sort_by.split('_')

        params = context.getDisplayParams(sort_by=sort_by,
                                          direction=direction)

        brains = context.search(query=query,
                                sort_by=params['sort_by'],
                                direction=params['direction'])

        return filter(None, [brain.getObject() for brain in brains])


    def _buildQuery(self):
        query = {}

        # hardcoded portal_type
        query['portal_type'] = 'BlogEntry'

        if self.query_title:
            query['Title'] = self.query_title
        if self.query_description:
            query['Description'] = self.query_description
        if self.query_fulltext:
            query['SearchableText'] = self.query_fulltext
        if self.query_categories:
            query['Subject'] = self.query_categories
        if self.query_status:
            query['review_state'] = self.query_status

        if self.query_modified:
            modified = None
            if self.query_modified == 'time_last_login':
                mtool = getToolByName(self, 'portal_membership')
                member = mtool.getAuthenticatedMember()
                if hasattr(aq_base(member), 'last_login_time'):
                    modified = member.last_login_time
            else:
                today = DateTime()
                if self.query_modified == 'time_yesterday':
                    modified = today - 1
                elif self.query_modified == 'time_last_week':
                    modified = today - 7
                elif self.query_modified == 'time_last_month':
                    modified = today - 31
            if modified:
                query['modified'] = modified
                query['modified_usage'] = "range:min"

        return query

InitializeClass(BlogAggregator)


def addBlogAggregator(container, id, REQUEST=None, **kw):
    """Factory method"""
    ob = BlogAggregator(id, **kw)
    container._setObject(id, ob)

    if REQUEST:
        ob = container._getOb(id)
        LOG(log_key, DEBUG, "object = %s" % ob)
        REQUEST.RESPONSE.redirect(ob.absolute_url() + '/manage_main')

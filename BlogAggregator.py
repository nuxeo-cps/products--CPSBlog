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
from Products.CMFCore.permissions import View
from Products.CPSDocument.CPSDocument import CPSDocument
from Products.CMFCore.utils import getToolByName
from Products.CPSPortlets.CPSPortlet import CPSPortlet
from DateTime import DateTime


class BlogAggregatorBase(CPSDocument):
    security = ClassSecurityInfo()

    security.declareProtected(View, 'getSearchResults')
    def getSearchResults(self, context):
        """Get sorted search result of blog entries.
        
        FIXME: what is context ?"""

        query = self._buildQuery()

        sort_by, direction = None, 'asc'
        if self.sort_by:
            sort_by, direction = self.sort_by.split('_')

        params = context.getDisplayParams(sort_by=sort_by,
                                          direction=direction)

        if sort_by == 'date':
            catalog = context.portal_catalog
            query['sort_on'] = 'effective'
            if direction.startswith('desc'):
                query['sort_order'] = 'reverse'
            else:
                query['sort_order'] = 'ascending'
            brains = catalog.searchResults(**query)
        else:
            brains = context.search(query=query,
                                    sort_by=params['sort_by'],
                                    direction=params['direction'])
        if self.search_limit > 0:
            brains = brains[:self.search_limit]

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

InitializeClass(BlogAggregatorBase)


blog_aggregator_fti = {}

class BlogAggregator(BlogAggregatorBase):
    """BlogAggregator that makes catalog searches about blog entries."""

    portal_type = meta_type = 'BlogAggregator'

InitializeClass(BlogAggregator)

def addBlogAggregator(container, id, **kw):
    """Factory method"""
    ob = BlogAggregator(id, **kw)
    container._setObject(id, ob)


blog_aggregator_portlet_fti = {}

class BlogAggregatorPortlet(BlogAggregator, CPSPortlet):
    """BlogAggregator portlet makes catalog searches about blog entries."""

    portal_type = meta_type = 'BlogAggregator Portlet'

    security = ClassSecurityInfo()

InitializeClass(BlogAggregatorPortlet)

def addBlogAggregatorPortlet(container, id, **kw):
    """Factory method"""
    ob = BlogAggregatorPortlet(id, **kw)
    container._setObject(id, ob)


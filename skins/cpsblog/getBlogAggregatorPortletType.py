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

blogaggregator_portlet_type = {
    'title': 'portal_type_BlogAggregatorPortlet_title',
    'description': 'portal_type_BlogAggregatorPortlet_description',
    'content_icon': 'blogaggregator_portlet_icon.png',
    'content_meta_type': 'BlogAggregator Portlet',
    'product': 'CPSBlog',
    'factory': 'addBlogAggregatorPortlet',
    'immediate_view': 'cpsportlet_edit_form',
    'global_allow': False,
    'filter_content_types': False,
    'allowed_content_types': (),
    'allow_discussion': False,
    'cps_is_searchable': False,
    'cps_proxy_type': '',
    'cps_display_as_document_in_listing': False,
    'schemas': ('portlet_common', 'blogaggregator_portlet', 'common', 'metadata'),
    'layouts': ('portlet_common', 'blogaggregator_portlet',),
    'flexible_layouts': (),
    'storage_methods': (),
    'cps_is_portlet': True,
    'actions': (
         {'id': 'create',
          'name': 'action_create',
          'action': 'string:${object_url}/cpsportlet_create_form',
          'condition': '',
          'permission': ('Manage Portlets',),
          'category': 'object',
          'visible': 0,},
         {'id': 'edit',
          'name': 'action_edit',
          'action': 'string:${object_url}/cpsportlet_edit_form',
          'condition': '',
          'permission': ('Manage Portlets',),
          'category': 'object',
          'visible': 0,},
         {'id': 'view',
          'name': 'action_view',
          'action': 'string:${object_url}/render',
          'condition': '',
          'permission': ('View',),
          'category': 'object',
          'visible': False,},
         {'id': 'metadata',
          'name': 'action_metadata',
          'action': 'string:${object_url}/cpsportlet_metadata',
          'condition': '',
          'permission': ('Manage Portlets',),
          'category': 'object',
          'visible': 0,},
    )
}

types = {'BlogAggregator Portlet': blogaggregator_portlet_type}

return types

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

blogaggregator_portlet_schema = {
    'custom_cache_params': {
        'type': 'CPS String List Field',
        'data': {
            'default_expr': "python:['no-cache']",
            'is_searchabletext': False,
            'acl_read_permissions': '',
            'acl_read_roles': '',
            'acl_read_expr': '',
            'acl_write_permissions': '',
            'acl_write_roles': '',
            'acl_write_expr': '',
            'read_ignore_storage': False,
            'read_process_expr': '',
            'read_process_dependent_fields': (),
            'write_ignore_storage': False,
            'write_process_expr': '',
            },
        },
    'query_title': {
        'type': 'CPS String Field',
        'data': {'default_expr': 'string:',
                 'is_searchabletext': 0,
                 },
        },
    'query_description': {
        'type': 'CPS String Field',
        'data': {'default_expr': 'string:',
                 'is_searchabletext': 0,
                 },
        },
    'query_fulltext': {
        'type': 'CPS String Field',
        'data': {'default_expr': 'string:',
                 'is_searchabletext': 0,
                 },
        },
    'query_categories': {
        'type': 'CPS String Field',
        'data': {'is_searchabletext': 0,
                 },
        },
    'query_modified': {
        'type': 'CPS String Field',
        'data': {'default_expr': 'string:',
                 'is_searchabletext': 0,
                 },
        },
    'query_status': {
        'type': 'CPS String Field',
        'data': {'default_expr': 'string:',
                 'is_searchabletext': 0,
                 },
        },
    'view_mode': {
        'type': 'CPS String Field',
        'data': {'default_expr': 'string:',
                 'is_searchabletext': 0,
                 },
        },
    'entries_per_page' : {
        'type': 'CPS Int Field',
        'data': {'default_expr': 'python:10',
                 'is_searchabletext': 0,
                 },
        },
    'sort_by': {
        'type': 'CPS String Field',
        'data': {'default_expr': 'string:date_desc',
                 'is_searchabletext': 0,
                 },
        },
    }

schemas = {'blogaggregator_portlet': blogaggregator_portlet_schema}
return schemas

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
# $id

from Products.CMFCore.CMFCorePermissions import View, ModifyPortalContent

blog_type = {
    'title': "portal_type_Blog_title",
    'description': "portal_type_Blog_description",
    'content_icon': 'blog_icon.png',
    'content_meta_type': 'Blog',
    'product': 'CPSBlog',
    'factory': 'addBlogInstance',
    'immediate_view': 'blog_view',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': ['BlogEntry'],
    'allow_discussion': 1,
    'cps_is_searchable': 1,
    # Choose between 'document', 'folder' or 'folderishdocument'
    # according to the need to store objects in your document or not.
    'cps_proxy_type': 'folderishdocument',
    'schemas': ['metadata', 'common', 'blog'],
    'layouts': ['common', 'blog'],
    'flexible_layouts': [],
    'storage_methods': [],
    'cps_workspace_wf': 'workspace_content_wf',
    'cps_section_wf': 'section_content_wf',
    'use_content_status_history': 1,
    'actions': ({'id': 'view',
                 'name': 'action_view',
                 'action': 'blog_view',
                 'permissions': (View,)
                 },
                {'id': 'new_content',
                 'name': 'action_new_content',
                 'action': 'string:${object_url}/folder_factories',
                 'condition': "python:object.getTypeInfo().cps_proxy_type != 'document'",
                 'permissions': (ModifyPortalContent,)
                 },
                {'id': 'contents',
                 'name': 'action_folder_contents',
                 'action': 'string:${object_url}/folder_contents',
                 'condition' : "python:object.getTypeInfo().cps_proxy_type != 'document'",
                 'permissions': (ModifyPortalContent,)
                 },
                {'id': 'edit',
                 'name': 'action_edit',
                 'action': 'string:${object_url}/cpsdocument_edit_form',
                 'condition' : '',
                 'permissions': (ModifyPortalContent,)
                 },
                {'id': 'metadata',
                 'name': 'action_metadata',
                 'action': 'string:${object_url}/cpsdocument_metadata',
                 'condition' : 'not:portal/portal_membership/isAnonymousUser',
                 'permissions': (View,)
                 },
                {'id': 'localroles',
                 'name': 'action_local_roles',
                 'action': 'string:${object_url}/folder_localrole_form',
                 'condition' : "python:object.getTypeInfo().cps_proxy_type != 'document'",
                 'permissions': ('Change permissions',)
                 })
    }

blog_entry_type = {
    'title': "portal_type_BlogEntry_title",
    'description': "portal_type_BlogEntry_description",
    'content_icon': 'blog_entry_icon.png',
    'content_meta_type': 'BlogEntry',
    'product': 'CPSBlog',
    'factory': 'addBlogEntryInstance',
    'immediate_view': 'cpsdocument_view',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': [],
    'allow_discussion': 1,
    'cps_is_searchable': 1,
    # Choose between 'document', 'folder' or 'folderishdocument'
    # according to the need to store objects in your document or not.
    'cps_proxy_type': 'document',
    'schemas': ['metadata', 'common', 'blog_entry'],
    'layouts': ['common', 'blog_entry'],
    'flexible_layouts': [],
    'storage_methods': [],
    'cps_workspace_wf': 'workspace_content_wf',
    'cps_section_wf': 'section_content_wf',
    'use_content_status_history': 1,
    }

def getDocumentTypes(portal=None):
    types = {}
    types['Blog'] = blog_type
    types['BlogEntry'] = blog_entry_type
    return types


blog_schema = {
    'view_mode': {
        'type': 'CPS String Field',
        'data': {'default_expr': 'string:',
                 'is_searchabletext': 0,
                 },
        },
    'display_entries' : {
        'type': 'CPS Int Field',
        'data': {'default_expr': 'python:10',
                 'is_searchabletext': 0,
                 },
        },
    }

blog_entry_schema = {
    'body' : {
        'type': 'CPS String Field',
        'data': {'default_expr': 'string:',
                 'is_searchabletext': 0,
                 },
        },
    }

def getDocumentSchemas(portal=None):
    schemas = {}
    schemas['blog'] = blog_schema
    schemas['blog_entry'] = blog_entry_schema
    return schemas


blog_view_mode_vocabulary = {
    'data': {
        'tuples':(
            ('title', 'Title', 'view_mode_Title_label'),
            ('description', 'Description', 'view_mode_Description_label'),
            ('full', 'Full', 'view_mode_Full_label'),
            ),
        },
    }

blog_categories_vocabulary = {
    'data': {
#        'tuples':((), ),
        },
    }

def getDocumentVocabularies(portal=None):
    vocabularies = {}
    vocabularies['blog_view_mode'] = blog_view_mode_vocabulary
    vocabularies['blog_categories'] = blog_categories_vocabulary
    return vocabularies


blog_layout = {
    'widgets': {
        'view_mode': {
            'type': 'Select Widget',
            'data': {'title': '',
                     'fields': ('view_mode',),
                     'is_required': False,
                     'label': '',
                     'label_edit': '',
                     'description': '',
                     'help': '',
                     'is_i18n': True,
                     'readonly_layout_modes': (),
                     'hidden_layout_modes': ('view',),
                     'hidden_readonly_layout_modes': (),
                     'hidden_empty': False,
                     'hidden_if_expr': '',
                     'css_class': '',
                     'widget_mode_expr': '',
                     'vocabulary': 'blog_view_mode',
                     'translated': True,
                },
            },
        'display_entries': {
            'type': 'Int Widget',
            'data': {'title': '',
                     'fields': ('display_entries',),
                     'is_required': False,
                     'label': '',
                     'label_edit': '',
                     'description': '',
                     'help': '',
                     'is_i18n': True,
                     'readonly_layout_modes': (),
                     'hidden_layout_modes': ('view',),
                     'hidden_readonly_layout_modes': (),
                     'hidden_empty': False,
                     'hidden_if_expr': '',
                     'css_class': '',
                     'width': 3,
                     'widget_mode_expr': '',
                     'translated': True,
                },
            },
        },
    'layout': {
        'style_prefix': 'layout_default_',
        'ncols': 1,
        'rows': [
            [{'widget_id': 'view_mode'},],
            [ {'widget_id': 'display_entries'},],
            ],
        },
    }

blog_entry_layout = {
    'widgets': {
        'body': {
            'type': 'Rich Text Editor Widget',
            'data': {'title': '',
                     'fields': ('body',),
                     'is_required': False,
                     'label': '',
                     'label_edit': '',
                     'description': '',
                     'help': '',
                     'is_i18n': True,
                     'readonly_layout_modes': (),
                     'hidden_layout_modes': ('view',),
                     'hidden_readonly_layout_modes': (),
                     'hidden_empty': False,
                     'hidden_if_expr': '',
                     'css_class': '',
                     'widget_mode_expr': '',
                     'vocabulary': '',
                     'translated': True,
                },
            },
        'Subject': {
            'type': 'MultiSelect Widget',
            'data': {'title': '',
                     'fields': ('Subject',),
                     'is_required': False,
                     'label': '',
                     'label_edit': 'Categories',
                     'description': '',
                     'help': '',
                     'is_i18n': True,
                     'readonly_layout_modes': (),
                     'hidden_layout_modes': ('view',),
                     'hidden_readonly_layout_modes': (),
                     'hidden_empty': False,
                     'hidden_if_expr': '',
                     'css_class': '',
                     'widget_mode_expr': '',
                     'vocabulary': 'blog_categories',
                     'translated': True,
                },
            },
        },
    'layout': {
        'style_prefix': 'layout_default_',
        'ncols': 1,
        'rows': [
            [{'widget_id': 'body'}, ],
            [{'widget_id': 'Subject'}, ],
            ],
        },
    }

def getDocumentLayouts(portal=None):
    layouts = {}
    layouts['blog'] = blog_layout
    layouts['blog_entry'] = blog_entry_layout
    return layouts

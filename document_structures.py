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

from Products.CMFCore.CMFCorePermissions import View, ModifyPortalContent
from Products.CPSBlog.permissions import BlogEntryCreate

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
    'cps_display_as_document_in_listing': True,
    'schemas': ['metadata', 'common', 'blog'],
    'layouts': ['common', 'blog'],
    'flexible_layouts': [],
    'storage_methods': [],
    'cps_workspace_wf': 'blog_workspace_wf',
    'cps_section_wf': 'blog_section_wf',
    'use_content_status_history': 1,
    'actions': ({'id': 'view',
                 'name': 'action_view',
                 'action': 'blog_view',
                 'permissions': (View,)
                 },
                {'id': 'new_content',
                 'name': 'action_new_content',
                 'action': 'string:${object_url}/cpsdocument_create_form?type_name=BlogEntry',
                 'condition': '',
                 'permissions': (ModifyPortalContent, BlogEntryCreate)
                 },
                {'id': 'contents',
                 'name': 'action_folder_contents',
                 'action': 'string:${object_url}/folder_contents',
                 'condition' : '',
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
                 'action': 'string:${object_url}/blog_localrole_form',
                 'condition' : '',
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
    'schemas': ['metadata', 'blog_entry', 'blog_entry_flexible'],
    'layouts': ['common', 'blog_entry', 'blog_entry_flexible'],
    'flexible_layouts' : ['blog_entry_flexible:blog_entry_flexible'],
    'storage_methods': [],
    'cps_workspace_wf': 'blog_entry_wf',
    'cps_section_wf': 'blog_entry_wf',
    'use_content_status_history': 1,
    'actions': ({'id': 'view',
                 'name': 'action_view',
                 'action': 'blog_entry_view',
                 'permissions': (View,)
                 },
                {'id': 'new_content',
                 'name': 'action_new_content',
                 'action': 'string:${object_url}/folder_factories',
                 'condition': '',
                 'permissions': (ModifyPortalContent,)
                 },
                {'id': 'contents',
                 'name': 'action_folder_contents',
                 'action': 'string:${object_url}/folder_contents',
                 'condition' : '',
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
                 'condition' : '',
                 'permissions': ('Change permissions',)
                 })
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
    'author_photo' : {
        'type': 'CPS Image Field',
        'data': {'default_expr': 'nothing',
                 'is_searchabletext': 0,
                 },
        },
    }

blog_entry_schema = {
    'preview': {
        'type': 'CPS Image Field',
        'data': {
            'default_expr': 'nothing',
            'is_searchabletext': 0,
            'acl_read_permissions': '',
            'acl_read_roles': '',
            'acl_read_expr': '',
            'acl_write_permissions': '',
            'acl_write_roles': '',
            'acl_write_expr': '',
            'read_ignore_storage': 0,
            'read_process_expr': '',
            'read_process_dependent_fields': [],
            'write_ignore_storage': 0,
            'write_process_expr': '',
        },
    },
    'allow_discussion': {
        'type': 'CPS Int Field',
        'data': {
            'default_expr': 'python:1',
            'is_searchabletext': 0,
            'acl_read_permissions': '',
            'acl_read_roles': '',
            'acl_read_expr': '',
            'acl_write_permissions': '',
            'acl_write_roles': '',
            'acl_write_expr': '',
            'read_ignore_storage': 0,
            'read_process_expr': '',
            'read_process_dependent_fields': [],
            'write_ignore_storage': 0,
            'write_process_expr': '',
        },
    },
    'body' : {
        'type': 'CPS String Field',
        'data': {'default_expr': 'string:',
                 'is_searchabletext': 0,
                 },
        },
    }

blog_entry_flexible_schema = {
    }

def getDocumentSchemas(portal=None):
    schemas = {}
    schemas['blog'] = blog_schema
    schemas['blog_entry'] = blog_entry_schema
    schemas['blog_entry_flexible'] = blog_entry_flexible_schema
    return schemas


blog_view_mode_vocabulary = {
    'data': {
        'tuples':(
            ('title', 'Title', 'view_mode_Title_label'),
            ('title_desc', 'Title and Description',
             'view_mode_TitleDescription_label'),
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
                     'label_edit': 'blog_view_mode_label_edit',
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
        'author_photo': {
            'type': 'Photo Widget',
            'data': {'title': '',
                     'fields': ('author_photo',),
                     'is_required': False,
                     'label': '',
                     'label_edit': 'author_photo_label_edit',
                     'description': '',
                     'help': '',
                     'is_i18n': True,
                     'readonly_layout_modes': (),
                     'hidden_layout_modes': (),
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
        'style_prefix': 'layout_blog_',
        'ncols': 1,
        'rows': [
            [{'widget_id': 'view_mode'}],
            [{'widget_id': 'display_entries'}],
            [{'widget_id': 'author_photo'}],
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
                     'hidden_layout_modes': (),
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
                     'hidden_layout_modes': (),
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


blog_entry_flexible_layout = {
    'widgets': {
        'attachedFile': {
            'type': 'AttachedFile Widget',
            'data': {
                'title': 'cpsdoc_flex_attachedFile_title',
                'fields': ['?'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_flex_attachedFile_label_edit',
                'label': 'cpsdoc_flex_attachedFile_label',
                'css_class': 'ddefault',
                'hidden_empty': 1,
                'deletable': 1,
                'size_max': 4*1024*1024,
                },
            },
        'link': {
            'type': 'Link Widget',
            'data': {
                'title': 'cpsdoc_flex_link_title',
                'fields': ['?'],
                'is_i18n': 1,
                'css_class': 'ddefault',
                'label_edit': 'cpsdoc_Link_label_edit',
                'widget_ids': ['link_href',
                               'link_title',
                               'link_description'],
            },
        },
        'link_href': {
            'type': 'URL Widget',
            'data': {
                'fields': ['?'],
                'is_i18n': 1,
                'label_edit': 'cpsschemas_label_link_href',
                'display_width': 60,
            },
        },
        'link_title': {
            'type': 'String Widget',
            'data': {
                'fields': ['?'],
                'is_i18n': 1,
                'label_edit': 'cpsschemas_label_link_content',
                'display_width': 60,
                'size_max': 100,
            },
        },
        'link_description': {
            'type': 'TextArea Widget',
            'data': {
                'fields': ['?'],
                'is_i18n': 1,
                'label_edit': 'cpsschemas_label_link_title',
                'width': 60,
                'height': 3,
            },
        },
        },
    'layout': {
        'flexible_widgets': ['link', 'attachedFile'],
        'style_prefix': 'layout_default_',
        'ncols': 1,
        'rows': [
            ],
        },
    }

def getDocumentLayouts(portal=None):
    layouts = {}
    layouts['blog'] = blog_layout
    layouts['blog_entry'] = blog_entry_layout
    layouts['blog_entry_flexible'] = blog_entry_flexible_layout
    return layouts

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

from Products.CMFCore.permissions import View, ModifyPortalContent
from Products.CPSBlog.permissions import BlogEntryCreate

blog_type = {
    'title': "portal_type_Blog_title",
    'description': "portal_type_Blog_description",
    'content_icon': 'blog_icon.png',
    'content_meta_type': 'Blog',
    'product': 'CPSBlog',
    'factory': 'addBlog',
    'immediate_view': 'blog_view',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': ['BlogEntry'],
    'allow_discussion': 1,
    'cps_is_searchable': 1,
    # Choose between 'document', 'folder' or 'folderishdocument'
    # according to the need to store objects in your document or not.
    'cps_proxy_type': 'btreefolderishdocument',
    'cps_display_as_document_in_listing': True,
    'schemas': ['metadata', 'common', 'blog'],
    'layouts': ['blog'],
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
                 'action': 'string:${object_url}/blog_entry_create_form?type_name=BlogEntry',
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
                {'id': 'categories',
                 'name': 'action_manage_blog_categories',
                 'action': 'string:${object_url}/blog_manage_categories',
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
    'factory': 'addBlogEntry',
    'immediate_view': '',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': [],
    'allow_discussion': 1,
    'cps_is_searchable': 1,
    # Choose between 'document', 'folder' or 'folderishdocument'
    # according to the need to store objects in your document or not.
    'cps_proxy_type': 'document',
    'schemas': ['metadata', 'blog_entry', 'blog_entry_flexible'],
    'layouts': ['blog_entry', 'blog_entry_flexible'],
    'flexible_layouts' : ['blog_entry_flexible:blog_entry_flexible'],
    'storage_methods': [],
    'cps_workspace_wf': 'blog_entry_wf',
    'cps_section_wf': 'blog_entry_wf',
    'use_content_status_history': 1,
    'actions': ({'id': 'create',
                 'name': 'action_create',
                 'action': 'string:${object_url}/blog_entry_create_form',
                 'condition': '',
                 'permission': (ModifyPortalContent,),
                 'category': 'object',
                 'visible': 0
                 },
                {'id': 'view',
                 'name': 'action_view',
                 'action': 'blog_entry_view',
                 'permissions': (View,)
                 },
                {'id': 'new_content',
                 'name': 'action_new_content',
                 'action': 'string:${object_url}/folder_factories',
                 'condition': '',
                 'permissions': (ModifyPortalContent,),
                 'visible' : 0
                 },
                {'id': 'contents',
                 'name': 'action_folder_contents',
                 'action': 'string:${object_url}/folder_contents',
                 'condition' : '',
                 'permissions': (ModifyPortalContent,),
                 'visible' : 0
                 },
                {'id': 'edit',
                 'name': 'action_edit',
                 'action': 'string:${object_url}/blog_entry_edit_form',
                 'condition' : '',
                 'permissions': (ModifyPortalContent,)
                 },
                {'id': 'metadata',
                 'name': 'action_metadata',
                 'action': 'string:${object_url}/cpsdocument_metadata',
                 'condition' : 'not:portal/portal_membership/isAnonymousUser',
                 'permissions': (View,),
                 'visible' : 0
                 },
                {'id': 'localroles',
                 'name': 'action_local_roles',
                 'action': 'string:${object_url}/folder_localrole_form',
                 'condition' : '',
                 'permissions': ('Change permissions',),
                 'visible' : 0
                 })
    }


blogaggregator_type = {
    'title': "portal_type_BlogAggregator_title",
    'description': "portal_type_BlogAggregator_description",
    'content_icon': 'blogaggregator_icon.png',
    'content_meta_type': 'BlogAggregator',
    'product': 'CPSBlog',
    'factory': 'addBlogAggregator',
    'immediate_view': 'blogaggregator_view',
    'global_allow': 1,
    'filter_content_types': 1,
    'allowed_content_types': [],
    'allow_discussion': 0,
    'cps_is_searchable': 1,
    # Choose between 'document', 'folder' or 'folderishdocument'
    # according to the need to store objects in your document or not.
    'cps_proxy_type': 'folderishdocument',
    'cps_display_as_document_in_listing': True,
    'schemas': ['metadata', 'common', 'blogaggregator'],
    'layouts': ['common', 'blogaggregator'],
    'flexible_layouts': [],
    'storage_methods': [],
    'cps_workspace_wf': 'workspace_folder_wf',
    'cps_section_wf': 'section_folder_wf',
    'use_content_status_history': 1,
    'actions': ({'id': 'view',
                 'name': 'action_view',
                 'action': 'blogaggregator_view',
                 'permissions': (View,)
                 },
                {'id': 'edit',
                 'name': 'action_edit',
                 'action': 'string:${object_url}/cpsdocument_edit_form',
                 'condition' : '',
                 'permissions': (ModifyPortalContent,)
                 })
    }


def getDocumentTypes(portal=None):
    types = {}
    types['Blog'] = blog_type
    types['BlogEntry'] = blog_entry_type
    types['BlogAggregator'] = blogaggregator_type
    return types


blog_schema = {
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
    'author_photo' : {
        'type': 'CPS Image Field',
        'data': {'default_expr': 'nothing',
                 'is_searchabletext': 0,
                 },
        },
    'langs': {
        'type': 'CPS String List Field',
        'data': {'default_expr': 'string:',
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
    'content' : {
        'type': 'CPS String Field',
        'data': {'default_expr': 'string:',
                 'is_searchabletext': 1,
                 },
        },
    'lang': {
        'type': 'CPS String Field',
        'data': {'default_expr': 'string:',
                 'is_searchabletext': 0,
                 },
        },
    'accept_trackback_pings': {
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
    'dispatch_trackback_urls': {
        'type': 'CPS String List Field',
        'data': {
            'default_expr': 'string:',
            'is_searchabletext': 0,
            'acl_read_permissions': '',
            'acl_read_roles': '',
            'acl_read_expr': '',
            'acl_write_permissions': '',
            'acl_write_roles': '',
            'acl_write_expr': '',
            'read_ignore_storage': 0,
            'read_process_expr': 'string:',
            'read_process_dependent_fields': [],
            'write_ignore_storage': 0,
            'write_process_expr': '',
            },
        },
    }

blog_entry_flexible_schema = {
    }

blogaggregator_schema = {
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

def getDocumentSchemas(portal=None):
    schemas = {}
    schemas['blog'] = blog_schema
    schemas['blog_entry'] = blog_entry_schema
    schemas['blog_entry_flexible'] = blog_entry_flexible_schema
    schemas['blogaggregator'] = blogaggregator_schema
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

blog_glob_categories_vocabulary = {
    'data': {
#        'tuples':((), ),
        },
    }

blogaggregator_status_vocabulary = {
    'data': {
        'tuples':(
            ('published', 'Published', 'label_published'),
            ('work', 'Work', 'label_work'),
            ),
        },
    }

blogaggregator_modified_vocabulary = {
    'data': {
        'tuples':(
            ('', 'Choose', 'label_choose'),
            ('time_last_login', 'Last login', 'time_last_login'),
            ('time_yesterday', 'Yesterday',  'time_yesterday'),
            ('time_last_week', 'Last week', 'time_last_week'),
            ('time_last_month', 'Last month', 'time_last_month'),
            ),
        },
    }

blogaggregator_sort_by_vocabulary = {
    'data': {
        'tuples':(
            ('', "No sort", "label_sort_by"),
            ('title_asc', "Title ascending", "label_title_asc"),
            ('title_desc', "Title descending", "label_title_desc"),
            ('date_asc', "Date ascending", "label_date_effective_asc"),
            ('date_desc', "Date descending", "label_date_effective_desc"),
            ('status_asc', "Status ascending", "label_status_asc"),
            ('status_desc', "Status descending", "label_status_desc"),
            ),
        },
    }

blogaggregator_categories_voc = {
    'type' : 'CPS Method Vocabulary',
    'data': {'get_vocabulary_method' : 'getVocBlogAggregatorCategories',
             },
    }

blog_categories_vocabulary = {
    'type' : 'CPS Method Vocabulary',
    'data': {'get_vocabulary_method' : 'getVocBlogCategories',
             },
    }

blog_languages_vocabulary = {
    'type' : 'CPS Method Vocabulary',
    'data': {'get_vocabulary_method' : 'getVocBlogLanguages',
             },
    }

def getDocumentVocabularies(portal=None):
    vocabularies = {}
    vocabularies['blog_view_mode'] = blog_view_mode_vocabulary
    vocabularies['blog_glob_categories'] = blog_glob_categories_vocabulary
    vocabularies['blog_categories'] = blog_categories_vocabulary
    vocabularies['blog_languages'] = blog_languages_vocabulary
    vocabularies['blogaggregator_status'] = blogaggregator_status_vocabulary
    vocabularies['blogaggregator_modified'] = blogaggregator_modified_vocabulary
    vocabularies['blogaggregator_sort_by'] = blogaggregator_sort_by_vocabulary
    vocabularies['blogaggregator_categories'] = blogaggregator_categories_voc
    return vocabularies


blog_layout = {
    'widgets': {
        'LanguageSelector': {
            'type': 'Document Language Select Widget',
            'data': {
                'fields': ['Language'],
            },
        },
        'Title': {
            'type': 'Heading Widget',
            'data': {
                'fields': ['Title'],
                'level': 1,
                'is_i18n': 1,
                'is_required': 1,
                'label_edit': 'cpsdoc_title_label_edit',
                'display_width': 72,
                'size_max': 200,
            },
        },
        'Description': {
            'type': 'Text Widget',
            'data': {
                'fields': ['Description'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_description_label_edit',
                'label': '',
                'css_class': 'ddescription',
                'width': 72,
                'height': 5,
                'render_format': 'text',
            },
        },
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
        'entries_per_page': {
            'type': 'Int Widget',
            'data': {'title': '',
                     'fields': ('entries_per_page',),
                     'is_required': False,
                     'label': '',
                     'label_edit': 'blog_entries_per_page_label_edit',
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
                     'render_position' : 'right',
                     'widget_mode_expr': '',
                     'translated': True,
                },
            },
        'langs': {
            'type': 'MultiSelect Widget',
            'data': {'title': '',
                     'fields': ('langs',),
                     'is_required': False,
                     'label': '',
                     'label_edit': 'blog_languages_label_edit',
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
                     'vocabulary': 'language_voc',
                     'translated': True,
                },
            },
        },
    'layout': {
        'style_prefix': 'layout_blog_',
        'ncols': 1,
        'rows': [
            [{'widget_id': 'LanguageSelector'}],
            [{'widget_id': 'Title'},],
            [{'widget_id': 'Description'},],
            [{'widget_id': 'view_mode'}],
            [{'widget_id': 'entries_per_page'}],
            [{'widget_id': 'author_photo'}],
            [{'widget_id': 'langs'}],
            ],
        },
    }

blog_entry_layout = {
    'widgets': {
        'LanguageSelector': {
            'type': 'Document Language Select Widget',
            'data': {
                'fields': ['Language'],
            },
        },
        'Title': {
            'type': 'Heading Widget',
            'data': {
                'fields': ['Title'],
                'level': 1,
                'is_i18n': 1,
                'is_required': 1,
                'label_edit': 'cpsdoc_title_label_edit',
                'display_width': 72,
                'size_max': 250,
            },
        },
        'Description': {
            'type': 'Text Widget',
            'data': {
                'fields': ['Description'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_description_label_edit',
                'label': '',
                'hidden_layout_modes': ('view', 'create', 'edit'),
                'css_class': 'ddescription',
                'width': 72,
                'height': 5,
                'render_format': 'text',
            },
        },
        'content': {
            'type': 'Rich Text Editor Widget',
            'data': {'title': '',
                     'fields': ('content',),
                     'is_required': True,
                     'label': '',
                     'label_edit': 'blog_entry_content_label_edit',
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
                     'label_edit': 'blog_entry_categories_label_edit',
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
                     'translated': False,
                },
            },
        'lang': {
            'type': 'Select Widget',
            'data': {'title': '',
                     'fields': ('Language',),
                     'is_required': False,
                     'label': '',
                     'label_edit': 'label_language',
                     'description': '',
                     'help': '',
                     'is_i18n': True,
                     'hidden_layout_modes': ('view',),
                     'hidden_readonly_layout_modes': (),
                     'hidden_empty': False,
                     'hidden_if_expr': '',
                     'readonly_layout_modes': ('edit', ),
                     'css_class': '',
                     'widget_mode_expr': '',
                     'vocabulary': 'blog_languages',
                     'translated': True,
                },
            },
        'accept_trackback_pings': {
            'type': 'Boolean Widget',
            'data': {'title': '',
                     'fields': ('accept_trackback_pings',),
                     'is_required': False,
                     'label': '',
                     'label_edit': 'blog_entry_accept_pings_label_edit',
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
        'dispatch_trackback_urls': {
            'type': 'Lines Widget',
            'data': {'title': '',
                     'fields': ('dispatch_trackback_urls',),
                     'is_required': False,
                     'label': '',
                     'label_edit': 'blog_entry_dispatch_tb_urls_label_edit',
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
        },
    'layout': {
        'style_prefix': 'layout_blog_entry_',
        'ncols': 2,
        'rows': [
            [{'widget_id': 'LanguageSelector'}],
            [{'widget_id': 'Title'},],
            [{'widget_id': 'content'},],
            [{'widget_id': 'lang'},
             {'widget_id': 'accept_trackback_pings'}],
            [{'widget_id': 'Subject'},
             {'widget_id': 'dispatch_trackback_urls'}],
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
        'photo': {
            'type': 'Photo Widget',
            'data': {
                'title': 'cpsdoc_flex_photo_title',
                'fields': ['?'],
                'is_i18n': 1,
                'label_edit': 'cpsdoc_flex_photo_label_edit',
                'configurable': 'position',
                'display_width': 320,
                'display_height': 200,
                'size_max': 2*1024*1024,
                'allow_resize': 1,
            },
        },
        },
    'layout': {
        'flexible_widgets': ['link', 'attachedFile', 'photo'],
        'style_prefix': 'layout_blog_entry_',
        'ncols': 1,
        'rows': [
            ],
        },
    }


blogaggregator_layout = {
    'widgets': {
        'query_title': {
            'type': 'String Widget',
            'data': {'title': '',
                     'fields': ('query_title',),
                     'is_required': False,
                     'label': '',
                     'label_edit': 'label_search_title',
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
        'query_description': {
            'type': 'String Widget',
            'data': {'title': '',
                     'fields': ('query_description',),
                     'is_required': False,
                     'label': '',
                     'label_edit': 'label_search_description',
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
        'query_fulltext': {
            'type': 'String Widget',
            'data': {'title': '',
                     'fields': ('query_fulltext',),
                     'is_required': False,
                     'label': '',
                     'label_edit': 'label_search_full_text',
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
        'query_categories': {
            'type': 'MultiSelect Widget',
            'data': {'title': '',
                     'fields': ('query_categories',),
                     'is_required': False,
                     'label': '',
                     'label_edit': 'blog_entry_categories_label_edit',
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
                     'vocabulary': 'blogaggregator_categories',
                     'translated': False,
                },
            },
        'query_modified': {
            'type': 'Select Widget',
            'data': {'title': '',
                     'fields': ('query_modified',),
                     'is_required': False,
                     'label': '',
                     'label_edit': 'label_search_modified_since',
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
                     'vocabulary': 'blogaggregator_modified',
                     'translated': True,
                },
            },
        'query_status': {
            'type': 'Select Widget',
            'data': {'title': '',
                     'fields': ('query_status',),
                     'is_required': False,
                     'label': '',
                     'label_edit': 'label_search_status',
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
                     'vocabulary': 'blogaggregator_status',
                     'translated': True,
                },
            },
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
        'entries_per_page': {
            'type': 'Int Widget',
            'data': {'title': '',
                     'fields': ('entries_per_page',),
                     'is_required': False,
                     'label': '',
                     'label_edit': 'blog_entries_per_page_label_edit',
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
        'sort_by': {
            'type': 'Select Widget',
            'data': {'title': '',
                     'fields': ('sort_by',),
                     'is_required': False,
                     'label': '',
                     'label_edit': 'label_sort_by',
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
                     'vocabulary': 'blogaggregator_sort_by',
                     'translated': True,
                },
            },
        },
    'layout': {
        'style_prefix': 'layout_blogaggregator_',
        'ncols': 1,
        'rows': [
            [{'widget_id': 'query_title'}],
            [{'widget_id': 'query_description'}],
            [{'widget_id': 'query_fulltext'}],
            [{'widget_id': 'query_categories'}],
            [{'widget_id': 'query_modified'}],
            [{'widget_id': 'query_status'}],
            [{'widget_id': 'view_mode'}],
            [{'widget_id': 'entries_per_page'}],
            [{'widget_id': 'sort_by'}],
            ],
        },
    }

def getDocumentLayouts(portal=None):
    layouts = {}
    layouts['blog'] = blog_layout
    layouts['blog_entry'] = blog_entry_layout
    layouts['blog_entry_flexible'] = blog_entry_flexible_layout
    layouts['blogaggregator'] = blogaggregator_layout
    return layouts

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

"""
CPSBlog Installer

How to use the CPSBlog installer :
 - Log into the ZMI as manager
 - Go to your CPS root directory
 - Create an External Method with the following parameters:

     id            : cpsblog_install (or whatever)
     title         : CPSBlog Install (or whatever)
     Module Name   : CPSBlog.install
     Function Name : install

 - save it
 - then click on the test tab of this external method

Or use CMFQuickInstaller...
"""

from Products.CPSBlog.document_structures import \
     getDocumentTypes, getDocumentSchemas, getDocumentLayouts, \
     getDocumentVocabularies
from Products.CPSInstaller.CPSInstaller import CPSInstaller
from Products.CMFCore.CMFCorePermissions import \
     View, ModifyPortalContent, ManageProperties
from Products.CPSWorkflow.CPSWorkflowTransitions import \
     TRANSITION_INITIAL_CREATE, \
     TRANSITION_ALLOWSUB_CREATE, \
     TRANSITION_ALLOWSUB_COPY, \
     TRANSITION_ALLOWSUB_MOVE, \
     TRANSITION_ALLOWSUB_DELETE
from Products.DCWorkflow.Transitions import TRIGGER_USER_ACTION, \
     TRIGGER_AUTOMATIC
from Products.CPSBlog.permissions import BlogEntryCreate
from Products.PythonScripts.PythonScript import PythonScript

WebDavLockItem = 'WebDAV Lock items'
WebDavUnlockItem = 'WebDAV Unlock items'

LAYERS = {
    'cpsblog': 'Products/CPSBlog/skins/cpsblog',
    }

class ClientInstaller(CPSInstaller):

    product_name = 'CPSBlog'

    def install(self):
        """Converting a CPS Default Site to a client site"""
        self.log("Starting %s installation" % self.product_name)

        #################################################
        # CPSBlog-specific roles and permissions
        #################################################
        self.log("Verifying CPSBlog permissions")
        forum_perms = {
             BlogEntryCreate: ('Manager', 'Owner', 'WorkspaceManager',
                               'BlogPoster', 'SectionManager',
                               'SectionReviewer',
                               ),
             }

        self.verifyRoles(('BlogPoster',))
        self.setupPortalPermissions(forum_perms)

        # The product skins have to be set up AFTER the cpsdefault_installer
        # is run, because the product skins override the cpsdefault skins.
        #self.setupCps()

        self.log("Installing layers and configure Basic skin")
        self.verifySkins(LAYERS)

        self.log("Installing custom types")
        custom_types = getDocumentTypes(self.portal)
        self.log("custom types = %s" % str(custom_types))
        self.verifyFlexibleTypes(custom_types)

        self.log("Installing custom schemas")
        custom_schemas = getDocumentSchemas(self.portal)
        self.log("custom schemas = %s" % str(custom_schemas))
        self.verifySchemas(custom_schemas)

        self.log("Installing custom layouts")
        custom_layouts = getDocumentLayouts(self.portal)
        self.verifyLayouts(custom_layouts)

        self.log("Installing custom vocabularies")
        vocabularies = getDocumentVocabularies(self.portal)
        self.verifyVocabularies(vocabularies)

        self.allowContentTypes(('Blog', 'BlogAggregator'),
                               ('Workspace', 'Section'))

        self.setupBoxes()

        ########################################
        # WORKFLOW DEFINITION
        ########################################

        wfscripts = {
            'add_blog_boxes': {
            '_owner': None,
            'script': """
##parameters=state_change
blog_proxy = state_change.object
blog_rel_url = context.portal_url.getRelativeContentURL(blog_proxy)
kw = {'type_name' : 'Blog Calendar Box',
      'slot_name' : 'right',
      'title' : blog_proxy.Title(),
      'events_in' : blog_rel_url,
      'event_types' : ('BlogEntry', ),
      'box_skin': 'here/box_lib/macros/wbox2'
      }
blog_proxy.box_create(**kw)

# Search box
kw = {'type_name' : 'Base Box',
      'slot_name' : 'right',
      'title' : 'Search',
      'provider' : 'cpsblog',
      'btype' : 'blogsearch',
      'box_skin': 'here/box_lib/macros/sbox'
      }
blog_proxy.box_create(**kw)

# Archives box
kw = {'type_name' : 'Base Box',
      'slot_name' : 'right',
      'title' : 'Archives',
      'provider' : 'cpsblog',
      'btype' : 'blogarchive',
      'box_skin': 'here/box_lib/macros/sbox'
      }
blog_proxy.box_create(**kw)
            """
            },
            }

        # Workspace workflow for Blog
        wfdef = {'wfid': 'blog_workspace_wf',
                 'permissions': (View, ModifyPortalContent,
                                 WebDavLockItem, WebDavUnlockItem,)
                 }

        wfstates = {
            'work': {
                'title': 'Work',
                'transitions':('create_content', 'cut_copy_paste'),
                'permissions': {View: ('Manager', 'WorkspaceManager',
                                       'WorkspaceMember', 'WorkspaceReader',
                                       'BlogPoster'),
                                ModifyPortalContent: ('Manager', 'Owner',
                                                      'WorkspaceManager')},
                },
            }

        wftransitions = {
            'cut_copy_paste': {
                'title': 'Cut/Copy/Paste',
                'new_state_id': '',
                'transition_behavior': (TRANSITION_ALLOWSUB_DELETE,
                                        TRANSITION_ALLOWSUB_MOVE,
                                        TRANSITION_ALLOWSUB_COPY),
                'clone_allowed_transitions': None,
                'trigger_type': TRIGGER_USER_ACTION,
                'actbox_name': '',
                'actbox_category': '',
                'actbox_url': '',
                'props': {'guard_permissions':'',
                          'guard_roles':'Manager; WorkspaceManager; '
                                        'WorkspaceMember',
                          'guard_expr':''},
                },
            'create': {
                'title': 'Initial creation',
                'new_state_id': 'work',
                'transition_behavior': (TRANSITION_INITIAL_CREATE,),
                'clone_allowed_transitions': None,
                'actbox_category': 'workflow',
                'after_script_name' : 'add_blog_boxes',
                'props': {'guard_permissions':'',
                          'guard_roles':'Manager; WorkspaceManager; '
                                        'WorkspaceMember',
                          'guard_expr':''},
                },
            'create_content': {
                'title': 'Create content',
                'new_state_id': 'work',
                'transition_behavior': (TRANSITION_ALLOWSUB_CREATE,),
                'clone_allowed_transitions': None,
                'trigger_type': TRIGGER_USER_ACTION,
                'actbox_name': '',
                'props': {'guard_permissions':'Create Blog Entry',
                          'guard_roles':'',
                          'guard_expr':''},
                },
            }
        self.verifyWorkflow(wfdef, wfstates, wftransitions, wfscripts, {})

        # Section workflow for Blog
        wfdef = {'wfid': 'blog_section_wf',
                 'permissions': (View, ModifyPortalContent)}

        wfstates = {
            'work': {
                'title': 'Work',
                'transitions': ('create_content', 'cut_copy_paste'),
                'permissions': {View: ('Manager', 'SectionManager',
                                       'SectionReviewer', 'SectionReader',
                                       'BlogPoster'),
                                ModifyPortalContent: ('Manager', 'Owner',
                                                      'SectionManager',
                                                      'SectionReviewer')},
                },
            }

        wftransitions = {
            'cut_copy_paste': {
                'title': 'Cut/Copy/Paste',
                'new_state_id': '',
                'transition_behavior': (TRANSITION_ALLOWSUB_DELETE,
                                        TRANSITION_ALLOWSUB_MOVE,
                                        TRANSITION_ALLOWSUB_COPY),
                'clone_allowed_transitions': None,
                'trigger_type': TRIGGER_USER_ACTION,
                'actbox_name': '',
                'actbox_category': '',
                'actbox_url': '',
                'props': {'guard_permissions': '',
                          'guard_roles': 'Manager; SectionManager; '
                                         'SectionReviewer; SectionReader',
                          'guard_expr': ''},
                },
            'create': {
                'title': 'Initial creation',
                'new_state_id': 'work',
                'transition_behavior': (TRANSITION_INITIAL_CREATE,),
                'clone_allowed_transitions': None,
                'actbox_category': 'workflow',
                'after_script_name' : 'add_blog_boxes',
                'props': {'guard_permissions': '',
                          'guard_roles': 'Manager; SectionManager',
                          'guard_expr': ''},
                },
            'create_content': {
                'title': 'Create content',
                'new_state_id': 'work',
                'transition_behavior': (TRANSITION_ALLOWSUB_CREATE,),
                'clone_allowed_transitions': None,
                'trigger_type': TRIGGER_USER_ACTION,
                'props': {'guard_permissions': 'Create Blog Entry',
                          'guard_roles': '',
                          'guard_expr': ''},
                },
            }
        self.verifyWorkflow(wfdef, wfstates, wftransitions, wfscripts, {})

        # workflow for BlogEntry
        wfdef = {'wfid': 'blog_entry_wf',
                 'permissions': (View, ModifyPortalContent,
                                 WebDavLockItem, WebDavUnlockItem,)
                 }

        wfstates = {
            'work': {'title': 'Work',
                     'transitions':('publish',),
                     'permissions': {View: ('Manager', 'Owner',
                                            'WorkspaceManager',
                                            'SectionManager',
                                            'SectionReviewer',
                                            'BlogPoster'),
                                     ModifyPortalContent: ('Manager',
                                                           'Owner',
                                                           'WorkspaceManager',
                                                           'SectionManager',
                                                           'SectionReviewer')}
                     },
            'published': {'title': 'Published',
                          'transitions':('unpublish', ),
                          'permissions': {View: ('Manager', 'SectionManager',
                                                 'SectionReviewer',
                                                 'SectionReader',
                                                 'WorkspaceManager',
                                                 'WorkspaceMember',
                                                 'BlogPoster')}
                          },
            }

        wftransitions = {
            'create': {
                'title': 'Initial creation',
                'new_state_id': 'work',
                'transition_behavior': (TRANSITION_INITIAL_CREATE,),
                'clone_allowed_transitions': None,
                'actbox_category': 'workflow',
                'props': {'guard_permissions':'Create Blog Entry',
                          'guard_roles':'',
                          'guard_expr':''},
                },
            'publish': {
                'title': 'Publish BlogEntry',
                'new_state_id': 'published',
                'transition_behavior': (),
                'clone_allowed_transitions': None,
                'trigger_type': TRIGGER_USER_ACTION,
                'actbox_name': 'Publish',
                'actbox_category': 'workflow',
                'actbox_url': '%(content_url)s/blog_entry_publish',
                'props': {'guard_permissions':'',
                          'guard_roles':'Manager; SectionManager; '
                                        'SectionReviewer; BlogPoster; '
                                        'WorkspaceManager; WorkspaceMember',
                          'guard_expr':''},
                },
            'unpublish': {
                'title': 'Unpublish BlogEntry',
                'new_state_id': 'work',
                'transition_behavior': (),
                'clone_allowed_transitions': None,
                'trigger_type': TRIGGER_USER_ACTION,
                'actbox_name': 'Unpublish',
                'actbox_category': 'workflow',
                'actbox_url': '%(content_url)s/blog_entry_unpublish',
                'props': {'guard_permissions':'',
                          'guard_roles':'Manager; SectionManager; '
                                        'SectionReviewer; BlogPoster; '
                                        'WorkspaceManager; WorkspaceMember',
                          'guard_expr':''},
                },
            }
        self.verifyWorkflow(wfdef, wfstates, wftransitions, {}, {})

        ########################################
        #   WORKFLOW ASSOCIATIONS
        ########################################
        ws_chains = { 'Blog': 'blog_workspace_wf',
                      'BlogEntry': 'blog_entry_wf',
                      'BlogAggregator' : 'workspace_folder_wf'}
        se_chains = { 'Blog': 'blog_section_wf',
                      'BlogEntry': 'blog_entry_wf',
                      'BlogAggregator' : 'section_folder_wf'}

        self.verifyLocalWorkflowChains(self.portal['workspaces'],
                                       ws_chains, destructive=1)
        self.verifyLocalWorkflowChains(self.portal['sections'],
                                       se_chains, destructive=1)

        self.setupNeededProducts()
        self.setupTranslations()

        # set custom actions and action icons
        self.setupActions()

        self.log("Ending %s installation" % self.product_name)

    def setupCps(self):
        # Calling the CPS installer
        self.log("")
        self.log("### CPS update")
        self.log(self.portal.cpsupdate())
        self.log("### End of CPS update")

    def setupNeededProducts(self):
        self.log("%s.setupNeededProducts()" % self.product_name)
        self.log("### CPSSubscriptions setup ###")
        try:
            import Products.CPSSubscriptions
            methodName = 'cpssubscriptions_install'
            if not self.portalHas(methodName):
                self.log('Adding CPSSubscriptions installer')
                from Products.ExternalMethod.ExternalMethod import ExternalMethod
                method = ExternalMethod(methodName,
                                        'CPSSubscriptions install',
                                        'CPSSubscriptions.install',
                                        'install')
                self.portal._setObject(methodName, method)
            self.log(self.portal.cpssubscriptions_install())
        except ImportError:
            self.log("Could not import CPSSubscriptions")
            pass
        self.log("### End of CPSSubscriptions setup ###")

    def setupBoxes(self):
        from Products.CPSBlog.BlogCalendarBox import factory_type_information
        blogcalendarbox_fti = factory_type_information[0]

        types = (
            {'id' : blogcalendarbox_fti['id'],
             'meta_type' : blogcalendarbox_fti['meta_type'],
             'title' : blogcalendarbox_fti['title'],
             'description' : blogcalendarbox_fti['description']
             },
            )

        ttool = self.portal.portal_types
        ptypes = ttool.objectIds()

        for boxtype in types:
            boxid = boxtype['id']
            if boxid in ptypes:
                self.log('Deleted Box ' + boxid)
                ttool.manage_delObjects(boxid)
            self.log('Adding Box ' + boxid)
            ttool.manage_addTypeInformation(
                id=boxid,
                add_meta_type='Factory-based Type Information',
                typeinfo_name='CPSBlog: ' + boxid,
                )
            ttool.manage_changeProperties(
                title=boxtype['title'],
                description=boxtype['description'],
                content_meta_type=boxtype['meta_type'],
                )

    def setupActions(self):
        from Products.CPSSubscriptions.CPSSubscriptionsPermissions import \
             CanNotifyContent

        try:
            ai = self.portal.portal_actionicons
        except AttributeError:
            self.log('CMFActionIcons is not installed!')
            return

        at = self.portal.portal_actions

        document_actions = (
            ('document_actions', 'print'),
            ('document_actions', 'mnotify'),
            ('document_actions', 'rss'),
            )

        _ac = at._cloneActions()
        _acn = []

        for action in _ac:
            if (action.category, action.id) in document_actions:
                continue
            _acn.append(action)

        at._actions = tuple(_acn)

        at.addAction('print',
                     name='Print this page',
                     action='string:javascript:this.print();',
                     condition='',
                     permission='View',
                     category='document_actions')
        at.addAction('mnotify',
                     name='Send a mail notification',
                     action='string:$object_url/content_notify_email_form',
                     condition="python:object.portal_type != 'Portal'",
                     permission=(CanNotifyContent,),
                     category='document_actions')
        at.addAction('rss',
                     name='RSS feed',
                     action='string:$object_url/exportrss',
                     condition='',
                     permission='View',
                     category='document_actions')

        ai_actions = (
            ('cps', 'print', 'print_icon.gif', 'Print'),
            ('cps', 'mnotify', 'mail_icon.gif', 'Mail Notify'),
            ('cps', 'rss', 'rss.gif', 'RSS')
            )

        for action in ai_actions:
            if ai.queryActionIcon(*action[:2]) is None:
                ai.addActionIcon(*action)


def install(self):
    """Installation function for use by a Zope External Method

    @return: C{None}
    @rtype: C{None}

    @param self: CPSPortal Linked by External Method
    @type self: L{CPSDefaultSite}
    """

    installer = ClientInstaller(self)

    installer.install()

    return installer.logResult()

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

"""
CPSBlog Installer

Howto use the CPSBlog installer :
 - Log into the ZMI as manager
 - Go to your CPS root directory
 - Create an External Method with the following parameters:

     id            : cpsblog_install (or whatever)
     title         : CPSBlog Install (or whatever)
     Module Name   : CPSBlog.install
     Function Name : install

 - save it
 - then click on the test tab of this external method
"""

from Products.CPSBlog.document_structures import \
     getDocumentTypes, getDocumentSchemas, getDocumentLayouts, \
     getDocumentVocabularies
from Products.CPSInstaller.CPSInstaller import CPSInstaller
from Products.CMFCore.CMFCorePermissions import \
     View, ModifyPortalContent, ManageProperties
from Products.CPSCore.CPSWorkflow import \
     TRANSITION_INITIAL_PUBLISHING, TRANSITION_INITIAL_CREATE, \
     TRANSITION_ALLOWSUB_CREATE, TRANSITION_ALLOWSUB_PUBLISHING, \
     TRANSITION_BEHAVIOR_PUBLISHING, TRANSITION_BEHAVIOR_FREEZE, \
     TRANSITION_BEHAVIOR_DELETE, TRANSITION_BEHAVIOR_MERGE, \
     TRANSITION_ALLOWSUB_CHECKOUT, TRANSITION_INITIAL_CHECKOUT, \
     TRANSITION_BEHAVIOR_CHECKOUT, TRANSITION_ALLOW_CHECKIN, \
     TRANSITION_BEHAVIOR_CHECKIN, TRANSITION_ALLOWSUB_DELETE, \
     TRANSITION_ALLOWSUB_MOVE, TRANSITION_ALLOWSUB_COPY
from Products.DCWorkflow.Transitions import TRIGGER_USER_ACTION, \
     TRIGGER_AUTOMATIC

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

        self.allowContentTypes(('Blog', 'BlogEntry'), ('Workspace', 'Section'))

        ########################################
        # WORKFLOW DEFINITION
        ########################################

        # workflow for BlogEntry
        wfdef = {'wfid': 'blog_entry_wf',
                 'permissions': (View, ModifyPortalContent,
                                 WebDavLockItem, WebDavUnlockItem,)
                 }

        wfstates = {
            'work': {'title': 'Work',
                     'transitions':('publish',),
                     'permissions': {View: ('Manager', 'WorkspaceManager',
                                            'WorkspaceMember',
                                            'WorkspaceReader')}
                     },
            'published': {'title': 'Published',
                          'transitions':('unpublish', ),
                          'permissions': {View: ('Manager', 'WorkspaceManager',
                                                 'WorkspaceMember',
                                                 'WorkspaceReader')}
                          },
            }

        wftransitions = {
            'create': {
                'title': 'Initial creation',
                'new_state_id': 'work',
                'transition_behavior': (TRANSITION_INITIAL_CREATE,),
                'clone_allowed_transitions': None,
                'actbox_category': 'workflow',
                'props': {'guard_permissions':'',
                          'guard_roles':'Manager; WorkspaceManager; WorkspaceMember',
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
                          'guard_roles':'Manager; WorkspaceManager; WorkspaceMember',
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
                          'guard_roles':'Manager; WorkspaceManager; '
                          'WorkspaceMember',
                          'guard_expr':''},
                },
            }
        self.verifyWorkflow(wfdef, wfstates, wftransitions, {}, {})


        ########################################
        #   WORKFLOW ASSOCIATIONS
        ########################################
        ws_chains = { 'Blog': 'workspace_folderish_content_wf',
                      'BlogEntry': 'blog_entry_wf'}
        se_chains = { 'Blog': 'section_folder_wf',
                      'BlogEntry': 'blog_entry_wf'}

        self.verifyLocalWorkflowChains(self.portal['workspaces'],
                                       ws_chains, destructive=1)
        self.verifyLocalWorkflowChains(self.portal['sections'],
                                       se_chains, destructive=1)

        self.setupNeededProducts()
        self.setupTranslations()

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

# $Id$

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
import CPSBlogTestCase

class TestGlobalInstall(CPSBlogTestCase.CPSBlogTestCase):

    def afterSetUp(self):
        self.login('manager')
        #from Products.ExternalMethod.ExternalMethod import ExternalMethod
        #installer = ExternalMethod('cpsblog_installer', 'CPSBlog Install',
        #                           'CPSBlog.install', 'install')
        #self.portal._setObject('cpsblog_installer', installer)
        #self.portal.cpsblog_installer()

    def beforeTearDown(self):
        self.logout()

    def testInstallerScript(self):
        self.assert_('cpsblog_installer' in self.portal.objectIds(),
                     'Installer script was not correctly added to portal')

    def testCPSBlogPortalTypes(self):
        ttool = self.portal.portal_types
        self.assert_('Blog' in ttool.objectIds(),
                     'Blog type is not in portal_types')
        self.assert_('BlogEntry' in ttool.objectIds(),
                     'BlogEntry type is not in portal_types')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestGlobalInstall))
    return suite

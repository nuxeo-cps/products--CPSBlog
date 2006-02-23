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

    def testPortalTypes(self):
        ttool = self.portal.portal_types
        portal_types = ['Blog', 'BlogEntry', 'BlogAggregator',
                        'BlogAggregator Portlet']
        for portal_type in portal_types:
            self.assert_(portal_type in ttool.objectIds(),
                         '%s is not in portal_types' % portal_type)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestGlobalInstall))
    return suite

# $Id$

from Testing import ZopeTestCase
from Products.ExternalMethod.ExternalMethod import ExternalMethod
from Products.CPSDefault.tests import CPSTestCase

ZopeTestCase.installProduct('CPSBlog')

CPSBlogTestCase = CPSTestCase.CPSTestCase

class CPSBlogInstaller(CPSTestCase.CPSInstaller):
    def addPortal(self, id):
        """Override the Default addPortal method installing
        a Default CPS Site.

        """

        CPSTestCase.CPSInstaller.addPortal(self, id)
        portal = getattr(self.app, id)

        # Install the CPSBlog product
        cpsblog_installer = ExternalMethod('cpsblog_installer',
                                                    '',
                                                    'CPSBlog.install',
                                                    'install')
        portal._setObject('cpsblog_installer', cpsblog_installer)
        portal.cpsblog_installer()


CPSTestCase.setupPortal(PortalInstaller=CPSBlogInstaller)

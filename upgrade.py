# (C) Copyright 2010 Georges Racinet <georges@racinet.fr>
# Author:
# G.Racinet
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

import logging
import re

import transaction
from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.CPSUtil.text import upgrade_string_unicode

def upgrade_unicode(portal, resync_trees=True):
    """Upgrade all blog documents to unicode.
    """

    logger = logging.getLogger('Products.CPSBlog.upgrades.unicode')
    repotool = portal.portal_repository
    done = 0
    total = 0
    for blog in repotool.iterValues():
        if blog.portal_type != 'Blog': # TODO improve itervalues for repo
            continue
        total += 1
        if not upgrade_blog_unicode(blog):
            logger.error("Could not upgrade blog %s", blog)
            continue

        done += 1
        if done % 100 == 0:
            logger.info("Upgraded %d/%d document revisions", done, total)
            transaction.commit()

    transaction.commit()
    logger.warn("Finished unicode upgrade of %d/%d found blog documents.",
                done, total)

def upgrade_blog_unicode(blog):
    logger = logging.getLogger('Products.CPSBlog.upgrade.upgrade_wiki_unicode')
    logger.debug("Upgrading blog at %s", blog.absolute_url_path())

    # categories
    categories = blog.categories
    for catid in categories.iterkeys():
        cat = categories[catid]
        cat['title'] = upgrade_string_unicode(cat['title'])
        cat['description'] = upgrade_string_unicode(cat['description'])
        categories[catid] = cat
    return True

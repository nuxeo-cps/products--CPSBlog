##parameters=proxy
# $Id$
"""Retrieves number of ForumPost objects under .cps_discussions directory
for the given proxy. This gives us total number of comments posts to proxy.
"""

from Products.CMFCore.utils import getToolByName
from Products.CPSUtil.integration import isProductPresent

number = 0

if isProductPresent('Products.CPSForum'):
    dtool = getToolByName(context, 'portal_discussion')
    # XXX AT: absolute_url(relative=1) should not be used
    forum_url = dtool.getCommentForumURL(proxy.absolute_url(relative=1))
    if forum_url:
        forum = context.restrictedTraverse(forum_url)
        number = len(forum.objectIds())

return number

##parameters=proxy
# $Id$
"""Retrieves number of ForumPost objects under .cps_discussions directory
for the given proxy. This gives us total number of comments posts to proxy.
"""

from Products.CMFCore.utils import getToolByName

portal = getToolByName(context, 'portal_url').getPortalObject()
if hasattr(portal, 'portal_discussion'):
    dtool = context.portal_discussion

    forum_url = dtool.getCommentForumURL(proxy.absolute_url(relative=1))
    if forum_url:
        forum = context.restrictedTraverse(forum_url)
        return len(forum.objectIds())

return 0

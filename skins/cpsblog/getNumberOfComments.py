##parameters=proxy
# $Id$
"""Retrieves number of ForumPost objects under .cps_discussions directory
for the given proxy. This gives us total number of comments posts to proxy.
"""

from Products.CMFCore.utils import getToolByName

number = 0

# Check if CPSForum is installed
dtool = getToolByName(context, 'portal_discussion', None)
if dtool is not None and dtool.meta_type == 'CPS Discussion Tool':
    # XXX AT: absolute_url(relative=1) should not be used
    forum_url = dtool.getCommentForumURL(proxy.absolute_url(relative=1))
    if forum_url:
        forum = context.restrictedTraverse(forum_url)
        number = len(forum.objectIds())

return number

##parameters=proxy_blogentry
"""Retrieves number of ForumPost objects
under .cps_discussions directory for the given proxy_blogentry.
This gives us total number of comments posts to proxy_blogentry.
"""

# $Id$

path = list(context.portal_url.getRelativeContentPath(proxy_blogentry))
path.insert(-1, '.cps_discussions')
path = '/'.join(path)

obj = context.restrictedTraverse(path, None)
if obj is None:
    return 0
else:
    return len(obj.objectIds())

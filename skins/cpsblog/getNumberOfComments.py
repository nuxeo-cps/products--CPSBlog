##parameters=proxy
"""Retrieves number of ForumPost objects under .cps_discussions directory
for the given proxy. This gives us total number of comments posts to proxy.
"""

# $Id$

def getDiscussionsFolder(proxy):
    getParentNode = lambda node: getattr(getattr(node, 'aq_inner', None),
                                         'aq_parent', None)
    parent = getParentNode(proxy)
    while parent:
        if hasattr(parent, '.cps_discussions'):
            return getattr(parent, '.cps_discussions')
        parent = getParentNode(parent)
    return None

discussions_folder = getDiscussionsFolder(proxy)

if discussions_folder is not None:
    forum = getattr(discussions_folder, proxy.getId(), None)
    if forum is not None:
        return len(forum.objectIds())

return 0

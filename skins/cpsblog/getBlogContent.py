##parameters=proxy=None
# $Id$
"""Iterates over tree and returns content of first blog proxy it
encounters.
"""

if proxy is None:
    proxy = context

def isBlogType(proxy):
    return proxy.portal_type == 'Blog'

# check if current context is of Blog type
if isBlogType(proxy):
    return proxy.getContent()

getParentNode = lambda node: getattr(getattr(node, 'aq_inner', None),
                                     'aq_parent', None)
parent = getParentNode(proxy)
while parent:
    if isBlogType(parent):
        return parent.getContent()
    parent = getParentNode(parent)
return None

##parameters=proxy=None
# $Id$
"""Iterates over tree and returns first blog proxy it encounters."""

if proxy is None:
    proxy = context

def isBlogType(proxy):
    try:
        return proxy.portal_type == 'Blog'
    except AttributeError:
        return False

# check if current context is of Blog type
if isBlogType(proxy):
    return proxy

getParentNode = lambda node: getattr(getattr(node, 'aq_inner', None),
                                     'aq_parent', None)
parent = getParentNode(proxy)
while parent:
    if isBlogType(parent):
        return parent
    parent = getParentNode(parent)
return None

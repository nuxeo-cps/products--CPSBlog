##parameters=proxy_blogentry

# $id$

path = list(context.portal_url.getRelativeContentPath(proxy_blogentry))
path.insert(-1, '.cps_discussions')
path = '/'.join(path)
obj = context.restrictedTraverse(path)

return len(obj.objectIds())

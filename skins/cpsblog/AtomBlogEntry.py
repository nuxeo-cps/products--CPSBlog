##Return blogs and services available through ATOM for a given user
print 'coucou'
for i in context.subject():
	print i
return printed

return context.REQUEST

#mtool = context.portal_membership
#if mtool.isAnonymousUser():
#	return "coucou"
#else:
#	user_id = mtool.getAuthenticatedMember().getMemberId()

catalog = context.portal_catalog
query = {}
query['portal_type'] = ('Blog',)
query['allowedRolesAndUsers'] = (user_id, 'BlogManager')
brains = catalog(**query)

results= ''
for brain in brains:
	ob = brain.getObject()
	results += ob.atomBlogServicesDiscovery()

return results
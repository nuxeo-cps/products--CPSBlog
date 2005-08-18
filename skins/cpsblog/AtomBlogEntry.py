##Return blogs and services available through ATOM for a given user

catalog = context.portal_catalog
results = blabla #XXX TODO
blog_list = ""

for r in results:
	results += r.getObject().atomBlogServices()

return results
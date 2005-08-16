##parameters=key=None, is_i18n=None
# $Id$
"""Return blog categories from global categories and all blogs"""

glob_cats_voc = context.portal_vocabularies.blog_glob_categories

catalog = context.portal_catalog

unique_keys = {}
query = {}
query['portal_type'] = 'Blog'

brains = catalog.searchResults(**query)
proxies = [brain.getObject()
           for brain in brains if brain.getObject() is not None]

for proxy in proxies:
    for category in proxy.getContent().getSortedCategories():
        unique_keys[category['title']] = 1

blog_categories = [(k, k) for k in unique_keys]

if key is not None:
    if key in blog_categories:
        return key
    return glob_cats_voc.get(key)

categories = blog_categories + glob_cats_voc.items()
categories.sort()

return tuple(categories)

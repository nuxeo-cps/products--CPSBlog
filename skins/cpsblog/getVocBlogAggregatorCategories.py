##parameters=key=None, is_i18n=None
# $Id$
"""Returns blog categories from global categories and all blogs"""

glob_cats_voc = context.portal_vocabularies.blog_glob_categories

catalog = context.portal_catalog

unique_keys = {}
query = {}
query['portal_type'] = 'Blog'

brains = catalog.searchResults(**query)
for brain in brains:
    for category in brain.getObject().getContent().getSortedCategories():
        unique_keys[category['title']] = 1

blog_categories = [(k, k) for k in unique_keys.keys()]

if key is not None:
    if key in blog_categories:
        return key
    return glob_cats_voc.get(key)


glob_categories = [(k, v) for k, v in glob_cats_voc.items()]

categories = blog_categories + glob_categories
categories.sort()

return tuple(categories)

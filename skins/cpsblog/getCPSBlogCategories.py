##parameters=proxy
# $Id$
"""Returns list of dictionaries containing category title, number of
posts within that category and boolean determining if category is global.

For blog aggregator: categories are all categories referenced in blog
entries displayed for this blog aggregator.
For blog: categories are union of global categories and local categories
of this blog."""

categories = {}
brains = []
glob_categories = context.portal_vocabularies.blog_glob_categories.keys()

if proxy.portal_type == 'BlogAggregator':
    # for blog aggregator categories are all categories referenced in blog
    # entries displayed for this blog aggregator
    entries = proxy.getContent().getSearchResults(proxy)
elif proxy.portal_type == 'Blog':
    # for blog, categories are union of global categories and local categories
    # of this blog
    catalog = context.portal_catalog
    query = {}
    query['portal_type'] = 'BlogEntry'
    query['Subject'] = {'query' : glob_categories, 'operator' : 'or'}
    query['cps_filter_sets'] = 'searchable'
    brains = catalog.searchResults(**query)
    items = filter(None, [brain.getObject() for brain in brains])
    items.extend(proxy.getSortedBlogEntries())
    unique_entries = {}
    # filter out entries that are present in global search result
    for entry in items:
        unique_entries[entry.absolute_url()] = entry
    entries = unique_entries.values()

for entry in entries:
    for category in entry.getContent().Subject():
        if categories.has_key(category):
            categories[category] = categories[category] + 1
        else:
            categories[category] = 1

items = [(k.lower(), {'title' : k, 'posts' : v, 'global' : k in glob_categories})
         for k, v in categories.items()]
items.sort()
categories = [t[1] for t in items]

return categories

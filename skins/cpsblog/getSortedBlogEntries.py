##parameters=sort_on='effective',sort_order='reverse',start_date=None,end_date=None,category=None,path=None
# $Id$
"""Returns list of sorted blog entries.
If path parameter is None then path will be computed as path to context.
"""

catalog = context.portal_catalog

query = {}
query['meta_type'] = 'BlogEntry'
query['sort_on'] = sort_on
query['sort_order'] = sort_order
query['cps_filter_sets'] = 'searchable'
#query['review_state'] = 'published'
if path is not None:
    query['path'] = path
else:
    query['path'] = '/'.join(context.getPhysicalPath())

if start_date and end_date:
    from DateTime import DateTime
    query['effective'] = {'query' : [DateTime(start_date)-1,
                                     DateTime(end_date)+1],
                          'range' : 'minmax'}

if category:
    query['Subject'] = category

brains = catalog.searchResults(**query)

return filter(None, [brain.getObject() for brain in brains])

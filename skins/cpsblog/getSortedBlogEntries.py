##parameters=sort_on='created',sort_order='reverse',start_date=None,end_date=None
# $Id$
"""Returns tuple containing list of sorted blog entries and day_separators
list containing ids of blog entry proxies which marks first objects in group
of objects posted in the same year-month-day.
Lets say we have resulting brains sorted on creation date in reverse order and
containing:
[test5, test4, test3, test2, test1]

test5, test4 are posted on January 4
test3, test2, test1 are posted on January 3
then our day_separators will look like:
[test5, test3]
day_separators makes sense when search query is sorted on creation date and is
used for visually groupping blog entries by day."""

catalog = context.portal_catalog

query = {}
query['meta_type'] = 'BlogEntry'
query['sort_on'] = sort_on
query['sort_order'] = sort_order
query['path'] = '/'.join(context.getPhysicalPath())

if start_date and end_date:
    from DateTime import DateTime
    query['created'] = {'query' : [DateTime(start_date)-1, DateTime(end_date)+1],
                        'range' : 'minmax'}

brains = catalog.searchResults(**query)

day_separators = []

if len(brains) > 0:
    day_separators.append(brains[0].getObject().getId())

def get_date(ob):
    return ob.created().strftime('%Y-%m-%d')

for i in range(1, len(brains)):
    ob = brains[i].getObject()
    prev_ob = brains[i-1].getObject()
    if get_date(ob) != get_date(prev_ob):
        day_separators.append(ob.getId())

return filter(None, [brain.getObject() for brain in brains]), day_separators

##parameters=
# $Id$
"""Returns list of dictionaries containing start and end date strings
in form of '%Y/%m/%d' for constructing blog archive search urls."""

catalog = context.portal_catalog

brains = catalog.searchResults(meta_type='BlogEntry',
                               sort_on='effective',
                               sort_order='reverse',
                               path='/'.join(context.getPhysicalPath()))

# { year : [list of months integers] }
dyear = {}

for brain in brains:
    date = brain.getObject().effective()
    year = date.year()
    month = date.month()
    if year in dyear:
        if month not in dyear[year]:
            dyear[year].append(month)
    else:
        dyear[year] = [month]

year_keys = dyear.keys()
year_keys.sort()
year_keys.reverse()

for key in year_keys:
    dyear[key].sort()
    dyear[key].reverse()

from DateTime import DateTime

return [{'start_date' : '%s/%s/1' % (year, month),
         'end_date' : '%s/%s/%s' % (year, month,
                                    context.getLastDayOfMonth(year, month)),
         'month_name' : DateTime('%s/%s/1' % (year, month)).Month(),
         'year' : year,
         'month' : month,
         'month_mm' : DateTime('%s/%s/1' % (year, month)).mm()}
        for year in year_keys
        for month in dyear[year]]

##parameters=
# $Id$
"""Returns blog entries for month detecting it from subpath."""

if len(traverse_subpath) != 2:
    return None

year = traverse_subpath[0]
month = traverse_subpath[1]

try:
    iyear = int(year)
    imonth = int(month)
except ValueError:
    iyear = 0
    imonth = 0

if (iyear > 3000 or iyear < 1970) or \
       (imonth > 12 or imonth < 0):
    return []

start_date = '%s/%s/1' % (year, month)
end_date = '%s/%s/%s' % (year, month, context.getLastDayOfMonth(year, month))

return context.getBlogProxy().getSortedBlogEntries(start_date=start_date,
                                                   end_date=end_date)

##parameters=
# $Id$
"""Returns blog entries for the year detecting it from subpath."""

from DateTime import DateTime

if len(traverse_subpath) != 1:
    return None

year = traverse_subpath[0]

try:
    iyear = int(year)
except ValueError:
    iyear = 0

if iyear > 3000 or iyear < 1970:
    return []

start_date = DateTime('%s/1/1' % year)
end_date = DateTime('%s/12/%s' % (year, context.getLastDayOfMonth(year, '12')))

return context.getBlogProxy().getSortedBlogEntries(start_date=start_date,
                                                   end_date=end_date)

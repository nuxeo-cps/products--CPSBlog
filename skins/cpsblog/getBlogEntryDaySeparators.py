##parameters=items
# $Id$
"""Returns day_separators list containing ids of blog entry proxies which marks
first objects in group of objects posted in the same year-month-day.
Lets say we have items sorted on creation date in reverse order and containing:
[test5, test4, test3, test2, test1]

test5, test4 are posted on January 4
test3, test2, test1 are posted on January 3
then our day_separators will look like:
[test5, test3]
day_separators makes sense when 'items' are sorted on creation date and is
used for visually groupping blog entries by day."""

day_separators = []

if len(items) > 0:
    day_separators.append(items[0].getId())

def get_date(proxy):
    return proxy.effective().strftime('%Y-%m-%d')

for i in range(1, len(items)):
    proxy = items[i]
    prev_proxy = items[i-1]
    if get_date(proxy) != get_date(prev_proxy):
        day_separators.append(proxy.getId())

return day_separators

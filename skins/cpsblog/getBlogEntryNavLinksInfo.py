##parameters=
# $Id$
"""Returns info dictionary containing urls and titles of previous and next
blog entry with regard to current blog entry."""

proxy = context.getBlogProxy()
bentries = [v for v in proxy.contentValues(filter={'meta_type':'BlogEntry'})]

items = [(bentry.created(), bentry) for bentry in bentries]
items.sort()

bentries[:] = [t[1] for t in items]

blen = len(bentries)
info = {}

for i in range(blen):
    if context.getId() == bentries[i].getId():
        if i + 1 >= blen:
            info['next_url'] = ''
            info['next_title'] = ''
        else:
            info['next_url'] = bentries[i+1].absolute_url()
            info['next_title'] = bentries[i+1].Title()
        if i - 1 < 0:
            info['prev_url'] = ''
            info['prev_title'] = ''
        else:
            info['prev_url'] = bentries[i-1].absolute_url()
            info['prev_title'] = bentries[i-1].Title()
        return info
return None

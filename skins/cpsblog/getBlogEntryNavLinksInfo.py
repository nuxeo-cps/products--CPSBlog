##parameters=
# $Id$
"""Returns info dictionary containing urls and titles of previous and next
blog entry with regard to current blog entry."""

proxy = context.getBlogProxy()
bentries = proxy.getSortedBlogEntries(sort_order='ascending')

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

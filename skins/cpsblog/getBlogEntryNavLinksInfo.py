##parameters=
# $Id$
"""Returns info dictionary containing urls and titles of previous and next
blog entry with regard to current blog entry."""

URL_TITLE_MAX_LENGTH = 40

def strip_title(title):
    if len(title) > URL_TITLE_MAX_LENGTH:
        stitle = title[:URL_TITLE_MAX_LENGTH]
        i = stitle.rfind(' ')
        if i > 0:
            stitle = stitle[:i]
        stitle += '...'
        return stitle
    return title

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
            info['next_title'] = strip_title(bentries[i+1].Title())
        if i - 1 < 0:
            info['prev_url'] = ''
            info['prev_title'] = ''
        else:
            info['prev_url'] = bentries[i-1].absolute_url()
            info['prev_title'] = strip_title(bentries[i-1].Title())
        return info
return None

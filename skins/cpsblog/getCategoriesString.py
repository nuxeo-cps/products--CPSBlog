##parameters=proxy=None
# $Id$
"""Returns string, containing categories to which blog entry belongs"""

if proxy is not None:
    context = proxy

categories = context.getContent().Subject()
cats_len = len(categories)

if cats_len == 0:
    return None
elif cats_len == 1:
    return categories[0]

catstr = ', '.join(categories[:-1])
catstr += ' <span tal:omit-tag="" i18n:translate="">and</span> '
catstr += categories[-1]
return catstr

##parameters=url
from urlparse import urlparse

#See : <link rel="alternate"> is always the permalink of the entry
#http://diveintomark.org/archives/2004/05/28/howto-atom-id - article
#about constructing id

(location, path) = urlparse(url)[1:3]
i = location.rfind(':')
if i > 0:
    location = location[:i]
p = path.replace('/', ':')
uid = 'tag:' + location + p

return uid
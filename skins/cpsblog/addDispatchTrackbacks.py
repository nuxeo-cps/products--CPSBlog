##parameters=trackback_urls,REQUEST=None,proxy=None
# $Id$
"""Adds dispatching trackbacks to the blog entry and sends pings."""
import re

if proxy is not None:
    context = proxy

blog_entry = context.getContent()

for url in trackback_urls:
    blog_entry.addDispatchTrackback(url)

params = {}
if REQUEST is not None:
    # at this moment schema fields were not set yet,
    # so we need to compute needed information from request
    DESCRIPTION_MAX_LENGTH = 200
    def strip_html(text):
        # stripping of html tags based on simple regexp
        return re.sub("<[^>]+>", '', text)

    content = REQUEST.form.get('widget__content')
    excerpt = strip_html(content)
    if len(excerpt) > DESCRIPTION_MAX_LENGTH:
        excerpt = excerpt[:DESCRIPTION_MAX_LENGTH]
        i = excerpt.rfind(' ')
        if i > 0:
            excerpt = excerpt[:i]
        excerpt += '...'

    params = {'title' : REQUEST.form.get('widget__Title'),
              'excerpt' : excerpt
              }

return blog_entry.sendTrackbacks(context, **params)

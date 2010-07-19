##parameters=REQUEST=None
# $Id: exportatom.py 25893 2005-08-16 22:55:23Z sfermigier $
"""Creates an ATOM feed for BlogAggregator and Blog portal types."""

if context.portal_type == 'Blog':
    result = context.atomFeed()
elif context.portal_type == 'BlogEntry':
    result = context.atomEntry()
elif context.portal_type == "BlogAggregator":
    objects = context.getContent().getSearchResults(context)
    result = context.atomFeed(entries=objects)

result = """<?xml version="1.0" encoding="UTF-8"?>\n""" + result

if REQUEST is not None:
    REQUEST.RESPONSE.setHeader('Content-Type', 'application/xml; charset=UTF-8')
    REQUEST.RESPONSE.setHeader('Cache-Control', 'no-cache')

return result


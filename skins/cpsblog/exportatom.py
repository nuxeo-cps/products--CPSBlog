##parameters=REQUEST=None
# $Id: exportatom.py 25893 2005-08-16 22:55:23Z sfermigier $
"""Creates an ATOM feed for BlogAggregator and Blog portal types."""


if context.portal_type == 'Blog':
    result = context.atomFeed()
elif context.portal_type == 'BlogEntry':
    result = context.atomEntry()

if REQUEST is not None:
    REQUEST.RESPONSE.setHeader('Content-Type', 'application/xml; charset=ISO-8859-15')
    REQUEST.RESPONSE.setHeader('Cache-Control', 'no-cache')
    REQUEST.RESPONSE.setBody(result)

return REQUEST.RESPONSE

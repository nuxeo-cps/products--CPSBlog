##parameters=REQUEST=None
# $Id: exportatom.py 25893 2005-08-16 22:55:23Z sfermigier $
"""Creates an ATOM feed for BlogAggregator and Blog portal types."""

# FIXME: 'result' is accessed before assignment if the portal_type is BlogAggregator

if context.portal_type == 'Blog':
    result = context.atomFeed()
elif context.portal_type == 'BlogEntry':
    result = context.atomEntry()

if REQUEST is not None:
    REQUEST.RESPONSE.setHeader('Content-Type', 'application/xml; charset=ISO-8859-15')
    REQUEST.RESPONSE.setHeader('Cache-Control', 'no-cache')

return result


##parameters=REQUEST=None
# $Id$
"""Passes context and REQUEST to the real object's tbping method
for handling Trackback's GET and POST request and returns result.
Context of the script should always be blog entry."""

return context.getContent().tbping(context, REQUEST)

##parameters=category, id
# $Id$
"""Returns icon for given category and id"""

try:
    actionicons = context.portal_actionicons
except AttributeError:
    return ''

return actionicons.getActionIcon(category, id)

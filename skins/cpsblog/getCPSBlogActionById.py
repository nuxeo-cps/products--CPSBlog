##parameters=actions,id
# $Id$
"""Returns action list by given id from passed actions"""

return [action for action in actions if action['id'] == id]

##parameters=rows, widget_id
# $Id$
"""Returns cell containing widget with given id."""

for row in rows:
    for cell in row:
        if cell['widget'].getWidgetId() == widget_id:
            return cell
return None

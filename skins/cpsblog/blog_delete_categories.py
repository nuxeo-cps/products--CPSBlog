##parameters=categories=None
# $Id$
"""Removes blog categories."""

if categories:
    for catid in categories:
        context.getEditableContent().removeCategory(catid)

return context.blog_manage_categories()

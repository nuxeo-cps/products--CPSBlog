##parameters=categories=None,REQUEST=None
# $Id$
"""Removes blog categories."""

if categories:
    for catid in categories:
        context.getEditableContent().removeCategory(catid)

REQUEST.RESPONSE.redirect(REQUEST.URL1+'/blog_manage_categories')

##parameters=
"""Unpublish BlogEntry
"""

# $Id$

wftool = context.portal_workflow

try:
    wftool.doActionFor(context,
                       'unpublish',
                       comment="Unpublishing BlogEntry")
    psm = "psm_blog_entry_unpublish_done"
except:
    psm = "psm_blog_entry_unpublish_not_possible"

if context.REQUEST is not None:
    context.REQUEST.RESPONSE.redirect(context.absolute_url()+'?portal_status_message='+psm)

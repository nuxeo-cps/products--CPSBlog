##parameters=
"""Publish BlogEntry"""

# $Id$

wftool = context.portal_workflow

try:
    wftool.doActionFor(context,
                       'publish',
                       comment="Publishing BlogEntry")
    psm = "psm_blog_entry_publish_done"
except:
    psm = "psm_blog_entry_publish_not_possible"

if context.REQUEST is not None:
    context.REQUEST.RESPONSE.redirect(context.absolute_url()+'?portal_status_message='+psm)

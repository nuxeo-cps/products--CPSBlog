##parameters=trackbacks_ids,REQUEST=None
# $Id$
"""Removes trackbacks from blog entry. This script is called from edit
layout for blog entry, so 'context' is repository blog entry object,
not proxy."""

context.removeTrackbacks(trackbacks_ids)

REQUEST.RESPONSE.redirect(REQUEST['HTTP_REFERER'])

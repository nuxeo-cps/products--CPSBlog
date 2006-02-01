##parameters=REQUEST, cluster=None, cpsdocument_edit_and_view_button=None, action=None
# $Id$
"""
Called when a document form is posted.

Validates data, then:

 - if there's no error, updates the object and redirects to it,

 - if there's an error, puts data in session and redirects to edit form.

A form uid is propagated during the redirect to uniquely identify the
form in the session.
"""

from urllib import urlencode
from Products.CPSDocument.utils import getFormUidUrlArg

# Until ajax posts directly to its own script...
if 'ajax_edit' in REQUEST.form:
    return self.blogentry_edit_ajax(REQUEST, cluster=cluster)

# Check flexible controls
context.editLayouts(REQUEST=REQUEST)

# Validate the document and write it if it's valid
# (We don't call getEditableContent here, validate does it when needed.)
doc = context.getContent()
is_valid, ds = doc.validate(request=REQUEST, proxy=context, cluster=cluster,
                            use_session=True)

if action is None:
    action = '/blog_entry_edit_form'

if is_valid:
    comments = REQUEST.get('comments')
    context.cpsdocument_notify_modification(comments=comments)
    if cpsdocument_edit_and_view_button is not None:
        action = ''
    psm = 'psm_content_changed'
    args = {}

    # add and send trackbacks
    doc.addDispatchTrackbacks(context=context)
else:
    psm = 'psm_content_error'
    args = getFormUidUrlArg(REQUEST)

args['portal_status_message'] = psm
url = context.absolute_url() + action + '?' + urlencode(args)
REQUEST.RESPONSE.redirect(url)

##parameters=REQUEST, layout_id=None, cluster=None
# $Id$
"""
edit layout and content if form submited

return html renderer + psm
"""
doc = context.getContent()

do_notify = False

layout_changed = context.editLayouts(REQUEST=REQUEST);

if layout_changed or REQUEST.has_key('cpsdocument_edit_button'):
    request = REQUEST
    psm = 'psm_content_changed'
    do_notify = True
else:
    request = None
    psm = ''

res = doc.renderEditDetailed(request=request, proxy=context,
                             layout_id=layout_id, cluster=cluster)

if not res[1]:
    psm = 'psm_content_error'
    do_notify = False

if do_notify:
    # XXX:
    # Notification has to be done manually here until the workflow takes care of
    # the "workflow_modify" transition.
    context.portal_eventservice.notifyEvent('workflow_modify', context,
                                            {'comments': request.get('comments')
                                             })

return res[0], psm

##parameters=REQUEST, cluster=None
# $Id$
"""
Called when a document form is posted for AJAX validation.

Returns the validation result and the rendered page in an XML-RPC response.
"""

# This is hardcoded here because CPS is not UTF-8 yet (it's ISO-8859-15)
# so the form fields are sent in strings that are unicode in fact
for key, value in REQUEST.form.items():
    if isinstance(value, str):
        value = value.decode('utf-8', 'replace').encode('iso-8859-15')
        REQUEST.form[key] = value

doc = context.getContent()
res = doc.renderEditDetailed(request=REQUEST, proxy=context, cluster=cluster)
layout, is_valid = str(res[0]), res[1]

# AJAX tries to change the doc and just needs to know if there were errors
# for feedback without a new form rendering.
# XXX TODO: avoid here an extra HTML rendering
# by calling renderEditDetailed() with the right parameters

# At this time we do XML-RPC answers.
# We'll see later how to automate it to avoid a manual serialization here.

# Send UTF-8 content
layout = layout.decode('iso-8859-15').encode('utf-8')

if is_valid and 'cpsdocument_edit_and_view_button' in REQUEST:
    action = 'view'
    # add and send trackbacks
    doc.addDispatchTrackbacks(context=context)
else:
    action = ''

REQUEST.RESPONSE.setHeader('Content-Type', 'text/xml')
REQUEST.RESPONSE.setHeader('Cache-Control', 'no-cache')
response = '<?xml version="1.0" encoding="utf-8" ?>'
response += '<ajax-response>'
response += '<result>%s</result>' % str(bool(is_valid))
response += '<layout><![CDATA[%s]]></layout>' % layout
response += '<action>%s</action>' % action
response += '</ajax-response>'
return response

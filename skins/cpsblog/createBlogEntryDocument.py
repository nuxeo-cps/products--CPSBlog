##parameters=REQUEST
# $Id$
"""
Create a Blog Entry

return html renderer + psm
"""
type_name = REQUEST.form['type_name']
ti = context.portal_types[type_name]
validate = REQUEST.has_key('cpsdocument_create_button')

res = ti.renderCreateObjectDetailed(container=context, request=REQUEST,
                                    validate=validate, layout_mode='create',
                                    create_callback='createBlogEntryDocument_cb',
                                    created_callback='blogentrydocument_created')

psm = ''
if not res[1]:
    psm = 'psm_content_error'
elif validate:
    psm = 'psm_content_created'

return res[0], psm

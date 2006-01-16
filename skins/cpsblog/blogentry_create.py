##parameters=REQUEST, cluster=None, type_name=None
# $Id$
"""
Called when a document form is posted.

Validates data, then:

 - if there's no error, updates the object and redirects to it,

 - if there's an error, puts data in session and redirects to creation form.

A form uid is propagated during the redirect to uniquely identify the
form in the session.
"""
from urllib import urlencode
from Products.CMFCore.utils import getToolByName
from Products.CPSDocument.utils import getFormUidUrlArg

ti = getToolByName(context, 'portal_types').getTypeInfo(type_name)

is_valid, ds = ti.validateObject(None, layout_mode='create',
                                 request=REQUEST, context=context,
                                 cluster=cluster, use_session=True)

if is_valid:
    ob = context.blogentry_create_do(type_name, ds.getDataModel())
    url = ob.absolute_url()
    action = ob.getTypeInfo().immediate_view
    psm = 'psm_content_created'
    args = {}
else:
    url = context.absolute_url()
    action = 'cpsdocument_create_form'
    psm = 'psm_content_error'
    args = {'type_name': type_name}
    args.update(getFormUidUrlArg(REQUEST))

args['portal_status_message'] = psm
url = url + '/' + action + '?' + urlencode(args)
REQUEST.RESPONSE.redirect(url)

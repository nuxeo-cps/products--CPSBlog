##parameters=type_name, datamodel
# $Id$
"""
Create an empty object in the context according to the datamodel.

Datamodel may be examined to create a suitable id.

Returns the created object (usually a proxy).
"""
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime

id = datamodel.get('Title')
if not id:
    id = 'my ' + type_name
id = context.computeId(compute_from=id) # XXX shouldn't use a skin

language = datamodel.get('Language')
if not language:
    ts = getToolByName(context, 'translation_service')
    language = ts.getSelectedLanguage()

# custom prefix
id = DateTime().strftime('%Y_%m_%d') + '_' + id

# Datamodel is passed so that flexti can initialize the object.
new_id = context.invokeFactory(type_name, id, datamodel=datamodel,
                               language=language)
if new_id is not None:
    id = new_id

ob = getattr(context, id)

# set effective date equal to created after creation
ob.getEditableContent().setEffectiveDate(ob.created())
ob.setEffectiveDate(ob.created())

context.notifyCPSDocumentCreation(ob=ob) # BBB obsolete in CPS 3.5.0

return ob

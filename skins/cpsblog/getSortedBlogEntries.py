##parameters=sort_on='created',sort_order='reverse'
# $Id$
"""Returns list of sorted blog entries."""

catalog = context.portal_catalog

brains = catalog.searchResults(meta_type='BlogEntry',
                               sort_on=sort_on,
                               sort_order=sort_order,
                               path='/'.join(context.getPhysicalPath()))

return filter(None, [brain.getObject() for brain in brains])

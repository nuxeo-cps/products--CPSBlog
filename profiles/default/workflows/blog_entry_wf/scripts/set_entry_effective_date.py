##parameters=state_change
from DateTime import DateTime
now = DateTime()
blog_entry_proxy = state_change.object
blog_entry_proxy.getEditableContent().setEffectiveDate(now)
blog_entry_proxy.setEffectiveDate(now)
blog_entry_proxy.reindexObject(idxs=['effective', 'start', 'end'])
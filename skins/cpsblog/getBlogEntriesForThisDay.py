##parameters=this_day,REQUEST
# $Id$
"""Returns list of blog entries published on pointed day."""

location = REQUEST.get('location', None)
event_types = REQUEST.get('event_types', None)

calendar = context.portal_calendar
brains = calendar.getCPSEventsForThisDay(this_day,
                                         location=location,
                                         event_types=event_types)

return filter(None, [brain.getObject() for brain in brains])

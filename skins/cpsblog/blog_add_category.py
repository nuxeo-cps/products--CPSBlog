##parameters=REQUEST=None
# $Id$
"""Adds blog category."""

title = REQUEST.get('title')
description = REQUEST.get('description')

catdef = {'title' : title,
          'description' : description,
          'urls_to_ping' : (),
          'accept_pings' : False
          }

context.getEditableContent().addCategory(**catdef)

return context.blog_manage_categories()

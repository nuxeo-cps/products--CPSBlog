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

REQUEST.RESPONSE.redirect(REQUEST.URL1+'/blog_manage_categories')

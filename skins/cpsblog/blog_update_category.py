##parameters=REQUEST=None
# $Id$
"""Updates blog category."""

category_id = REQUEST.get('category_id')
title = REQUEST.get('title')
description = REQUEST.get('description')

catdef = {'title' : title,
          'description' : description
          }

context.getEditableContent().updateCategory(category_id, catdef)

return context.blog_manage_categories()

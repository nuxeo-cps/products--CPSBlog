##parameters=key=None, is_i18n=None
# $Id$
"""Returns blog categories for method vocabulary."""

blog = context.getBlogContent()

if key is not None and is_i18n is not None:
    category = blog.getCategoryByTitle(key)
    return category['title']
elif key is not None:
    category = blog.getCategoryByTitle(key)
    return category['title']

categories = [(cat['title'], cat['title']) for cat
              in blog.getSortedCategories()]
return tuple(categories)

##parameters=key=None, is_i18n=None
# $Id$
"""Returns blog categories for method vocabulary."""

blog = context.getBlogContent()
glob_cats_voc = context.portal_vocabularies.blog_glob_categories

if key is not None and is_i18n is not None:
    category = blog.getCategoryByTitle(key)
    if category is None:
        return glob_cats_voc.getMsgid(key)
    return category['title']
elif key is not None:
    category = blog.getCategoryByTitle(key)
    if category is None:
        return glob_cats_voc.get(key)
    return category['title']

blog_categories = [(cat['title'], cat['title']) for cat
                   in blog.getSortedCategories()]

glob_categories = [(k, v) for k, v in glob_cats_voc.items()]

categories = blog_categories + glob_categories
categories.sort()

return tuple(categories)

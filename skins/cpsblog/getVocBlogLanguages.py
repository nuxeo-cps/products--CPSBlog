##parameters=key=None, is_i18n=None
# $Id$
"""Returns blog languages for method vocabulary."""

blog = context.getBlogContent()
lang_voc = context.portal_vocabularies.language_voc
mcat = context.Localizer.default

t = [(mcat(lang_voc.getMsgid(lang)).lower(), lang) for lang in blog.langs]
t.sort()
langs = [v[1] for v in t]

if key is not None and is_i18n is not None:
    return lang_voc.getMsgid(key)
elif key is not None:
    return lang_voc.get(key)

return ([(lang, lang) for lang in langs])

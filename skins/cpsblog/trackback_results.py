##parameters=REQUEST=None, **kw
# $Id$
"""Returns result for tbping"""

error = kw.get('error')

def setHeaderParameters():
    if REQUEST is not None:
        REQUEST.RESPONSE.setHeader('Content-Type', 'text/xml; charset=ISO-8859-15')
        REQUEST.RESPONSE.setHeader('Cache-Control', 'no-cache')

if error:
    output = """<?xml version="1.0" encoding="ISO-8859-15"?>
    <response>
    <error>%(error)s</error>
    <message>%(message)s</message>
    </response>
    """
    setHeaderParameters()
    message = kw.get('message')
    return output % {'error' : error,
                     'message' : message,
                     }

output = """<?xml version="1.0" encoding="ISO-8859-15"?>
<response>
<error>%(error)s</error>
%(trackbacks)s
</response>
"""

trackbacks_template = """<rss version="0.91">
<channel>
<title>%(blog_entry_title)s</title>
<link>%(blog_entry_url)s</link>
<description>summary of blog entry</description>
%(trackbacks)s
</channel>
</rss>
"""

trackback_template = """<item>
<title>%(trackback_title)s</title>
<link>%(trackback_url)s</link>
<description>%(trackback_excerpt)s</description>
</item>
"""

trackbacks_items = ''

for tb in context.getContent().getSortedTrackbacks():
    tb_kw = {'trackback_title' : tb.title,
             'trackback_url' : tb.url,
             'trackback_excerpt' : tb.excerpt
             }
    trackbacks_items += trackback_template % tb_kw


trackbacks = trackbacks_template % {'blog_entry_title' : context.Title(),
                                    'blog_entry_url' : context.absolute_url(),
                                    'trackbacks' : trackbacks_items,
                                    }

text = output % {'error' : error,
                 'trackbacks' : trackbacks,
                 }

setHeaderParameters()

return text

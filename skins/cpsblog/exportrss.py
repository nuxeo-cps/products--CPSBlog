##parameters=REQUEST=None
# $Id$
"""Creates an rss 1.0 feed for BlogAggregator and Blog portal types."""

from cgi import escape
import re

DESCRIPTION_MAX_LENGTH = 200

items = []
if context.portal_type == 'BlogAggregator':
    items = context.getContent().getSearchResults(context)
elif context.portal_type == 'Blog':
    items = context.getSortedBlogEntries()

# this is the hard coded rss 1.0
rdf_ns = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"

rss_fmt = r"""<?xml version="1.0" encoding="ISO-8859-1"?>
<?xml-stylesheet href="%(css_url)s" type="text/css"?>
<rdf:RDF
  xmlns:rdf="%(rdf_ns)s"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns="http://purl.org/rss/1.0/"
  xmlns:xhtml="http://www.w3.org/1999/xhtml">

  <channel rdf:about="%(channel_about)s">
    <title>%(channel_title)s</title>
    <description>%(channel_description)s</description>
    <link>%(channel_link)s</link>

    <items>
      <rdf:Seq>
%(items_li)s
      </rdf:Seq>
    </items>

  </channel>


%(items)s

  <xhtml:script id="js" type="text/javascript" src="%(js_url)s" />

</rdf:RDF>
"""

rss_item_li = """        <rdf:li rdf:resources="%(item_id)s" />\n"""

rss_item = """  <item rdf:about="%(item_id)s">
    <title>%(item_title)s</title>
    <description>%(item_description)s</description>
    <link>%(item_link)s</link>
%(item_dc)s
  </item>\n"""

rss_item_dc = """    <dc:%(dc_key)s>%(dc_value)s</dc:%(dc_key)s>\n"""

# dublin core available from getContentInfo
dc_keys = ('subject', 'date', 'creator',
           'contributor', 'rights', 'language',
           'coverage', 'relation', 'source')

# computed value
base_url = context.portal_url()+'/'
channel_url = context.absolute_url() + '/exportrss'
channel_description = "RSS 1.0 export from the folder '%s'." % \
                      context.title_or_id()

header_text = body_text = ''
for item in items:
    info = context.getContentInfo(item, level=2)
    url = base_url + info.get('rpath')
    header_text += rss_item_li % {'item_id': url}
    item_date = context.getDateStr(info.get('time'), fmt='iso8601')
    dc_text = ''
    for key in dc_keys:
        if key == 'date':
            value = item_date
        else:
            value = info.get(key)
        if value:
            dc_text += rss_item_dc % {'dc_key': key,
                                      'dc_value': escape(value)}
    doc = info['doc']

    def strip_html(text):
        # stripping of html tags based on simple regexp
        return re.sub("<[^>]+>", '', text)

    if hasattr(doc, 'summary'):
        summary = strip_html(doc.summary)
    else:
        summary = strip_html(doc.content)
        if len(summary) > DESCRIPTION_MAX_LENGTH:
            summary = summary[:DESCRIPTION_MAX_LENGTH]
            i = summary.rfind(' ')
            if i > 0:
                summary = summary[:i]
            summary += '...'

    body_text += rss_item % {'item_id': url,
                             'item_title': escape(info.get('title', '')),
                             'item_description': escape(summary),
                             'item_link': url,
                             'item_dc': dc_text,}

text = rss_fmt % {'css_url': base_url + 'nuxeo_rss_css.css',
                  'rdf_ns': rdf_ns,
                  'channel_about': channel_url,
                  'channel_title': escape(context.title_or_id()),
                  'channel_link': channel_url,
                  'channel_description': escape(channel_description),
                  'items_li': header_text,
                  'items': body_text,
                  'js_url': base_url + 'rss.js',
                  }

if REQUEST:
   REQUEST.RESPONSE.setHeader('Content-Type', 'text/xml')
   REQUEST.RESPONSE.setHeader('Cache-Control', 'no-cache')

return text

##parameters=
# $Id$
"""Returns computed RDF block to be inserted into blog entry
for trackbacks discovery."""

info = context.getContentInfo(context, level=1)

output = """<!--
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:trackback="http://madskills.com/public/xml/rss/module/trackback/"
         xmlns:dc="http://purl.org/dc/elements/1.1/">
<rdf:Description
    rdf:about="%(rdf_about)s"
    trackback:ping="%(trackback_ping)s"
    dc:title="%(dc_title)s"
    dc:identifier="%(dc_identifier)s"
    dc:subject="%(dc_subject)s"
    dc:description="%(dc_description)s"
    dc:creator="%(dc_creator)s"
    dc:date="%(dc_date)s"
/>
</rdf:RDF>
-->
"""
# " <- for Emacs python mode

return output % {'rdf_about' :  context.absolute_url(),
                 'trackback_ping' : context.absolute_url() + '/tbping',
                 'dc_title' : info['title'],
                 'dc_identifier' : context.absolute_url(),
                 'dc_subject' : ','.join(context.getContent().Subject()),
                 'dc_description' : info['description'],
                 'dc_creator' : info['creator'],
                 'dc_date' : context.created(),
                 }

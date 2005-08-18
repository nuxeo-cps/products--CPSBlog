# (C) Copyright 2004 Nuxeo SARL <http://nuxeo.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
# $Id: Blog.py 25927 2005-08-17 22:57:00Z ebarroca $

from zLOG import LOG, DEBUG, TRACE
from Products.CPSUtil.html import sanitize

class AtomAware:
    """Class that add some Atom capacity to CPSDocuments"""

    def parseAtomXmlEntry(self, xml_string):
        from lxml import etree
        from StringIO import StringIO

        body = StringIO(xml_string)
        tbody = etree.parse(body)
        info = {}
        ns = {'a': 'http://purl.org/atom/ns#',
              'ab': 'http://purl.org/atom-blog/ns#',
              'dc': 'http://purl.org/dc/elements/1.1/',
              'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
              'wsu': 'http://schemas.xmlsoap.org/ws/2002/07/utility',
              'wsse': 'http://schemas.xmlsoap.org/ws/2002/07/secext',
              'xmlns': 'http://schemas.xmlsoap.org/wsdl/http/'}

        xtitle = tbody.xpath('//a:entry/a:title', ns)
        xcontent = tbody.xpath('//a:entry/a:content', ns)
        xcategories = tbody.xpath('//a:entry/dc:subject', ns)
        xissued = tbody.xpath('//a:entry/a:issued', ns)
        
        if len(xtitle):
            info['Title'] = sanitize(xtitle[0].text)
        if len(xcontent):
            info['content'] = sanitize(xcontent[0].text)
        if len(xissued):
            info['CreationDate'] = info['EffectiveDate'] = xissued[0].text
            
        info['subject'] = []
        for category in xcategories:
            info['subject'].append(category.text)
        
        return info
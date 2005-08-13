# (C) Copyright 2004-2005 Nuxeo SARL <http://nuxeo.com>
# Author: Ruslan Spivak <rspivak@nuxeo.com>
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
# $Id$


def update_blogaggregator(self):
    """Updates BlogAggregator's schema.

    Adds search_limit field is not present
    """
    catalog = self.portal_catalog

    proxies = [b.getObject()
               for b in catalog.searchResults(portal_type='BlogAggregator')]

    for proxy in proxies:
        doc = proxy.getContent()
        if getattr(doc, 'search_limit', None) is None:
            doc.search_limit = 20
    return 'Fin'

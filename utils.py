# (C) Copyright 2005 Nuxeo SARL <http://nuxeo.com>
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

import httplib
import urllib
import urlparse
import re

def post_trackback(trackback_url, title='', excerpt='', url='', blog_name=''):
    """Sends trackback to given url."""
    params = urllib.urlencode({'title' : title,
                               'excerpt' : excerpt,
                               'url' : url,
                               'blog_name' : blog_name
                               })

    headers = {'Content-Type' : 'application/x-www-form-urlencoded',
               'Accept' : 'text/xml',
               }

    location, path = urlparse.urlparse(trackback_url)[1:3]

    try:
        conn = httplib.HTTPConnection(location)
        conn.request('POST', path, params, headers)

        response = conn.getresponse()
        data = response.read()
        conn.close()

        error_code = 0
        msg = ''
        m = re.search(r'<error>(.*)</error>', data)
        if m:
            error_code = int(m.group(1))
        else:
            # this may be in case, for example, if you try to ping entry
            # that is in unpublished state
            error_code = -1
        m = re.search(r'<message>(.*)</message>', data)
        if m:
            msg = m.group(1)
        else:
            # set data returned by the server as message, may be helpful
            # for diagnostics.
            msg = data
    except Exception, e:
        error_code = -1
        msg = str(e)

    return error_code, msg

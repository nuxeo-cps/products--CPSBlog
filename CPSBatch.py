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
# $Id$

from ZTUtils.Batch import Batch as ZTUBatch
from ZTUtils.Batch import LazyPrevBatch, LazyNextBatch, LazySequenceLength
from ZTUtils.Batch import opt
from ZTUtils import make_query


class Batch(ZTUBatch):
    """Handles sequence batches."""
    __allow_access_to_unprotected_subobjects__ = 1

    previous = LazyPrevBatch()
    next = LazyNextBatch()
    sequence_length = LazySequenceLength()

    def __init__(self, sequence, size, start=0, end=0, orphan=0, overlap=0,
                 page_range=7):

        start = start + 1

        start, end, sz = opt(start, end, size, orphan, sequence)

        self._sequence = sequence
        self.size = sz
        self._size = size
        self.start = start
        self.end = end
        self.orphan = orphan
        self.overlap = overlap
        self.first = max(start - 1, 0)
        self.length = self.end - self.first

        if self.first == 0:
            self.previous = None

        # total number of pages
        self.numpages = calculate_numpages(self.sequence_length-self.orphan,
                                           self.size, self.overlap)

        self.cur_page = calculate_page_number(self.start, self.size,
                                              self.overlap)

        self.page_range, self.page_range_start, self.page_range_end = \
                         calculate_page_range(self.cur_page, self.numpages,
                                              page_range)

        # set up the lists for navigation: 4 5 [6] 7 8
        # nav_list is the complete list, including current page number
        # prev_list is the 4 5 in the example above
        # next_list is 7 8 in the example above
        self.nav_list = self.prev_list = self.next_list = []
        if self.page_range and self.numpages >= 1:
            self.nav_list  = range(self.page_range_start, self.page_range_end)
            self.prev_list = range(self.page_range_start, self.cur_page)
            self.next_list = range(self.cur_page + 1, self.page_range_end)

    def getPageUrl(self, form_dict, page_number=None):
        """Makes the url for a given page"""
        if page_number is None:
            page_number = self.cur_page
        b_start = page_number * (self.size - self.overlap) - self.size
        return make_query(form_dict, b_start=b_start)

    def getNavigationUrls(self, form_dict, nav_list=None):
        """Returns list of pairs (page number, url) for navigation links."""
        if nav_list is None:
            nav_list = self.nav_list
        return map(lambda x: (x, self.getPageUrl(form_dict, x)), nav_list)

    def getPrevUrls(self, form_dict):
        """Helper method to get prev navigation list from templates"""
        return self.getNavigationUrls(form_dict, self.prev_list)

    def getNextUrls(self, form_dict):
        """Helper method to get next navigation list from templates"""
        return self.getNavigationUrls(form_dict, self.next_list)


def calculate_page_number(element_number, batch_size, overlap=0):
    """Calculates page number for the given element number."""
    try:
        page_number, remainder = divmod(element_number, batch_size - overlap)
    except ZeroDivisionError:
        page_number, remainder = divmod(element_number, 1)

    if remainder > overlap:
        page_number = page_number + 1
    page_number = max(page_number, 1)

    return page_number

def calculate_numpages(sequence_length, batch_size, overlap=0):
    """Calculates total number of pages."""
    return calculate_page_number(sequence_length, batch_size, overlap)

def calculate_page_range(page_number, numpages, page_range):
    """Calculates the page range for the navigation quick links."""
    # page range is the number of pages linked to in the navigation,
    # always odd number.
    page_range = max(0 , page_range + page_range % 2 - 1)

    half_prange = (page_range - 1) / 2

    # start shouldn't be negative
    page_range_start = max(1, page_number - half_prange)

    # end shouldn't go beyond last page
    page_range_end = min(page_number + half_prange, numpages) + 1

    return page_range, page_range_start, page_range_end

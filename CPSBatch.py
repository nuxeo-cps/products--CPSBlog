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
from ZTUtils.Batch import opt
from ZTUtils import make_query
# XXX calling 'from ExtensionClass import Base' makes doctests fail
import ExtensionClass

# These classes have to be duplicated from ZTUtils.Batch, so that
# proper Batch class will be used.
class LazyPrevBatch(ExtensionClass.Base):
    def __of__(self, parent):
        return Batch(parent._sequence, parent._size,
                     parent.first - parent._size + parent.overlap, 0,
                     parent.orphan, parent.overlap)

class LazyNextBatch(ExtensionClass.Base):
    def __of__(self, parent):
        try: parent._sequence[parent.end]
        except IndexError: return None
        return Batch(parent._sequence, parent._size,
                     parent.end - parent.overlap, 0,
                     parent.orphan, parent.overlap)

class LazySequenceLength(ExtensionClass.Base):
    def __of__(self, parent):
        parent.sequence_length = l = len(parent._sequence)
        return l


class Batch(ZTUBatch):
    """Handles sequence batches.

    Testing empty Batch

    >>> b = Batch([], 5)
    >>> b.previous is None
    True
    >>> b.next is None
    True
    >>> len(b) == b.start == b.end == 0
    True


    Test single Batch

    >>> b = Batch([1], 5)
    >>> b.previous is None
    True
    >>> b.next is None
    True
    >>> b.start == 1
    True
    >>> b.end == 1
    True
    >>> len(b)
    1
    >>> b.sequence_length
    1


    Test orphans

    >>> b = Batch(range(6), 5, orphan=3)
    >>> b.next is None
    True
    >>> len(b)
    6
    >>> b.sequence_length
    6
    >>> b = Batch(range(7), 5, orphan=3)
    >>> b.next is None
    True
    >>> len(b)
    7
    >>> b.sequence_length
    7
    >>> b = Batch(range(8), 5)
    >>> len(b)
    5
    >>> b.sequence_length
    8
    >>> len(b.next)
    3


    Test limit case where batch length is equal to size + orphans

    >>> b = Batch(range(12), size=10, start=1, end=0, orphan=3, overlap=0)
    >>> b.length
    11
    >>> b.end
    12
    >>> b = Batch(range(14), size=10, start=1, end=0, orphan=3, overlap=0)
    >>> b.length
    13
    >>> b.end
    14
    >>> b = Batch(range(15), size=10, start=1, end=0, orphan=3, overlap=0)
    >>> b.length
    10
    >>> b.end
    11
    """
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
        """Makes the url for a given page

        >>> b = Batch(range(30), size=10, overlap=0)

        Test method with default value of page_number

        >>> b.getPageUrl({})
        'b_start:int=0'

        Pass some page_number values

        >>> b.getPageUrl({}, 1)
        'b_start:int=0'
        >>> b.getPageUrl({}, 2)
        'b_start:int=10'
        >>> b.getPageUrl({}, 3)
        'b_start:int=20'

        Test method with default value of page_number for next batches

        >>> b.next.getPageUrl({})
        'b_start:int=10'
        >>> b.next.next.getPageUrl({})
        'b_start:int=20'
        """
        if page_number is None:
            page_number = self.cur_page
        b_start = page_number * (self.size - self.overlap) - self.size
        return make_query(form_dict, b_start=b_start)

    def getNavigationUrls(self, form_dict, nav_list=None):
        """Returns complete list of pairs (page number, url) for navigation
        links. Serves as a helper method for urls methods.

        >>> b = Batch(sequence=range(30), size=10, overlap=0)

        Test with default parameter and check that it returns the same results
        for every batch in chain.

        >>> b.getNavigationUrls({})
        [(1, 'b_start:int=0'), (2, 'b_start:int=10'), (3, 'b_start:int=20')]
        >>> b.next.getNavigationUrls({})
        [(1, 'b_start:int=0'), (2, 'b_start:int=10'), (3, 'b_start:int=20')]
        >>> b.next.next.getNavigationUrls({})
        [(1, 'b_start:int=0'), (2, 'b_start:int=10'), (3, 'b_start:int=20')]
        """
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
    """Calculates the page range for the navigation quick links.
    page_number is current page for which we want to get page range.

    Check that page_range will always be odd number

    >>> cpr = calculate_page_range
    >>> page_range, pr_start, pr_end = cpr(page_number=1, numpages=5, page_range=8)
    >>> page_range
    7
    >>> page_range, pr_start, pr_end = cpr(page_number=1, numpages=5, page_range=7)
    >>> page_range
    7

    Test limit case where page_range greater then numpages

    >>> page_range, pr_start, pr_end = cpr(page_number=1, numpages=5, page_range=7)
    >>> pr_start
    1
    >>> pr_end
    5
    >>> page_range, pr_start, pr_end = cpr(page_number=4, numpages=5, page_range=7)
    >>> pr_start
    1
    >>> pr_end
    6

    Normal case

    >>> page_range, pr_start, pr_end = cpr(page_number=7, numpages=14, page_range=3)
    >>> pr_start
    6
    >>> pr_end
    9
    """
    # page range is the number of pages linked to in the navigation,
    # always odd number.
    page_range = max(0 , page_range + page_range % 2 - 1)

    half_prange = (page_range - 1) / 2

    # start shouldn't be negative
    page_range_start = max(1, page_number - half_prange)

    # end shouldn't go beyond last page
    page_range_end = min(page_number + half_prange, numpages) + 1

    return page_range, page_range_start, page_range_end

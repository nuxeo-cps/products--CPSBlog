## Script (Python) "getCustomBoxTypes"
##parameters=
# $Id$
"""Return custom box types."""

items = [{'category': 'blogcalendarbox',
          'title': 'portal_type_BlogCalendarBox_title',
          'desc':'portal_type_BlogCalendarBox_description',
          'types': [{'provider': 'cpsblog',
                     'id': 'default',
                     'desc': 'description_blog_blogcalendarbox_default'},
                    ]
          },
         {'category': 'basebox',
          'title': 'portal_type_BlogSearchBox_title',
          'desc':'portal_type_BlogSearchBox_description',
          'types': [{'provider': 'cpsblog',
                     'id': 'blogsearch',
                     'desc': 'description_blog_blogsearchbox_default'},
                    ]
          },
         ]

return items

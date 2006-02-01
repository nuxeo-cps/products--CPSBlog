##parameters=state_change
blog_proxy = state_change.object
blog_rel_url = context.portal_url.getRelativeContentURL(blog_proxy)

ptool = context.portal_cpsportlets

# Calendar portlet

kw = {'slot': 'latest_doc',
      'order': 0,
      'Title': blog_proxy.Title(),
      'render_method': 'blogcalendar_portlet',
      }
ptool.createPortlet(ptype_id='Custom Portlet', context=blog_proxy, **kw)

# Search portlet

kw = {'slot': 'latest_doc',
      'order': 0,
      'Title': 'Search',
      }
ptool.createPortlet(ptype_id='Search Portlet', context=blog_proxy, **kw)

# Archives portlet

kw = {'slot' : 'latest_doc',
      'order': 0,
      'Title' : 'Archives',
      'render_method' : 'blogarchive_portlet',
      }
ptool.createPortlet(ptype_id='Custom Portlet', context=blog_proxy, **kw)

# Categories portlet

kw = {'slot' : 'latest_doc',
      'order': 0,
      'Title' : 'Categories',
      'render_method' : 'blogcategories_portlet',
      }
ptool.createPortlet(ptype_id='Custom Portlet', context=blog_proxy, **kw)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This file is part of the prometeo project.

This program is free software: you can redistribute it and/or modify it 
under the terms of the GNU Lesser General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

__author__ = 'Emanuele Bertoldi <emanuele.bertoldi@gmail.com>'
__copyright__ = 'Copyright (c) 2011 Emanuele Bertoldi'
__version__ = '0.0.2'

from django.db.models.signals import post_syncdb
from django.utils.translation import ugettext_noop as _

from prometeo.core.widgets.models import *

def install(sender, **kwargs):
    # Regions.
    footer_region, is_new = Region.objects.get_or_create(
        slug="footer",
        description=_("Footer")
    )
    
    sidebar_region, is_new = Region.objects.get_or_create(
        slug="sidebar",
        description=_("Sidebar")
    )
    
    # Widgets.
    powered_by_widget, is_new = Widget.objects.get_or_create(
        title=_("Powered by"),
        slug="powered-by",
        description=_("Info about Prometeo"),
        source="prometeo.core.widgets.base.dummy",
        template="widgets/powered-by.html",
        context="{\"text\": \"Prometeo\", \"url\": \"http://code.google.com/p/prometeo-erp/\"}",
        show_title=False,
        region=footer_region
    )
    
    post_syncdb.disconnect(install)

post_syncdb.connect(install)

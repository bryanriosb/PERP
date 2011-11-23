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
__version__ = '0.0.5'

from django.conf.urls.defaults import *

urlpatterns = patterns('prometeo.core.notifications.views',

    # Notifications.
    url(r'^users/(?P<username>[\w\d\@\.\+\-\_]+)/notifications/$', view='notification_list', name='notification_list'),
    url(r'^users/(?P<username>[\w\d\@\.\+\-\_]+)/notifications/(?P<id>\d+)/$', view='notification_detail', name='notification_detail'),
    url(r'^users/(?P<username>[\w\d\@\.\+\-\_]+)/notifications/(?P<id>\d+)/delete/$', view='notification_delete', name='notification_delete')
)
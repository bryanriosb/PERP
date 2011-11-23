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

from django.core.urlresolvers import reverse
from django.db.models.signals import post_syncdb
from django.utils.translation import ugettext_noop as _

from prometeo.core.menus.models import *
from prometeo.core.notifications.models import Signature

def install(sender, **kwargs):
    main_menu, is_new = Menu.objects.get_or_create(slug="main")

    # Menus.
    project_menu, is_new = Menu.objects.get_or_create(
        slug="project_menu",
        description=_("Main menu for projects")
    )

    milestone_menu, is_new = Menu.objects.get_or_create(
        slug="milestone_menu",
        description=_("Main menu for milestones")
    )

    ticket_menu, is_new = Menu.objects.get_or_create(
        slug="ticket_menu",
        description=_("Main menu for tickets")
    )
    
    # Links.
    projects_link, is_new = Link.objects.get_or_create(
        title=_("Projects"),
        slug="projects",
        description=_("Project management"),
        url=reverse("project_list"),
        menu=main_menu
    )

    project_dashboard_link, is_new = Link.objects.get_or_create(
        title=_("Dashboard"),
        slug="project_dashboard",
        url="{{ object.get_absolute_url }}",
        menu=project_menu
    )

    project_milestones_link, is_new = Link.objects.get_or_create(
        title=_("Milestones"),
        slug="project_milestones",
        url="{% url milestone_list object.code %}",
        menu=project_menu
    )

    project_tickets_link, is_new = Link.objects.get_or_create(
        title=_("Tickets"),
        slug="project_tickets",
        url="{% url ticket_list object.code %}",
        menu=project_menu
    )

    project_timeline_link, is_new = Link.objects.get_or_create(
        title=_("Timeline"),
        slug="project_timeline",
        url="{% url project_timeline object.code %}",
        menu=project_menu
    )

    milestone_dashboard_link, is_new = Link.objects.get_or_create(
        title=_("Dashboard"),
        slug="milestone_dashboard",
        url="{{ object.get_absolute_url }}",
        menu=milestone_menu
    )

    milestone_tickets_link, is_new = Link.objects.get_or_create(
        title=_("Tickets"),
        slug="milestone_tickets",
        url="{% url milestone_tickets object.project.code object.code %}",
        menu=milestone_menu
    )

    milestone_timeline_link, is_new = Link.objects.get_or_create(
        title=_("Timeline"),
        slug="milestone_timeline",
        url="{% url milestone_timeline object.project.code object.code %}",
        menu=milestone_menu
    )

    ticket_details_link, is_new = Link.objects.get_or_create(
        title=_("Details"),
        slug="ticket_details",
        url="{{ object.get_absolute_url }}",
        menu=ticket_menu
    )

    ticket_tasks_link, is_new = Link.objects.get_or_create(
        title=_("Tasks"),
        slug="ticket_tasks",
        url="{% url ticket_tasks object.project.code object.code %}",
        menu=ticket_menu
    )

    ticket_timeline_link, is_new = Link.objects.get_or_create(
        title=_("Timeline"),
        slug="ticket_timeline",
        url="{% url ticket_timeline object.project.code object.code %}",
        menu=ticket_menu
    )

    # Signatures.
    project_created_signature, is_new = Signature.objects.get_or_create(
        title=_("Project created"),
        slug="project-created"
    )

    project_changed_signature, is_new = Signature.objects.get_or_create(
        title=_("Project changed"),
        slug="project-changed"
    )

    project_deleted_signature, is_new = Signature.objects.get_or_create(
        title=_("Project deleted"),
        slug="project-deleted"
    )

    milestone_created_signature, is_new = Signature.objects.get_or_create(
        title=_("Milestone created"),
        slug="milestone-created"
    )

    milestone_changed_signature, is_new = Signature.objects.get_or_create(
        title=_("Milestone changed"),
        slug="milestone-changed"
    )

    milestone_deleted_signature, is_new = Signature.objects.get_or_create(
        title=_("Milestone deleted"),
        slug="milestone-deleted"
    )

    ticket_created_signature, is_new = Signature.objects.get_or_create(
        title=_("Ticket created"),
        slug="ticket-created"
    )

    ticket_changed_signature, is_new = Signature.objects.get_or_create(
        title=_("Ticket changed"),
        slug="ticket-changed"
    )

    ticket_deleted_signature, is_new = Signature.objects.get_or_create(
        title=_("Ticket deleted"),
        slug="ticket-deleted"
    )
    
    post_syncdb.disconnect(install)

post_syncdb.connect(install)
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

import re

from django import template
from django.utils.translation import ugettext as _
from django.template.loader import render_to_string

from ..models import Menu

register = template.Library()

class MenuNode(template.Node):
    def __init__(self, slug, html_template):
        self.slug = slug
        self.html_template = html_template

    def render(self, context):
        output = ''
        slug = self.slug.resolve(context)
        try:
            menu = Menu.objects.get(slug=slug)
            user = context['user']
            links = menu.links.all()
            user_perms = user.user_permissions.all()
            for link in links:
                perms = link.only_with_perms.all()
                link.authorized = True
                link.title = template.Template(link.title).render(context)
                link.description = template.Template(link.description).render(context)
                link.url = template.Template(link.url).render(context)
                if not (user.is_staff or user.is_superuser):
                    if link.only_authenticated and not user.is_authenticated():
                        link.authorized = False
                    elif link.only_staff and not (user.is_staff or user.is_superuser):
                        link.authorized = False
                    elif link.only_with_perms:
                        for perm in perms:
                            if perm not in user_perms:
                                link.authorized = False
                                break
        except Menu.DoesNotExist:
            links = None
        if isinstance(self.html_template, template.Variable):
            html_template = self.html_template.resolve(context)
        else:
            html_template = self.html_template
        if links:
            output += render_to_string(html_template, { 'links': links }, context)
        return output

@register.tag
def menu(parser, token):
    """
    Renders a menu.

    Example tag usage: {% menu menu_slug [html_template] %}
    """
    try:
        args = token.split_contents()
        if len(args) < 2:
            raise ValueError
        elif len(args) == 2:
            slug = parser.compile_filter(args[1])
            html_template = 'menus/menu.html'
        else:
            slug = parser.compile_filter(args[1])
            html_template = parser.compile_filter(args[2])
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires one or two arguments" % token.contents.split()[0]

    return MenuNode(slug, html_template)

@register.simple_tag(takes_context=True)
def matchlink(context, link, ref_url, css_class="active"):
    """
    Checks if the link instance is the best match for "ref_url".

    Example tag usage: {% matchlink link ref_url %}
    """
    links = link.menu.links.all()
    score = len(ref_url)
    matched_link = None
    for l in links:
        url = template.Template(l.url).render(context)
        if url == ref_url or ref_url.startswith(url):
            remainder = ref_url[len(url):]
            current_score = len(remainder)
            if current_score < score:
                score = current_score
                matched_link = l                    
    if matched_link == link:
        return " class=\"%s\"" % css_class
    return ""

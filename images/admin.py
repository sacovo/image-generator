
# Copyright (c) 2020 Sandro Covo
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation and/or
# other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from django.contrib import admin
from images import models

# Register your models here.


@admin.register(models.Font)
class FontAdmin(admin.ModelAdmin):
    list_display = [
        'font_name'
    ]


class TextOverlayInline(admin.StackedInline):
    model = models.TextOverlay

    fieldsets = (
        (None, {
            'fields': ('name', ('font', 'font_size'), 'force_all_caps', 'font_color')
        }),
        ('position', {
            'fields': (('horizontal_align', 'vertical_align'), ('x', 'y')),
            'classes': ('collapse',)
        }),
        ('sizing', {
            'fields': ('max_width', 'min_width', 'line_space'),
            'classes': ('collapse',)
        }),
        ('background', {
            'fields': ('enable_background', 'background_color', ('padding_top', 'padding_bottom'), ('padding_left', 'padding_right')),
            'classes': ('collapse',)
        }),
        ('customization', {
            'fields': ('override_font_size', 'override_font_color', 'override_background_color'),
            'classes': ('collapse',)
        })
    )

    extra = 0


class ImageOverlayInline(admin.StackedInline):
    model = models.ImageOverlay

    fieldsets = (
        (None, {
            'fields': ('source', ('horizontal_align', 'vertical_align'), ('x', 'y'), ('width', 'height'))
        }),
    )

    extra = 0


@admin.register(models.Template)
class TemplateAdmin(admin.ModelAdmin):
    inlines = [
        TextOverlayInline,
        ImageOverlayInline,
    ]

    list_display = [
        'name', 'plattform', 'width', 'height', 'language_code'
    ]

    list_filters = [
        'language_code', 'plattform'
    ]

    fieldsets = (
        (None, {
            'fields': ('name', 'plattform', ('width', 'height'), 'preview', 'black_and_white', 'language_code')
        }),
    )

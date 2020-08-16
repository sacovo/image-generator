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

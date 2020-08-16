from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from colorfield.fields import ColorField

# Create your models here.

class Template(models.Model):
    name = models.CharField(max_length=80)

    plattform = models.CharField(max_length=30)

    width = models.IntegerField(default=1080)
    height = models.IntegerField(default=1080)

    preview = models.ImageField(upload_to="preview", blank=True)

    black_and_white = models.BooleanField(default=False)

    language_code = models.CharField(max_length=2)

    def ratio(self):
        return self.width / self.height

    def get_absolute_url(self):
        return reverse('template_detail', args=(self.pk,))

    class Meta:
        ordering = ['plattform', 'name']


VERTICAL_ALIGNMENTS = (
    ('top', _("top")),
    ('middle', _("middle")),
    ('bottom', _("bottom")),
)

HORIZONTAL_ALIGNMENTS = (
    ('left', _("left")),
    ('center', _("center")),
    ('right', _("right")),
)


class ImageOverlay(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()

    width = models.IntegerField(blank=True)
    height = models.IntegerField(blank=True)

    vertical_align = models.CharField(max_length=10, choices=VERTICAL_ALIGNMENTS)
    horizontal_align = models.CharField(max_length=10, choices=HORIZONTAL_ALIGNMENTS)

    source = models.ImageField()

    template = models.ForeignKey(Template, models.CASCADE, 'image_overlays')


class Font(models.Model):
    font_name = models.CharField(max_length=100)

    truetype_file = models.FileField(upload_to='fonts')

    def __str__(self):
        return self.font_name


class TextOverlay(models.Model):
    name = models.CharField(max_length=80)
    font = models.ForeignKey(Font, models.CASCADE)

    font_size = models.SmallIntegerField()
    override_font_size = models.BooleanField(default=False)

    font_color = ColorField(blank=True)
    override_font_color = models.BooleanField(default=False)

    line_space = models.IntegerField(default=0)

    max_width = models.IntegerField()
    min_width = models.IntegerField()

    x = models.IntegerField()
    y = models.IntegerField()

    vertical_align = models.CharField(max_length=10, choices=VERTICAL_ALIGNMENTS)
    horizontal_align = models.CharField(max_length=10, choices=HORIZONTAL_ALIGNMENTS)

    force_all_caps = models.BooleanField(default=False)

    enable_background = models.BooleanField()

    background_color = ColorField(blank=True)
    override_background_color = models.BooleanField(default=False)

    padding_top = models.IntegerField(default=10)
    padding_bottom = models.IntegerField(default=15)

    padding_left = models.IntegerField(default=10)
    padding_right = models.IntegerField(default=10)

    template = models.ForeignKey(Template, models.CASCADE, 'text_overlays')

    def __str__(self):
        return self.name


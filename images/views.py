
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

from django.shortcuts import render, get_object_or_404
from PIL import Image, ImageDraw, ImageFont, ImageColor
from django.http.response import FileResponse, HttpResponse
from images import models
import io

# Create your views here.

def template_list_view(request):
    template_list = models.Template.objects.all()

    if query := request.GET.get('q', ''):
        template_list = template_list.filter(name__icontains=query)

    return render(request, 'images/template_list.html', {
        'template_list': template_list
    })


def template_detail_view(request, pk):
    template = get_object_or_404(models.Template, pk=pk)

    return render(request, 'images/template_detail.html', {
        'template': template
    })

def draw_img_overlay(overlay, img):
    if overlay.vertical_align == 'top':
        y = overlay.y
    if overlay.vertical_align == 'middle':
        y = overlay.y - overlay.height / 2
    if overlay.vertical_align == 'bottom':
        y = overlay.y - overlay.height

    if overlay.horizontal_align == 'left':
        x = overlay.x
    if overlay.horizontal_align == 'center':
        x = overlay.x - overlay.width / 2
    if overlay.horizontal_align == 'right':
        x = overlay.x - overlay.width

    img2 = Image.open(overlay.source).convert('RGBA').resize((overlay.width, overlay.height))
    img.paste(img2, (x, y), img2)


def draw_text_overlay(overlay, draw, data):
    font_size = int(data.get(f'size_{overlay.pk}', str(overlay.font_size)))
    font = ImageFont.truetype(overlay.font.truetype_file, font_size)
    complete_text = data.get(f'text_{overlay.pk}')
    if overlay.force_all_caps:
        complete_text = complete_text.upper()
    words = complete_text.split()

    current_line = ''
    texts = []

    for word in words:
        if font.getsize(current_line + ' ' + word)[0] < overlay.max_width:
            current_line += ' ' + word if current_line else word
        elif current_line:
            texts.append(current_line)
            current_line = word
        else:
            current_line = word

    if current_line:
        texts.append(current_line)

    line_count = 0

    width, height = font.getsize(complete_text + ',')
    if overlay.vertical_align == 'top':
        top_y = overlay.y
    elif overlay.vertical_align == 'middle':
        top_y = overlay.y - (overlay.line_space + height) * len(texts) / 2
    elif overlay.vertical_align == 'bottom':
        top_y = overlay.y - (overlay.line_space + height) * len(texts)

    for text in texts:
        width, _ = font.getsize(text)
        y = top_y  + (overlay.line_space + height) * line_count
        if overlay.horizontal_align == 'left': # y
            x = overlay.x
        elif overlay.horizontal_align == 'center':
            x = overlay.x - width/2
        elif overlay.horizontal_align == 'right':
            x = overlay.x - width
        if overlay.enable_background:
            if overlay.horizontal_align == 'left':
                box = [
                    (x - overlay.padding_left, y - overlay.padding_top),
                    (x + max(width, overlay.min_width) + overlay.padding_right, y + height + overlay.padding_bottom)
                ]
            elif overlay.horizontal_align == 'center':
                box = [
                    (overlay.x - max(width, overlay.min_width)/2 - overlay.padding_left, y - overlay.padding_top),
                    (overlay.x + max(width, overlay.min_width)/2 + overlay.padding_right, y + height + overlay.padding_bottom),
                ]
            elif overlay.horizontal_align == 'right':
                box = [
                    (overlay.x - max(width, overlay.min_width) - overlay.padding_left, y - overlay.padding_top),
                    (overlay.x + overlay.padding_right, y + height + overlay.padding_bottom)
                ]
            background_color = data.get(f'background_color_{overlay.pk}', overlay.background_color)
            draw.rectangle(box, fill=ImageColor.getrgb(background_color))
        font_color = data.get(f'font_color_{overlay.pk}', overlay.font_color)
        draw.text((x, y), text, font=font, fill=ImageColor.getrgb(font_color))
        line_count += 1

def draw_template(template, draw, img, data):
    for text_overlay in template.text_overlays.all():
        draw_text_overlay(text_overlay, draw, data)
    for image_overlay in template.image_overlays.all():
        draw_img_overlay(image_overlay, img)


def generate_image(request, pk):
    template = get_object_or_404(models.Template, pk=pk)
    img = Image.open(io.BytesIO(request.FILES['source_img'].read())).convert('RGBA')

    if template.black_and_white:
        img = img.convert('L').convert('RGBA')

    draw = ImageDraw.Draw(img)

    draw_template(template, draw, img, request.POST)

    response = HttpResponse(content_type="image/png")
    img.convert('RGB', dither=None).save(response, "PNG")
    return response

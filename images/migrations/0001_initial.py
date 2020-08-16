# Generated by Django 3.1 on 2020-08-16 09:50

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Font',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('font_name', models.CharField(max_length=100)),
                ('truetype_file', models.FileField(upload_to='fonts')),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('plattform', models.CharField(max_length=30)),
                ('width', models.IntegerField(default=1080)),
                ('height', models.IntegerField(default=1080)),
                ('preview', models.ImageField(blank=True, upload_to='preview')),
                ('black_and_white', models.BooleanField(default=False)),
                ('language_code', models.CharField(max_length=2)),
            ],
            options={
                'ordering': ['plattform', 'name'],
            },
        ),
        migrations.CreateModel(
            name='TextOverlay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('font_size', models.SmallIntegerField()),
                ('override_font_size', models.BooleanField(default=False)),
                ('font_color', colorfield.fields.ColorField(blank=True, default='', max_length=18)),
                ('override_font_color', models.BooleanField(default=False)),
                ('line_space', models.IntegerField(default=0)),
                ('max_width', models.IntegerField()),
                ('min_width', models.IntegerField()),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('vertical_align', models.CharField(choices=[('top', 'top'), ('middle', 'middle'), ('bottom', 'bottom')], max_length=10)),
                ('horizontal_align', models.CharField(choices=[('left', 'left'), ('center', 'center'), ('right', 'right')], max_length=10, verbose_name='Vertikale Ausrichtung')),
                ('force_all_caps', models.BooleanField(default=False)),
                ('enable_background', models.BooleanField()),
                ('background_color', colorfield.fields.ColorField(blank=True, default='', max_length=18)),
                ('override_background_color', models.BooleanField(default=False)),
                ('padding_top', models.IntegerField(default=10)),
                ('padding_bottom', models.IntegerField(default=15)),
                ('padding_left', models.IntegerField(default=10)),
                ('padding_right', models.IntegerField(default=10)),
                ('font', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='images.font')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='text_overlays', to='images.template')),
            ],
        ),
        migrations.CreateModel(
            name='ImageOverlay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('width', models.IntegerField(blank=True)),
                ('height', models.IntegerField(blank=True)),
                ('vertical_align', models.CharField(choices=[('top', 'top'), ('middle', 'middle'), ('bottom', 'bottom')], max_length=10)),
                ('horizontal_align', models.CharField(choices=[('left', 'left'), ('center', 'center'), ('right', 'right')], max_length=10)),
                ('source', models.ImageField(upload_to='')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_overlays', to='images.template')),
            ],
        ),
    ]

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

# This was first coded (not by me) to work with nautilus and using mediainfo, 
# to display properties of mostly images and PDFs
# I intentionally removed the support for images and PDFs to only 
# focus on Video and using ffmpeg instead of mediainfo
# This was made for my Bro Astoria
# Ka 2022

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gi
try:
    gi.require_version('Caja', '2.0')
    gi.require_version('GObject', '2.0')
except ValueError as error:
    print(error)
    exit(1)
from gi.repository import Caja as FileManager
from gi.repository import GObject

import urllib
import urllib.parse

import ffmpeg

# locale
import sys
import os
import json
import math
import locale
import gettext

class MediaInfoData:
    def __init__(self, path_to_video):
        self.path_to_video = path_to_video

        if os.path.isfile(path_to_video):
            has_video = False
            has_audio = False
            vid = ffmpeg.probe(path_to_video)
            video_stream = next((stream for stream in vid['streams'] if stream['codec_type'] == 'video'), None)
            if video_stream is None:
                self._duration = "N/A"
                self._videoformat = "N/A"
                self._width = "N/A"
                self._height = "N/A"
                self._codec_id = "N/A"
                self._encoded_library_name = "N/A"
                has_video = False
            else:
                has_video = True
                try:            
                    self._duration = int(float(video_stream['duration']))
                except: 
                    self._duration = "N/A"
                try:
                    self._videoformat = vid['format']['format_long_name']
                except:
                    self._videoformat = "N/A"
                try:
                    self._width = int(video_stream['width'])
                except:
                    self._width = "N/A"
                try:
                    self._height = int(video_stream['height'])
                except:
                    self._height = "N/A"
                try:    
                    self._codec_id = video_stream['codec_name']
                except:
                    self._codec_id = "N/A"
                try:
                    self._encoded_library_name = video_stream['codec_long_name']
                except:
                     self._encoded_library_name = "N/A"
            
            audio_stream = next((stream for stream in vid['streams'] if stream['codec_type'] == 'audio'), None)
            if audio_stream is None:
                self._audioformat = "No Audio"
                has_audio = False
            else:
                has_audio = True
                try:
                    self._audioformat = audio_stream['codec_name']
                except:
                    self._audioformat = "N/A"

                if self._duration == "N/A":
                    try:
                        self._duration = int(float(audio_stream['duration']))
                    except:
                        self._duration = "N/A"

            if has_video:
                if has_audio:
                    self._video_audio = "Video/Audio"
                else:
                    self._video_audio = "Video only"
            else:
                if has_audio:
                    self._video_audio = "Audio only"
                else:
                    self._video_audio = "None"

    def get_duration(self):
        """TODO: Docstring for get_duration.
        :returns: TODO

        """
        return self._duration

    def get_video_format(self):
        """TODO: Docstring for get_videoformat.
        :returns: TODO

        """
        return self._videoformat

    def get_width(self):
        """TODO: Docstring for get_width.
        :returns: TODO

        """
        return self._width

    def get_height(self):
        """TODO: Docstring for get_height.
        :returns: TODO

        """
        return self._height

    def get_audioformat(self):
        """TODO: Docstring for get_audioformat.
        :returns: TODO

        """
        return self._audioformat

    def get_encoded_library_name(self):
        return str(self._encoded_library_name)

    def get_duration_string(self):
        """TODO: Docstring for get_duration_string.
        :returns: TODO

        """
        if self._duration == "N/A":
            return self._duration
        else:
            seconds = int(float(self._duration))
            duration = '{:02d}:{:02d}:{:02d}'.format(int(seconds / 3600),
                                                     int((seconds / 60) % 60),
                                                     int(seconds % 60))
            return duration
    
    def get_codec(self):
        return self._codec_id


    def get_resolution(self):
        if self._width == "N/A" or self._height == "N/A":
            return "N/A"
        resolution = '{:02d}x{:02d}'.format(int(self._width),
                                                     int(self._height))
        return resolution
    
    def get_video_audio(self):
        return self._video_audio

    def get_definition(self):
        if self._width == "N/A" or self._height == "N/A":
            return "N/A"
        else:
            if self._width == 176  and self._height == 144:
                return "QCIF"            
            if self._width == 426  and self._height == 240:
                return "240p"
            if self._width == 640  and self._height == 360:
                return "360p"
            if self._width == 854  and  self._height == 480:
                return "SD (480p)"
            if self._width == 1280 and self._height == 720:
                return "HD (720p)"
            if self._width == 1920 and self._height == 1080:
                return "Full HD (1080p)"
            if self._width == 2560 and self._height == 1440:
                return "Quad HD (1440p)"
            if self._width >= 3840 and self._width <= 4096 and self._height == 2160:
                return "4K (2160p)"
            if self._width == 7680 and self._height == 4320:
                return "8K (7680p)"
        return "N/A"


class ColumnExtension(GObject.GObject,
                      FileManager.ColumnProvider,
                      FileManager.InfoProvider):
    def __init__(self):
        pass

    def get_columns(self):
        return (
            FileManager.Column(name='FileManagerPython::format_column', 
                               attribute='format',
                               label='Video Format',
                               description='Video Format'),
            FileManager.Column(name='FileManagerPython::codec_column',
                               attribute='codec_id',
                               label='Codec',
                               description='Video Codec'),
            FileManager.Column(name='FileManagerPython::audio_format_column',
                               attribute='audio_format',
                               label='Audio Format',
                               description='Audio Format'),
            FileManager.Column(name='FileManagerPython::encoded_library_name_column',
                               attribute='encoded_library_name',
                               label='Encoder',
                               description='Encoder'),
            FileManager.Column(name='FileManagerPython::duration_column',
                               attribute='duration',
                               label='Duration',
                               description='Duration'),
            FileManager.Column(name='FileManagerPython::resolution_column',
                               attribute='resolution',
                               label='Resolution',
                               description='Resolution'),
                               

            FileManager.Column(name='\
FileManagerPython::width_column',
                               attribute='width',
                               label='Width',
                               description=
                                    'Image/video/pdf width (pixel/mm)'),
            FileManager.Column(name='\
FileManagerPython::height_column',
                               attribute='height',
                               label='Height',
                               description=
                                    'Video height (pixel/mm)'),
            FileManager.Column(name='\
FileManagerPython::video_audio_column',
                               attribute='video_audio',
                               label='Video/Audio',
                               description=
                                    'Has Video and / or Audio track'),
            FileManager.Column(name='\
FileManagerPython::definition_column',
                               attribute='definition',
                               label='Definition',
                               description=
                                    'Video Definition'))


    def update_file_info(self, file):
        # set defaults to blank
        file.add_string_attribute('width', '')
        file.add_string_attribute('height', '')
        file.add_string_attribute('format', '')
        file.add_string_attribute('encoded_library_name', '')
        file.add_string_attribute('resolution', '')
        file.add_string_attribute('video_audio', '')
        file.add_string_attribute('definition', '')


        if file.get_uri_scheme() != 'file':
            return

        # strip file:// to get absolute path
        filename = urllib.parse.unquote_plus(file.get_uri()[7:])

        # video/flac handling
        if file.is_mime_type('video/x-msvideo') or\
                file.is_mime_type('video/mpeg') or\
                file.is_mime_type('video/x-ms-wmv') or\
                file.is_mime_type('video/quicktime') or\
                file.is_mime_type('video/x-quicktime') or\
                file.is_mime_type('video/MP2T') or\
                file.is_mime_type('video/mp2t') or\
                file.is_mime_type('video/3gpp') or\
                file.is_mime_type('video/mp4') or\
                file.is_mime_type('audio/x-flac') or\
                file.is_mime_type('video/x-flv') or\
                file.is_mime_type('video/x-fli') or\
                file.is_mime_type('video/x-matroska') or\
                file.is_mime_type('audio/x-wav'):
            metadata = MediaInfoData(filename)
            file.add_string_attribute('format',
                                      metadata.get_video_format())
            file.add_string_attribute('duration',
                                      metadata.get_duration_string())
            file.add_string_attribute('width',
                                      str(metadata.get_width()))
            file.add_string_attribute('height',
                                      str(metadata.get_height()))
            file.add_string_attribute('audio_format',
                                      metadata.get_audioformat())
            file.add_string_attribute('codec_id',
                                      metadata.get_codec())
            file.add_string_attribute('encoded_library_name',
                                      metadata.get_encoded_library_name())
            file.add_string_attribute('resolution',
                                      metadata.get_resolution())
            file.add_string_attribute('video_audio',
                                      metadata.get_video_audio())
            file.add_string_attribute('definition',
                                      metadata.get_definition())
        self.get_columns()

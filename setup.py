#!/usr/bin/env python
# gTranscribe is a software focussed on easy transcription of spoken words.
# Copyright (C) 2013-2014 Philip Rinn <rinni@inventati.org>
# Copyright (C) 2010 Frederik Elwert <frederik.elwert@web.de>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as 
# published by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import DistUtilsExtra.auto
assert DistUtilsExtra.auto.__version__ >= '2.18', 'gTranscribe needs DistUtilsExtra.auto >= 2.18'

DistUtilsExtra.auto.setup(
    name='gTranscribe',
    version='0.3',
    license='GPL-3',
    author='Philip Rinn',
    author_email='rinni@inventati.org',
    description='gTranscribe',
    long_description='gTranscribe is a software focussed on easy transcription of spoken words.',
    url='https://github.com/innir/gtranscribe'
    )

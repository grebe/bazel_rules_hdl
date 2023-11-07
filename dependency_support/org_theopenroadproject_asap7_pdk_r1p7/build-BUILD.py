#!/usr/bin/env python3
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pathlib

__path__ = pathlib.Path(__file__).resolve()
__dir__ = __path__.parent

license_header = []
for l in open(__path__).readlines()[1:]:
    if not l.startswith('#'):
        break
    license_header.append(l)

header = []
header.extend(license_header)
header.append('\n')
header.append('# DO NOT EDIT - This file is generated by `build-BUILD.py` script!\n')
header.append('\n')
header.append('''\
"""
ASAP7 -- Arizona State University 7nm "predictive" PDK

The PDK has RVT, LVT and SLVT based transistors.

The ASAP7 PDK currently provides 3 standard cell libraries;
 * Two revisions (rev 27 and rev 28) of a 7.5 track library
 * One revision (rev 26) of a 6 track library

These libraries are mapped to each of the transistor types;
 * RVT -> R
 * LVT -> L
 * SLVT -> SL

It also provides "4x scaled" versions of these libraries. These versions reuse
the same timing information but have their sizes scaled up.

The libraries provide 3 corners,
 * FF - fast
 * TT - typical
 * SS - slow

By default if not otherwise explicitly specified the default selection will be
the 7.5 track library using RVT transistors and slow corner.
"""

load("@rules_hdl//pdk:open_road_configuration.bzl", "open_road_pdk_configuration")
load("@rules_hdl//dependency_support/org_theopenroadproject_asap7_pdk_r1p7:asap7.bzl", "asap7_cell_library")
load("@rules_hdl//dependency_support/org_theopenroadproject_asap7_pdk_r1p7:asap7.bzl", "asap7_cells_files")
load("@rules_hdl//dependency_support/org_theopenroadproject_asap7_pdk_r1p7:asap7.bzl", "asap7_srams_files")

''')

for scdir in list(sorted(__dir__.parent.glob('org_theopenroadproject_asap7sc*'))):
    print('Processing ', scdir)
    output = []
    output.extend(header)

    common_file = scdir / 'common.bzl'
    assert common_file.exists(), common_file

    input_files = [common_file] + list(scdir.glob('cells-*.bzl'))
    input_files.sort()
    for input_file in input_files:
        output.append(f"""
# From {scdir.name}/{input_file.name}
""")
        print('Reading', input_file)
        with open(input_file) as f:
            lines = f.readlines()
            while lines.pop(0) in license_header:
                continue
            output.extend(lines)

    output_file = scdir / 'bundled.BUILD.bazel'
    print('Writing', output_file)
    with open(output_file, 'w') as f:
        for l in output:
            f.write(l)

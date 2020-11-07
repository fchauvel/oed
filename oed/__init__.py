#
# OeD - Open-ended Dependency Analyser
#
# Copyright (C) 2020 -- 2021 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


class Requirement:

    @property
    def is_open_ended(self):
        return True # Fake


class OeD:

    def __init__(self):
        pass


    def select(self, source_name, source_version, target_name):
        return Requirement()

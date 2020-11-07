#
# OeD - Open-ended Dependency Analyser
#
# Copyright (C) 2020 -- 2021 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from oed import OeD

from unittest import TestCase


class SelectOeD(TestCase):

    def setUp(self):
        self.system = OeD()
        
    def test_select_oed(self):
        requirement = self.system.select("Sphinx", "2.3", "alabaster")
        self.assertTrue(requirement.is_open_ended)

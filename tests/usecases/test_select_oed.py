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
from oed.library import UnknownPackage, UnknownRelease

from tests.usecases.stubs import PackagesStub

from unittest import TestCase


        
class SelectOeD(TestCase):

    
    def setUp(self):
        self.packages = PackagesStub()
        self.system = OeD(self.packages)
        
    def test_select_o(self):
        requirements = self.system.select("Sphinx", "1.0", "alabaster")
        self.assertTrue(all(r.is_open_ended for r in requirements))

    def test_when_version_does_not_exist(self):
        with self.assertRaises(UnknownRelease):
            self.system.select("Sphinx", "2.0", "alabaster")

    def test_when_source_package_does_not_exist(self):
        with self.assertRaises(UnknownPackage):
            self.system.select("Unknown", "1.0", "alabaster")
            
    def test_when_target_package_does_not_exist(self):
        with self.assertRaises(UnknownPackage):
            self.system.select("Sphinx", "1.0", "unknown")

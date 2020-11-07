#
# OeD - Open-ended Dependency Analyser
#
# Copyright (C) 2020 -- 2021 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from oed import OeD, Packages, Package, Release, Requirement

from unittest import TestCase



class PackagesStub(Packages):

    def __init__(self):
        super().__init__(
            [
                Package("Sphinx",
                        [ Release("1.0",
                                  [ Requirement(self, "alabaster")])
                        ]),
                Package("alabaster",
                        [ Release("1.0"),
                          Release("2.0")])
            ]);


        
class SelectOeD(TestCase):

    
    def setUp(self):
        self.packages = PackagesStub()
        self.system = OeD(self.packages)
        
    def test_select_oed(self):
        requirements = self.system.select("Sphinx", "1.0", "alabaster")
        self.assertTrue(all(r.is_open_ended for r in requirements))

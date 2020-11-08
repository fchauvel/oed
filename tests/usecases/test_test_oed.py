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

from tests.usecases.stubs import PackagesStub

from unittest  import TestCase


class TestOeD(TestCase):

    def setUp(self):
        packages = PackagesStub()
        self.system = OeD(packages)


    def test_success_scenario(self):
        initial_test_count = len(self.system.experiments())

        session = self.system.new_testing_session()
        requirements = self.system.select("Sphinx", "1.0", "alabaster")
        session.add(requirements)
        session.start()

        self.assertTrue(initial_test_count + 2)
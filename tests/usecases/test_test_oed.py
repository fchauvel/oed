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
from oed.laboratory import Laboratory

from tests.usecases.stubs import PackagesStub

from unittest  import TestCase


class TestOeD(TestCase):

    def setUp(self):
        packages = PackagesStub()
        laboratory = Laboratory()
        self.system = OeD(packages, laboratory)

    def test_success_scenario(self):
        session = self.system.new_testing_session()
        requirements = self.system.select("Sphinx", "1.0", "alabaster")
        session.add(requirements)
        session.start()

        self.assertEqual(2, len(self.system.experiments()))
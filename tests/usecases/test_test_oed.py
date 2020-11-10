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

        experiments = self.system.experiments.select(lambda r: r.subject == "sphinx==1.0" \
                                                            and r.object == "alabaster==1.0")
        self.assertEqual(1, len(experiments))
        self.assertTrue(experiments[0].is_complete)
        self.assertEqual(1581, experiments[0].results.test_count)

        # 1524 passed, 24 skipped, 8 xfailed, 25 xpassed, 6 warnings in 263.43s (0:04:23) 
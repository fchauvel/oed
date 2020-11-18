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
from oed.engines.os import OSPlatform

from tests.usecases.stubs import PackagesStub

from unittest  import TestCase



class TestPlatform(OSPlatform):

    def _execute_script(self):
        with open("tests/data/sample_pytest_output.log", "r", encoding="utf-16") as sample_output:
           return sample_output.readlines()
        #return ["= 1 failed, 1537 passed, 24 skipped, 8 xfailed, 25 xpassed, 7 warnings in 325.63s (0:05:25) \n"]
    

class TestOeD(TestCase):

    def setUp(self):
        packages = PackagesStub()
        laboratory = Laboratory(platform=TestPlatform())
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
        self.assertEqual(1595, experiments[0].results.test_count)

        # 1 failed, 1537 passed, 24 skipped, 8 xfailed, 25 xpassed,
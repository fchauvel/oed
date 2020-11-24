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
        return self._sample_output()
        #return self._minimal_relevant_output()

    def _sample_output(self):
        with open("tests/data/sample_pytest_output.log",
                  "r", encoding="utf-16") as sample_output:
            return sample_output.readlines()

    def _minimal_relevant_output(self):
        return [
            "= 1 failed, 1537 passed, 24 skipped, 8 xfailed, 25 xpassed, 7 warnings in 325.63s (0:05:25) \n",
            "TOTAL                                           36332   6040  13652   1471    81%\n"
            ]

    def _fetch_content(self, url):
        with open(self.SAMPLE_WEBPAGE, "r", encoding="iso-8859-1") as htmlfile:
            return htmlfile.read()

    SAMPLE_WEBPAGE = "tests/data/sphinx_homepage.html" 


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
        self.assertEqual(1595, experiments[0].results.tests.count)
        self.assertAlmostEqual(81.0, experiments[0].results.tests.coverage,
                               delta=0.5)

        # 1 failed, 1537 passed, 24 skipped, 8 xfailed, 25 xpassed,

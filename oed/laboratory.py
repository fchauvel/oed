#
# OeD - Open-ended Dependency Analyser
#
# Copyright (C) 2020 -- 2021 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from oed.os import Shell

from traceback  import print_exc


class Experiment:

    def __init__(self, platform, source_package_name, source_release_name, required_package_name, target_release_name):
        self._platform = platform
        self._source_package_name = source_package_name
        self._source_release_name = source_release_name
        self._required_package_name  = required_package_name
        self._target_release_name = target_release_name
        self._vcs_url = "https://github.com/sphinx-doc/sphinx.git"
        self._subject = "{}=={}".format(source_package_name, source_release_name)
        self._object = "{}=={}".format(required_package_name, target_release_name)
        self._test_results = None
   

    def start(self):
        self._test_results = self._platform.run(self)

    @property
    def subject(self):
        return self._subject

    @property
    def object(self):
        return self._object

    @property
    def is_complete(self):
        return self._test_results is not None

    @property
    def results(self):
        return self._test_results


class Results:

    @property
    def test_count(self):
        return 1581 # Fake




class Platform:
    """Hides the way the experiment is run (e.g., locally, remotely, using Docker, using virtualenv)"""

    def run(self, experiment):
        pass


class OSPlatform(Platform):

    def __init__(self, workspace=None, shell=None):
        super().__init__()
        self._workspace = workspace or "tmp-test"
        self._shell = shell or Shell()

    def run(self, experiment):
            return Results()        

    def _open_shell(self):
        self._shell.start()

    def _close_shell(self):
        self._shell.close()

    def _setup_working_directory(self, name="whatever"):
        command = "mkdir {}\\{}".format(self._workspace, name)
        self._shell.execute(command)

    def _fetch_source_code(self, vcs_url):
        command = ["git", "clone", vcs_url, "sources"]
        self._shell.execute(command)

    def _create_virtual_environment(self):
        command = ["virtualenv", ".venv"]
        self._shell.execute(command)
        command = [".\\.venv\\Scripts\\activate.ps1"]
        self._shell.execute(command)

    def _activate_resolution(self, package, version):
        command = ["pip", "install", "--force", "{}=={}".format(package, version)]
        self._shell.execute(command)

    def _install_dependencies(self):
        command = ["pip", "install", "-r", "requirements.txt"]
        self._shell.execute(command)

    def _install(self, package, version):
        command = ["pip", "install", ".", "{}=={}".format(package, version)]
        self._shell.execute(command)

    def run_tests(self):
        return Results()


class Experiments:

    def __init__(self, experiments=None):
        self._experiments = experiments or []

    def select(self, predicate):
        selection = []
        for any_experiment in self._experiments:
            if predicate(any_experiment):
                selection.append(any_experiment)
        return selection

    def store(self, experiment):
        self._experiments.append(experiment)



class Laboratory:

    def __init__(self, experiments=None, platform=None):
        self._experiments = experiments or Experiments()
        self._platform = platform or OSPlatform()

    def new_experiment(self, source_package_name, source_release_name, required_package_name, required_release_name):
        experiment = Experiment(self._platform, 
                                source_package_name, 
                                source_release_name, 
                                required_package_name, 
                                required_release_name)
        self._experiments.store(experiment)
        return experiment

    @property
    def experiments(self):
        return self._experiments
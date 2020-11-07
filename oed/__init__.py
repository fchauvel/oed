#
# OeD - Open-ended Dependency Analyser
#
# Copyright (C) 2020 -- 2021 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from pkg_resources import Requirement as PKGRequirement


class Packages:

    def __init__(self, packages):
        self._packages = packages
    
    def find_requirement(self, text):
        return Requirement(self, text)

    def find_release(self, package_name, release_name):
        package = self.find_package(package_name)
        return package.find_release(release_name)
    
    def find_package(self, package_name):
        for any_package in self._packages:
            if any_package.name == package_name:
                return any_package
        raise UnknownPackage(package_name)


    
    
class Package:

    def __init__(self, name, releases):
        self._name = name
        self._releases = releases

    @property
    def name(self):
        return self._name

    def __eq__(self,  other):
        if not isinstance(other, Package):
            return False
        return self._name == other.name

    @property
    def releases(self):
        return self._releases


    def find_release(self, name):
        for any_release  in self._releases:
            if any_release.name == name:
                return any_release
        raise UnknownRelease(self._name, name)

    

class Release:

    def __init__(self, name, requirements=[]):
        self._name = name
        self._requirements = requirements

    @property
    def name(self):
        return self._name

    def find_requirements_for(self, package):
        requirements = []
        for any_requirement in self._requirements:
            if any_requirement.targets(package):
                requirements.append(any_requirement)
        return requirements

    
class Requirement:

    def __init__(self, packages, specification):
        self._packages = packages
        self._specification = PKGRequirement.parse(specification)
    
    @property
    def is_open_ended(self):
        return len(self.candidate_releases) > 1

    @property
    def candidate_releases(self):
        candidates = []
        for any_release in self.required_package.releases:
            if self.is_satisfied_by(any_release):
                candidates.append(any_release)
        return candidates

    def targets(self, package):
        return self.required_package == package
    
    @property
    def required_package(self):
        return self._packages.find_package(self._specification.key)
        

    def is_satisfied_by(self, release):
        return release.name in self._specification


class UnknownPackage(Exception):

    def __init__(self, package_name):
        super().__init__("Unknown package '{}'".format(package_name))

class UnknownRelease(Exception):

    def __init__(self, package_name, release_name):
        super().__init__("Unknown release '{}' for package '{}'".format(release_name, package_name))
    

class OeD:

    def __init__(self, packages):
        self._packages = packages

    def select(self, source_name, source_version, target_name):
        target = self._packages.find_package(target_name)
        release = self._packages.find_release(source_name, source_version)
        return release.find_requirements_for(target)

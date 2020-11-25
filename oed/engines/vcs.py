#
# OeD - Open-ended Dependency Analyser
#
# Copyright (C) 2020 -- 2021 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from requests import get


from re import findall



class Repository:

    @staticmethod
    def from_URL(url):
        return None

    @property
    def URL(self):
        raise RuntimeError("Calling the abstract method 'clone_URL'")
        
    @property
    def clone_URL(self):
        raise RuntimeError("Calling the abstract method 'clone_URL'")


    def find_tag_for(self, version_name):
        raise RuntimeError("Calling the abstract method 'find_tag_for'")
    
    

class Github(Repository):

    @classmethod
    def from_URL(cls, url):
        match = findall(Github._REGEX, url)
        if match:
            return cls(match[0][0], match[0][1])
        return None

    _REGEX = r"https://github.com/([\w\.-]+)/([\w\.-]+)(?:/[\w\.-]+)*"

    
    def __init__(self, organization, project):
        self._organization = organization
        self._project = project


    @property
    def URL(self):
        return self.clone_URL
        
    @property
    def clone_URL(self):
        return  self._URL_TEMPLATE.format(self._organization, self._project)

    _URL_TEMPLATE = "https://github.com/{}/{}"

    
    @property
    def tags_URL(self):
        return self._TAGS_URL.format(self._organization,
                                    self._project)

    _TAGS_URL = "https://api.github.com/repos/{}/{}/tags"

    
    def find_tag_for(self, version_name):
        for any_tag in self._request_all_tags():
            if version_name in any_tag[self.TAG_NAME_KEY]:
                return any_tag[self.TAG_NAME_KEY]
        raise RuntimeError("Could not find a tag that match '{}'"\
                           .format(version_name))

    TAG_NAME_KEY = "name"
    
    def _request_all_tags(self):
        print("Requesting tags from Github")
        response = get(self.tags_URL)
        return response.json()



class RepositoryFactory:

    DEFAULT_PROVIDERS = [ Github ]

    
    def __init__(self, providers=None):
        self._providers = providers or self.DEFAULT_PROVIDERS

        
    def from_URL(self, url):
        for any_provider in self._providers:
            repository = any_provider.from_URL(url)
            if repository:
                return repository
        return None

        




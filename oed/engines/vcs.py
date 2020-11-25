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


from re import split



class Repository:

    @staticmethod
    def from_URL(url):
        for any_provider in PROVIDERS:
            if any_provider.complies_with(url):
                return any_provider.repository(url)
            return None

    def __init__(self, url):
        self._url = url

    def find_tag_for(self, version_name):
        url = self._url.replace("github.com/", "api.github.com/repos/") + "/tags"
        print("Hitting", url)
        response = get(url)
        for any_tag in response.json():
            if version_name in any_tag["name"]:
                return print("FOUND: ", any_tag["name"])
                return any_tag["name"]
        raise RuntimeError("Could not find a tag that match '{}'".format(version_name))

        
    @property
    def url(self):
        return self._url



class VCSProvider:

    def complies_with(self, url):
        pass

    

class Github(VCSProvider):

    def complies_with(self, url):
        return url.startswith("https://github.com")
    

    def repository(self, url):
        match = split(self.REGEX, url)
        if match:
            clean_url = self.URL_TEMPLATE.format(match[1], match[2])
            return Repository(clean_url)
            

    URL_TEMPLATE = "https://github.com/{}/{}"
    REGEX = r"https://[\w\.-]+/([\w\.-]+)/([\w\.-]+)(?:/[\w\.-]+)*"
        
        


PROVIDERS = [
    Github(),
]


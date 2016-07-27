#!/usr/bin/python
# encoding: utf-8
"""
orchard_recipe_tester.py

Specific testing module for orchard recipes

Copyright (C) University of Oxford 2016
    Ben Goodstein <ben.goodstein at it.ox.ac.uk>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from recipe_tester.recipe_tester import RecipeTester
import argparse
from os.path import split
import sys


class OrchardRecipeTester(RecipeTester):
    '''
    Tests specific to Orchard autopkg recipe standards
    '''
    def test_filename_ends_with_recipe(self):
        return self.assertTrue(self.getExt() == '.recipe')

    def test_recipe_is_loaded(self):
        return self.assertTrue(self.contents)

    def test_attribution_copyright_not_blank(self):
        return self.assertDictContains(self.contents,
                                       ['Attribution', 'Copyright'],
                                       expectedValue=self.NOTBLANK)

    def test_attribution_author_name_not_blank(self):
        return self.assertDictContains(self.contents,
                                       ['Attribution', 'Author', 'Name'],
                                       expectedValue=self.NOTBLANK)

    def test_attribution_author_email_not_blank(self):
        return self.assertDictContains(self.contents,
                                       ['Attribution', 'Author', 'Email'],
                                       expectedValue=self.NOTBLANK)

    def test_attribution_author_github_not_blank(self):
        return self.assertDictContains(self.contents,
                                       ['Attribution', 'Author', 'Github'],
                                       expectedValue=self.NOTBLANK)


class OrchardDownloadRecipeTester(OrchardRecipeTester):
        def test_recipe_has_download_extension(self):
            return self.assertTrue(self.getRecipeType() == '.download')


class OrchardMunkiRecipeTester(OrchardRecipeTester):

    def test_recipe_has_munki_extension(self):
        return self.assertTrue(self.getRecipeType() == '.munki')

    def test_input_pkginfo_category_not_blank(self):
        return self.assertDictContains(self.contents,
                                       ['Input', 'pkginfo', 'category'],
                                       expectedValue=self.NOTBLANK)

    def test_input_pkginfo_description_not_blank(self):
        return self.assertDictContains(self.contents,
                                       ['Input', 'pkginfo', 'description'],
                                       expectedValue=self.NOTBLANK)

    def test_input_pkginfo_developer_not_blank(self):
        return self.assertDictContains(self.contents,
                                       ['Input', 'pkginfo', 'developer'],
                                       expectedValue=self.NOTBLANK)

    def test_input_pkginfo_name_not_blank(self):
        return self.assertDictContains(self.contents,
                                       ['Input', 'pkginfo', 'name'],
                                       expectedValue=self.NOTBLANK)

    def test_input_pkginfo_display_name_not_blank(self):
        return self.assertDictContains(self.contents,
                                       ['Input', 'pkginfo', 'display_name'],
                                       expectedValue=self.NOTBLANK)

    def test_input_munki_repo_subdir_has_expected_value(self):
        return self.assertDictContains(self.contents,
                                       ['Input', 'MUNKI_REPO_SUBDIR'],
                                       expectedValue=r'^%NAME%$')

    def test_input_pkginfo_catalogs_has_expected_value(self):
        return self.assertDictContains(self.contents,
                                       ['Input', 'pkginfo', 'catalogs'],
                                       expectedValue=['testing'],
                                       severity='warn')

    def test_input_pkginfo_unattended_install_has_expected_value(self):
        return self.assertDictContains(self.contents,
                                       ['Input', 'pkginfo',
                                        'unattended_install'],
                                       expectedValue=True,
                                       severity='warn')


if __name__ == '__main__':
    fails = 0
    parser = argparse.ArgumentParser()
    parser.add_argument('recipe', action='append',
                        nargs='+', type=str,
                        help='at least one autopkg recipe file')
    args = parser.parse_args()
    for recipe in args.recipe[0]:
        _, recipeFile = split(recipe)
        if recipeFile.split('.')[-2] == 'munki':
            rt = OrchardMunkiRecipeTester(recipe)
        elif recipeFile.split('.')[-2] == 'download':
            rt = OrchardDownloadRecipeTester(recipe)
        else:
            rt = OrchardRecipeTester(recipe)
        rt()
        if rt._fails:
            fails += 1
    if fails:
        sys.exit(1)

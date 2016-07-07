#!/usr/bin/python
# encoding: utf-8
"""
recipe_tester.py

Module for testing autopkg recipes

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

import plistlib
import sys
import time
import argparse

DEFAULT_RECIPE = '/Users/ouit0354/Developer/recipe_checker/Github.munki.recipe'


class ResultError(Exception):
    pass


class Tester(object):

    def __init__(self):
        self._passes = []
        self._fails = []
        self._warns = []

    def __call__(self):
        self._runTests()

    def _evaluateTest(self, result, severity, msg):
        if result:
            code = 'pass'
        elif severity == 'warn':
            code = 'warn'
        else:
            code = 'fail'
        return (code, msg)

    def assertDictContains(self, aDict, keyList, notBlank=False,
                           expectedValue=None, severity="fail"):
        ''' Asserts whether keyList is present in nested aDict '''
        msg = ""
        keyFound = False
        # Could be None
        if aDict:
            for key in keyList:
                if key in aDict:
                    keyFound = True
                    if isinstance(aDict[key], dict):
                        aDict = aDict[key]
                else:
                    keyFound = False
                    msg = "Key %s not found" % keyList
            if (keyFound and expectedValue is not None and
                    aDict[keyList[-1]] != expectedValue):
                keyFound = False
                msg = "Key found but does not have expected value %s" % expectedValue
            if keyFound and notBlank and aDict[keyList[-1]] == "":
                keyFound = False
                msg = "Key found but is blank"
        return self._evaluateTest(keyFound, severity, msg)

    def assertTrue(self, expr, severity="fail"):
        result = expr
        msg = ""
        if not result:
            msg = "%s is not True" % result
        return self._evaluateTest(result, severity, msg)

    def _runTests(self, stream=sys.stdout):
        header = "=" * 70 + "\n"
        separator = "-" * 70 + "\n"
        tests = [f for f in dir(self) if f.startswith('test')]
        startTime = time.time()
        for test in tests:
            result, msg = getattr(self, test)()
            if result == 'fail':
                self._fails.append((test, msg))
                stream.write('F')
            elif result == 'warn':
                self._warns.append((test, msg))
                stream.write('W')
            elif result == 'pass':
                self._passes.append((test, msg))
                stream.write('.')
            else:
                raise ResultError('Result not recognised')
        timeTaken = time.time() - startTime
        stream.write('\n')
        if self._fails or self._warns:
            stream.write(header)
        if self._fails:
            for fail in self._fails:
                test, msg = fail
                stream.write('FAIL: %s\n-- Reason: %s\n' % (test, msg))
                stream.write(separator)
        if self._warns:
            for warn in self._warns:
                test, msg = warn
                stream.write('WARN: %s\n-- Reason: %s\n' % (test, msg))
                stream.write(separator)
        stream.write(
            "Ran %d tests in %.4f seconds.\n\n" % (len(tests), timeTaken)
        )
        if self._fails:
            stream.write('FAILED (failures=%d)\n' % len(self._fails))
        elif self._warns:
            stream.write('OK (warnings=%d)\n' % len(self._warns))
        else:
            stream.write('OK\n')


class RecipeTester(Tester):

    def __init__(self, filePath):
        super(RecipeTester, self).__init__()
        self.filePath = filePath
        try:
            self.contents = plistlib.readPlist(self.filePath)
        except Exception:
            self.contents = None

    def _runTests(self, stream=sys.stdout):
        stream.write('Testing recipe file %s:\n' % self.filePath)
        super(RecipeTester, self)._runTests()

    def test_filename_ends_with_recipe(self):
        return self.assertTrue(self.filePath.endswith('.recipe'))

    def test_recipe_is_loaded(self):
        return self.assertTrue(self.contents)

    def test_attribution_copyright_not_blank(self):
        return self.assertDictContains(self.contents,
                                       ['Attribution', 'Copyright'],
                                       notBlank=True)

    def test_attribution_author_name_not_blank(self):
        return self.assertDictContains(self.contents,
                                       ['Attribution', 'Author', 'Name'],
                                       notBlank=True)

    def test_attribution_author_email_not_blank(self):
        return self.assertDictContains(self.contents,
                                       ['Attribution', 'Author', 'Email'],
                                       notBlank=True)

    def test_attribution_author_github_not_blank(self):
        return self.assertDictContains(self.contents,
                                       ['Attribution', 'Author', 'Github'],
                                       notBlank=True)

    def test_input_pkginfo_category_not_blank(self):
        return self.assertDictContains(self.contents,
                                       ['Input', 'pkginfo', 'category'],
                                       notBlank=True)

    def test_input_pkginfo_description_not_blank(self):
        return self.assertDictContains(self.contents,
                                       ['Input', 'pkginfo', 'description'],
                                       notBlank=True)

    def test_input_pkginfo_developer_not_blank(self):
        return self.assertDictContains(self.contents,
                                       ['Input', 'pkginfo', 'developer'],
                                       notBlank=True)

    def test_input_pkginfo_name_not_blank(self):
        return self.assertDictContains(self.contents,
                                       ['Input', 'pkginfo', 'name'],
                                       notBlank=True)

    def test_input_pkginfo_display_name_not_blank(self):
        return self.assertDictContains(self.contents,
                                       ['Input', 'pkginfo', 'display_name'],
                                       notBlank=True)

    def test_input_munki_repo_subdir_has_expected_value(self):
        return self.assertDictContains(self.contents,
                                       ['Input', 'MUNKI_REPO_SUBDIR'],
                                       expectedValue="%NAME%")

    def test_input_pkginfo_catalogs_has_expected_value(self):
        return self.assertDictContains(self.contents,
                                       ['Input', 'pkginfo', 'catalogs'],
                                       expectedValue=['testing'],
                                       severity="warn")

    def test_input_pkginfo_unattended_install_has_expected_value(self):
        return self.assertDictContains(self.contents,
                                       ['Input', 'pkginfo', 'unattended_install'],
                                       expectedValue=True,
                                       severity="warn")


if __name__ == '__main__':
    fails = 0
    parser = argparse.ArgumentParser()
    parser.add_argument('recipe', action='append',
                        nargs='+', type=str,
                        help='at least one autopkg recipe file')
    args = parser.parse_args()
    for recipe in args.recipe[0]:
        rt = RecipeTester(recipe)
        rt()
        if rt._fails:
            fails += 1
    if fails:
        sys.exit(1)

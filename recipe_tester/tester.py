#!/usr/bin/python
# encoding: utf-8
"""
tester.py

Base tester module for recipe tests

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

import sys
import time
import re
import traceback

class ResultError(Exception):
    '''
    For debugging purposes
    '''
    pass


class Tester(object):
    '''
    Base Tester class that runs assertions, collates and outputs results
    '''

    # Constant for readability of code when writing tests.
    # Equals non-blank string
    NOTBLANK = r'[^()]'

    def __init__(self):
        '''
        Initialises lists for results
        '''
        self._passes = []
        self._fails = []
        self._warns = []
        self._errors = []

    def __call__(self):
        '''
        Calling Tester instance runs tests
        '''
        self._runTests()

    def _evaluateTest(self, result, severity, msg):
        '''
        Converts boolean result to pass, warn or fail
        '''
        if result:
            code = 'pass'
        elif severity == 'warn':
            code = 'warn'
        else:
            code = 'fail'
        return (code, msg)

    def _returnNestedValue(self, aDict, keyPath):
        for key in keyPath:
            if key in aDict:
                aDict = aDict[key]
            else:
                return None
        return aDict

    def _findValueInList(self, aList, keyPath, expectedValue):
        for item in aList:
            if keyPath:
                if isinstance(item, dict):
                    item = self._returnNestedValue(item, keyPath)
            else:
                if item == expectedValue:
                    return True
        return False

    # def assertDictContains(self, aDict, keyPath,
                           # expectedValue=None, severity='fail'):
        # '''
        # Asserts whether keyPath is present in (possibly nested) aDict.
        # Additionally can check if the final value matches an expectedValue
        # If this is a string, it will attempt a regex match, otherwise a
        # straight comparison will be attempted
        # '''
        # msg = ''
        # result = False
        # # Could be None
        # if aDict:
            # for key in keyPath:
                # if key in aDict:
                    # if isinstance(aDict[key], dict):
                        # aDict = aDict[key]
                    # else:
                        # result = True
                # else:
                    # msg = 'Key %s not found' % '->'.join(k for k in keyPath)

        # if result:
            # value = aDict[keyPath[-1]]
            # if expectedValue:
                # if isinstance(expectedValue, str):
                    # if not re.match(expectedValue, value):
                        # result = False
                # elif expectedValue != value:
                    # result = False
                # if not result:
                    # msg = 'Key %s found but does not match ' \
                          # 'expected value "%s"' % ('->'.join(k for k in keyPath),
                                                   # expectedValue)

        # return self._evaluateTest(result, severity, msg)

    def assertTrue(self, expr, severity='fail'):
        ''' Asserts Truth of expression '''
        result = expr
        msg = ''
        if not result:
            msg = '%s is not True' % result
        return self._evaluateTest(result, severity, msg)

    def _runTests(self, stream=sys.stdout):
        '''
        Runs all methods beginning with `test` in class. Outputs results to
        stdout
        '''
        def iter_results(results, result_type):
            for result in results:
                test, msg = result
                stream.write('%s: %s\n-- Reason: %s\n' % (result_type,
                                                          test,
                                                          msg))
                stream.write(separator)

        header = '=' * 70 + '\n'
        separator = '-' * 70 + '\n'
        tests = [f for f in dir(self) if f.startswith('test')]
        startTime = time.time()
        for test in tests:
            try:
                result, msg = getattr(self, test)()
            except Exception as e:
                tb = traceback.format_exc()
                result, msg = 'error', str(e) + '\n%s' % tb
            if result == 'fail':
                self._fails.append((test, msg))
                stream.write('F')
            elif result == 'error':
                self._errors.append((test, msg))
                stream.write('E')
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
        if self._fails or self._errors or self._warns:
            stream.write(header)

        if self._fails:
            iter_results(self._fails, "FAIL")
        if self._errors:
            iter_results(self._errors, "ERROR")
        if self._warns:
            iter_results(self._warns, "WARN")
        stream.write('Ran %d tests in %.4f seconds.\n\n' % (len(tests),
                                                            timeTaken))
        if self._fails or self._errors:
            failstr = []
            if self._fails:
                failstr.append('failures=%d' % len(self._fails))
            if self._errors:
                failstr.append('errors=%d' % len(self._errors))
            if self._warns:
                failstr.append('warnings=%d' % len(self._warns))

            stream.write('FAILED (' +
                         ', '.join([item for item in failstr]) +
                         ')\n')
        elif self._warns:
            stream.write('OK (warnings=%d)\n' % len(self._warns))
        else:
            stream.write('OK\n')

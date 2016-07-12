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
# Debug

class ResultError(Exception):
    pass


class Tester(object):
    '''
    Base Tester class that runs assertions, collates and outputs results
    '''

    # Constant for readability of code when writing tests.
    # Equals non-blank string
    NOTBLANK = r'[^()]'

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

    def assertDictContains(self, aDict, keyPath,
                           expectedValue=None, severity='fail'):
        '''
        Asserts whether keyPath is present in (possibly nested) aDict.
        Additionally can check if the final value matches an expectedValue
        If this is a string, it will attempt a regex match, otherwise a straight
        comparison will be attempted
        '''
        msg = ''
        result = False
        # Could be None
        if aDict:
            for key in keyPath:
                if key in aDict:
                    if isinstance(aDict[key], dict):
                        aDict = aDict[key]
                    else:
                        result = True
                else:
                    msg = 'Key %s not found' % keyPath

        if result:
            value = aDict[keyPath[-1]]
            if expectedValue:
                if isinstance(expectedValue, str):
                    if not re.match(expectedValue, value):
                        result = False
                elif expectedValue != value:
                    result = False
                if not result:
                    msg = 'Key found but does not match expected value %s' % expectedValue

        return self._evaluateTest(result, severity, msg)

    def assertTrue(self, expr, severity='fail'):
        ''' Asserts Truth of expression '''
        result = expr
        msg = ''
        if not result:
            msg = '%s is not True' % result
        return self._evaluateTest(result, severity, msg)

    def _runTests(self, stream=sys.stdout):
        header = '=' * 70 + '\n'
        separator = '-' * 70 + '\n'
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
        stream.write('Ran %d tests in %.4f seconds.\n\n' % (len(tests),
                                                            timeTaken))
        if self._fails:
            stream.write('FAILED (failures=%d)\n' % len(self._fails))
        elif self._warns:
            stream.write('OK (warnings=%d)\n' % len(self._warns))
        else:
            stream.write('OK\n')



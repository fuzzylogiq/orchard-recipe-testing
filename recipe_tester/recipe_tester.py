#!/usr/bin/python
# encoding: utf-8
'''
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
'''
from tester import Tester
import plistlib
import sys
from os.path import splitext


class RecipeTester(Tester):
    '''
    Extends Tester Class with methods for AutoPkg recipes
    '''

    def __init__(self, filePath):
        '''
        Adds further initialisation specific to Autopkg recipes
        '''
        super(RecipeTester, self).__init__()
        self.filePath = filePath
        self.contents = dict()
        try:
            with open(self.filePath, 'rb') as f:
                self.contents = plistlib.readPlist(f)
        except Exception:
            pass

    def _runTests(self, stream=sys.stdout):
        '''
        Adds further configuration for Autopkg recipes
        '''
        stream.write('Testing recipe file %s:\n' % self.filePath)
        super(RecipeTester, self)._runTests()

    def getExt(self):
        '''
        Returns a file extension from a path
        '''
        _, ext = splitext(self.filePath)
        return ext

    def getRecipeType(self):
        '''
        Returns a recipe type from a path (e.g. `.munki` or `.pkg`)
        '''
        fileName, _ = splitext(self.filePath)
        _, recipeType = splitext(fileName)
        return recipeType

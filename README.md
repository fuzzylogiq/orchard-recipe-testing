# orchard-recipe-testing
Tests to run on recipes submitted to Orchard's (University of Oxford IT Services Apple management programme) AutoPkg repos

This is an early alpha attempt to create an extensible python framework to test [AutoPkg](https://github.com/autopkg/autopkg) recipes.

To use, import the RecipeTester class:
```
from recipe_tester.recipe_tester import RecipeTester
```

Write a testing class that subclasses it:
```
class MyAmazingRecipeTester(RecipeTester):
```

Any methods in that class that start with 'test_' will be run when the class or an instance is __call__ed:
```
def test_something_i_expect_to_be_true_is_true(self):
  someCondition == True
  return assertTrue(someCondition)
```

Assertions tested will result in a fail if not passed unless you set the severity kwarg to 'warn':
```
def test_input_contains_name(self):
  return assertDictContains(self.contents, ['Input', 'name'], severity='warn')
```

To use in a python module:
```
recipeFile = '/Users/somebody/Library/AutoPkg/Recipes/Foo/Foo.download.recipe'
rt = MyAmazingRecipeTester(recipeFile)
rt()
```

See the orchard_recipe_tester.py file for an example of how we are using it locally to test recipes on the command line (and in Travis CI)

TODO:

- Add main() to recipe_tester module so it can be used and extended in scripts that use the module.
- Clean up assertion code and write some more useful assertions for AutoPkg recipes
- Improve this README

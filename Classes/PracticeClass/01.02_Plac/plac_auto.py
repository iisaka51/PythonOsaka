import plac
import plac_annotation

tests = [
  ['add', '1', '2'],
  ['mul', '2', '3'],
]
for testcase in tests:
    x = plac.call(plac_annotation.main, testcase)
    print(f'testcase: {testcase}, result:{x}')

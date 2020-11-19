import re

solutions= [
   ['EX1', r'[^a-zA-Z0-9\S]', 'Reject'],
   ['EX2', r'ab*', 'Accept'],
   ['EX3', r'ab+', 'Accept'],
   ['EX4', r'ab{3}', 'Accept'],
   ['EX5', r'ab{2,3}', 'Accept'],
   ['EX6', r'a.*?b$', 'Accept'],
   ['EX7', r'\w*z.\w*', 'Accept'],
   ['EX8', r'\S[^t]+t[^t]*\S', 'Accept'],
   ['EX8', r'\Bt\B', 'Accept'],
   ['EX9', r'(P\w+)\W(P\w+)', 'Accept'],
   ['EX10', r'(0[0-9]{1}|1{1}[0-9]{1}|2{1}[0-3]{1}):(0[0-9]{1}|[1-5]{1}[0-9]{1}):(0[0-9]{1}|[1-5]{1}[0-9]{1})$', 'Accept'],
]

tests = [
  ['test01', 'a'],
  ['test02', 'aa'],
  ['test03', 'aab'],
  ['test04', 'aabb'],
  ['test05', 'abc'],
  ['test06', 'abcabc'],
  ['test07', 'abbabbabb'],
  ['test08', 'abbbabbabbb'],
  ['test09', 'abbbabbabbb'],
  ['test10', 'Python PostgreSQL'],
  ['test11', 'Porker and Zork'],
  ['test12', 'I like zope.'],
  ['test13', 'thank you.'],
  ['test14', r'Big Think!'],
  ['test15', 'I was absent from school.'],
  ['test16', 'The work is near completion.'],
  ['test17', '01:02:03'],
  ['test18', '23:23:23'],
  ['test19', '25:00:00'],
  ['test20', '1:2:3']
]


def exercise(testcase, text, pattern, flag='Accept'):
    result={
        'Accept':['Accept', 'Reject'],
        'Reject':['Reject', 'Accept']
    }
    if re.search(pattern,  text):
        return result[flag][0]
    else:
        return result[flag][1]

if __name__ == '__main__':
    import plac
    for id, pattern, flag in solutions:
        print(f'--{id}:"{pattern}" -----')
        for testcase in tests:
            arg = testcase + [pattern, flag]
            x = plac.call(exercise, arg)
            print(f'testcase: {testcase[1:2]}, result: {x}')

import argparse

parser = argparse.ArgumentParser(description ='Search some files')
# nargs 引数の数を指定
# nargs='*': ０もしくはそれ以上  nargs='+': １もしくはそれ以上
parser.add_argument(dest ='filenames', metavar ='filename', nargs ='*')
parser.add_argument('-p', '--pat', metavar ='pattern',
                    required = True, dest ='patterns',
                    action ='append',
                    help ='text pattern to search for')
parser.add_argument('-v', dest ='verbose',
                    action ='store_true', help ='verbose mode')
parser.add_argument('-o', dest ='outfile',
                    action ='store', help ='output file')
parser.add_argument('--overwrite', dest ='overwrite',
                    action ='store', choices = {'yes', 'no'},
                    default ='no', help ='Overwrite if file existing')
args = parser.parse_args()

print(args)

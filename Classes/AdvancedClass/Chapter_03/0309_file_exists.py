import os
filepath = input('Input Filepath: ? ')
print(f'Directory Separator: {os.sep}')
if os.path.exists(filepath): # filepath が存在していれば真
    print(f'{filepath} exist.')
	if os.path.isfile(filepath): # filepath がファイルなら真
    	print(f'{filepath} is FILE')
	elif os.path.isdir(filepath): # filepath がディレクトリなら真
    	print(f'{filepath} is DIRECTORY')
else:
    print(f'No such file or directory: {filepath}')

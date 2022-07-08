def print_answer_file():
    with open('answer.txt','r') as f:
         print('the answer is',  f.read())
 
with open('answer.txt','w') as f:
    f.write('42')
    f.close()
 
print_answer_file()

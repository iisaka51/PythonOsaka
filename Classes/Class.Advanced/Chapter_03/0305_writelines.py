data = """“A wise man changes his mind sometimes, but a fool never.
To change your mind is the best evidence you have one.”
― Desmond Ford
"""

lines = data.split('\n')
f = open('new_data.txt', 'w')
f.writelines(data)
f.close()

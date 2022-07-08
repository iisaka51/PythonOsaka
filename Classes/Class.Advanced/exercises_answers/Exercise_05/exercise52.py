class StrKeeper():
    def __init__(self):
        self.strlist = []

    def getString(self,prompt='Input : '):
        self.strlist.append(input(prompt))
        return self.strlist[-1]

    def capString(self):
        return [ s.upper() for s in self.strlist]

if __name__ == '__main__':
    s = StrKeeper()
    ss = s.getString('Input Str :')
    print(ss)
    s.getString('Input Str :')
    print(s.capString())

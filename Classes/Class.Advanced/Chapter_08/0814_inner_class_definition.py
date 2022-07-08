class Outer:
    def __init__(self):
        self.inner = self.Inner()
        self.innerinner = self.inner.InnerInner()

    def myprint(self):
        print("This is Outer class")

    class Inner:
        def __init__(self):
            self.innerinner = self.InnerInner()

        def myprint(self):
            print("This is Inner class")

        class InnerInner:
            def inner_myprint(self, msg):
                print("This is multilevel InnerInner class")
                print(msg)

        # インデントに注目
        def inner_myprint(self, msg):
            print("This is Inner class")
            print(msg)

outer = Outer()
outer.myprint()
inner = outer.Inner()
inner.myprint()
innerinner = inner.InnerInner()
innerinner.inner_myprint("Hello!")

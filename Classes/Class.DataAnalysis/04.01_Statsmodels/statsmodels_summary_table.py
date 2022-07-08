from statsmodels.iolib.table import SimpleTable
mydata = [[11,12],[21,22]]  # data MUST be 2-dimensional
myheaders = [ "Column 1", "Column 2" ]
mystubs = [ "Row 1", "Row 2" ]
tbl = SimpleTable(mydata, myheaders, mystubs, title="Title")
print( tbl )

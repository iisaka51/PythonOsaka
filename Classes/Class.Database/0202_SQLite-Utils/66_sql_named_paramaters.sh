sqlite-utils query my_data2.db \
    "select * from creatures where species = :species;" \
    -p species chicken

sqlite-utils query my_data2.db "update creatures set name = :name where id=6;" -p name blue

sqlite-utils rows my_data2.db creatures

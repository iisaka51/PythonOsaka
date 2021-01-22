all_users = session.query(User.name.label('name_label')).all()
for row in all_users:
   print(row.name_label)

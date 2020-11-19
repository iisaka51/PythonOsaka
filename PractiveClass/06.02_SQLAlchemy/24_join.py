for u, a in session.query(User, Address).\
              filter(User.id==Address.user_id).\
              filter(Address.email_address=='jack@google.com').\
              all():
     print(u)
     print(a)

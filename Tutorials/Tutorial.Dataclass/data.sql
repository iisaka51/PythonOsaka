CREATE TABLE IF NOT EXISTS "User" (
"id" INTEGER,
  "name" TEXT,
  "part" TEXT,
  "email" TEXT
);
CREATE INDEX "ix_User_id"ON "User" ("id");

INSERT INTO User(id,name,part,email)
       VALUES (1,"Freddie","Vocal","freddie@example.com");
INSERT INTO User(id,name,part,email)
       VALUES (2,"Brian","Guitar","brian@example.com");
INSERT INTO User(id,name,part,email)
       VALUES (3,"John","Base","john@example.com");
INSERT INTO User(id,name,part,email)
       VALUES (4,"Roger","Drums","rogger@example.com");
INSERT INTO User(id,name,part,email)
       VALUES (5,"Adam","Vocal","adm@example.com");
INSERT INTO User(id,name,part,email)
       VALUES (6,"David","Guitar","david@example.com");
INSERT INTO User(id,name,part,email)
       VALUES (7,"Carlos","Guitar","carlos@example.com");
INSERT INTO User(id,name,part,email)
       VALUES (8,"Paul","Base","paul@example.com");
INSERT INTO User(id,name,part,email)
       VALUES (9,"Ian","Drums","ian@example.com");
INSERT INTO User(id,name,part,email)
       VALUES (10,"nick","Base","nick@example.com");

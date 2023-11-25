BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "users" (
	"id"	VARCHAR(32) NOT NULL,
	"email"	VARCHAR(345),
	"password"	TEXT NOT NULL,
	"username"	VARCHAR(50) NOT NULL,
	"first_name"	VARCHAR(50) NOT NULL,
	"last_name"	VARCHAR(50) NOT NULL,
	"phone_number"	VARCHAR(15),
	"isconnected"	BOOLEAN,
	PRIMARY KEY("id"),
	UNIQUE("username"),
	UNIQUE("id"),
	UNIQUE("email")
);
CREATE TABLE IF NOT EXISTS "comments" (
	"id"	VARCHAR(32) NOT NULL,
	"comment_text"	VARCHAR(345) NOT NULL,
	"note"	INTEGER,
	"user_id"	VARCHAR(32) NOT NULL,
	"film_id"	VARCHAR(32) NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("user_id") REFERENCES "users"("id")
);
CREATE TABLE IF NOT EXISTS "alembic_version" (
	"version_num"	VARCHAR(32) NOT NULL,
	CONSTRAINT "alembic_version_pkc" PRIMARY KEY("version_num")
);
INSERT INTO "users" VALUES ('3a35f0e481da48e0a7ec7d43b8db5a3d','saadimounalisa@gmail.com','$2b$12$OD14K8TqKDFyfvQhpb9H0.AObLpwrWD2EuBuaYM7upd/tz7cFZwy.','saadimouna','mouna lisa','saadi','0749103751',0);
INSERT INTO "users" VALUES ('c4d54a530a464cc5ac968b032b9960db','saadimonagmail.com','$2b$12$OUPqPcobAfXLD.Q89XCwkO3bxJdbz0PGj4uuzdeqTqprh/Ef5VoeC','monalisa','mona lisa','saadi','0749103751',1);
INSERT INTO "users" VALUES ('e334140a4c8c402cbe84c6a54a8b4daf','saadimonlisagmail.com','$2b$12$RMKKajO1yUsku/w8aSwrXOZb/8vhps3fGuma9MA1aQ0ibL0u6PBd6','monalisasdi','mona lisa','saadi','0749103751',1);
INSERT INTO "users" VALUES ('00c374155d8c43d485b651e099e63ad5','saadimonaalisagmail.com','$2b$12$WIgy.YGrFQdgBT49b8qnBOVuPkBbI/LOPJwqvNa/JdurDq5j9MG7e','monalisasddi','mona lisa','saadi','0749103751',1);
INSERT INTO "users" VALUES ('dc56cc05cd474b8d8f5713d3327470d8','lea@gmail.com','$2b$12$SMylkmkoxVjHHq8cjktjMe2qSqbNUfMmkFBpiEVl.wmcGVO4kKiQy','lele','Dornat','Léa','0627000000',1);
INSERT INTO "users" VALUES ('619c1087bf814f71b8c7d48c0ccbf53b','LDO@g.com','$2b$12$/B7m5LZSIpr3Fpy0z01J6uW7wWhW7gXbgtd0NwkVzGgNHInQVHFKa','LDO','Dornat','LDO','000000000000',1);
INSERT INTO "users" VALUES ('389e30264137486e9c3c7d0991e8ca9d','mona@gmail.com','$2b$12$s0cZMZEGjdw8tumFlsneQOLRLl728yl0r6oOzMmX3zdnw6ynRwqMG','mona','Mouna lisa','Saadi','0749103751',1);
INSERT INTO "comments" VALUES ('619c1087bf814f71b8c7d48c0ccbf53b872585','juh',0,'619c1087bf814f71b8c7d48c0ccbf53b','872585');
COMMIT;

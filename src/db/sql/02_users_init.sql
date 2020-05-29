CREATE TABLE "users" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "username" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "permission_lvl" INTEGER NOT NULL,
    "book_limit" INTEGER
);

INSERT INTO "users" VALUES
    (NULL, "admin", "admin@flibre.com", "pbkdf2:sha256:150000$dbbH91gl$13289330287439b69c5453491968ee57fd1647c8c6baeb523243cc4431607d7a", 1, 0),
    (NULL, "user", "user@flibre.com", "pbkdf2:sha256:150000$bKxg0PMB$c2efeb31e6a56458fd85f0221d2a72f3cabad19bc794cc98d43ed9e5e3ba58d2", 2, 5),

CREATE TABLE "books" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "author" TEXT NOT NULL,
    "description" TEXT,
    "isbn" INTEGER,
    "pages" INTEGER,
    "published" TEXT,
    "publisher" TEXT,
    "subtitle" TEXT,
    "title" TEXT NOT NULL,
    "website" TEXT
);

CREATE TABLE "users" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "username" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "permission_lvl" INTEGER NOT NULL
);

CREATE TABLE "users_to_books" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "user_id" INTEGER,
    "book_id" INTEGER,
    "borrow_date" TEXT,
    FOREIGN KEY ("user_id") REFERENCES "users" ("id"),
    FOREIGN KEY ("book_id") REFERENCES "books" ("id")
);

INSERT INTO "users" VALUES
    (NULL, "admin", "admin@flibre.com", "admin", 1),
    (NULL, "user", "user@flibre.com", "user", 2),
    (NULL, "guest", "guest@flibre.com", "guest", 3);

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
    "website" TEXT,
    "user_id" INTEGER,
    FOREIGN KEY ("user_id") REFERENCES "users" ("id")
);

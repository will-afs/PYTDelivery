DROP TABLE IF EXISTS pdf;

CREATE TABLE pdf (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  file_uri TEXT UNIQUE NOT NULL,
  metadata TEXT DEFAULT '',
  content TEXT DEFAULT ''
);
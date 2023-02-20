CREATE TABLE users (
id INTEGER PRIMARY KEY,
email TEXT NOT NULL,
password TEXT NOT NULL
);

CREATE TABLE queue (
user_id INTEGER,
data TEXT NOT NULL,
FOREIGN KEY (user_id) REFERENCES users(id)
);
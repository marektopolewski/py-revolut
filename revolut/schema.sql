DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS transactions;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    balance REAL NOT NULL DEFAULT 0.0
);

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_from INTEGER NOT NULL,
    user_to INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    amount REAL NOT NULL,
    pending INTEGER NOT NULL DEFAULT FALSE,
    FOREIGN KEY (user_from) REFERENCES users (id),
    FOREIGN KEY (user_to) REFERENCES users (id)
);


-- STUB DATA
INSERT INTO users (name, username, email, balance)
    VALUES ('Marek Topol', 'mtopol', 'm.t@gmail.com', 20.0);
INSERT INTO users (name, username, email, balance)
    VALUES ('Kamil Topol', 'ktopol', 'k.t@gmail.com', 100.0);

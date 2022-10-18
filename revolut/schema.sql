DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS transactions;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
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
INSERT INTO users (name, username, email, balance, password)
    VALUES ('Marek Topol', 'mtopol', 'm.t@gmail.com', 20.0, 'pbkdf2:sha256:260000$Dgj2Sa6nNv9J1uQH$07e45c3a7bb93099f7868dfe734b2f990d00675fc88de147f6b13f665158ad73');
INSERT INTO users (name, username, email, balance, password)
    VALUES ('Kamil Topol', 'ktopol', 'k.t@gmail.com', 100.0, 'pbkdf2:sha256:260000$Dgj2Sa6nNv9J1uQH$07e45c3a7bb93099f7868dfe734b2f990d00675fc88de147f6b13f665158ad73');

CREATE TABLE bets
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATETIME,
    sport int,
    competition VARCHAR(80),
    region VARCHAR(80),
    player1 VARCHAR(150),
    player2 VARCHAR(150),
    pick VARCHAR(150),
    bookie VARCHAR(50),
    market VARCHAR(50),
    tipster VARCHAR(50),
    stake FLOAT,
    one FLOAT,
    result VARCHAR(1),
    profit FLOAT,
    bet FLOAT,
    quota FLOAT
);

CREATE TABLE sports
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50)
);

INSERT INTO sports (name) VALUES ('Fútbol');
INSERT INTO sports (name) VALUES ('Baloncesto');
INSERT INTO sports (name) VALUES ('Balonmano');
INSERT INTO sports (name) VALUES ('Béisbol');
INSERT INTO sports (name) VALUES ('Boxeo');
INSERT INTO sports (name) VALUES ('Críquet');
INSERT INTO sports (name) VALUES ('Fútbol Americano');
INSERT INTO sports (name) VALUES ('Golf');
INSERT INTO sports (name) VALUES ('Tenis');
INSERT INTO sports (name) VALUES ('Tenis de mesa');
INSERT INTO sports (name) VALUES ('Voleibol');

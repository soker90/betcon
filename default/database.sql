CREATE TABLE bet
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATETIME,
    sport INTEGER,
    competition VARCHAR(80),
    region INTEGER,
    player1 VARCHAR(150),
    player2 VARCHAR(150),
    pick VARCHAR(150),
    bookie VARCHAR(50),
    market VARCHAR(50),
    tipster VARCHAR(50),
    stake REAL,
    one REAL,
    result VARCHAR(1),
    profit REAL,
    bet REAL,
    quota FLOAT
);

CREATE TABLE sport
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50)
);

INSERT INTO sport (id, name) VALUES (1, '');
INSERT INTO sport (name) VALUES ('Baloncesto');
INSERT INTO sport (name) VALUES ('Balonmano');
INSERT INTO sport (name) VALUES ('Béisbol');
INSERT INTO sport (name) VALUES ('Boxeo');
INSERT INTO sport (name) VALUES ('Críquet');
INSERT INTO sport (name) VALUES ('Fútbol');
INSERT INTO sport (name) VALUES ('Fútbol Americano');
INSERT INTO sport (name) VALUES ('Golf');
INSERT INTO sport (name) VALUES ('Tenis');
INSERT INTO sport (name) VALUES ('Tenis de mesa');
INSERT INTO sport (name) VALUES ('Voleibol');



CREATE TABLE region
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50)
);

INSERT INTO region (id,name) VALUES (1,'');

CREATE TABLE competition
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(80),
    region INT,
    sport INT
);

INSERT INTO competition (id, name, region, sport) VALUES (1, '', 1, 1);

CREATE TABLE bookie
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL
);
CREATE UNIQUE INDEX bookie_name_uindex ON bookie (name);

INSERT INTO bookie(name) VALUES ('Bet365');
INSERT INTO bookie(name) VALUES ('Betfair');
INSERT INTO bookie(name) VALUES ('Sportium');
INSERT INTO bookie(name) VALUES ('Bwin');
INSERT INTO bookie(name) VALUES ('888sport');
INSERT INTO bookie(name) VALUES ('William Hill');
INSERT INTO bookie(name) VALUES ('Luckia');


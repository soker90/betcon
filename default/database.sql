CREATE TABLE bet
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATETIME,
    sport INTEGER,
    competition INTEGER,
    region INTEGER,
    player1 VARCHAR(150),
    player2 VARCHAR(150),
    pick VARCHAR(150),
    bookie INTEGER,
    market INTEGER,
    tipster INTEGER,
    stake REAL,
    one REAL,
    result VARCHAR(50),
    profit REAL,
    bet REAL,
    quota REAL
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
INSERT INTO competition (id, name, region, sport) VALUES (2, '', 1, 2);
INSERT INTO competition (id, name, region, sport) VALUES (3, '', 1, 3);
INSERT INTO competition (id, name, region, sport) VALUES (4, '', 1, 4);
INSERT INTO competition (id, name, region, sport) VALUES (5, '', 1, 5);
INSERT INTO competition (id, name, region, sport) VALUES (6, '', 1, 6);
INSERT INTO competition (id, name, region, sport) VALUES (7, '', 1, 7);
INSERT INTO competition (id, name, region, sport) VALUES (8, '', 1, 8);
INSERT INTO competition (id, name, region, sport) VALUES (9, '', 1, 9);
INSERT INTO competition (id, name, region, sport) VALUES (10, '', 1, 10);
INSERT INTO competition (id, name, region, sport) VALUES (11, '', 1, 11);
INSERT INTO competition (id, name, region, sport) VALUES (12, '', 1, 12);

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

CREATE  TABLE market
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(80) NOT NULL
);

INSERT INTO market(name) VALUES ('Hándicap Asiático');
INSERT INTO market(name) VALUES ('Combinada');
INSERT INTO market(name) VALUES ('Córners');
INSERT INTO market(name) VALUES ('Descanso/Final');
INSERT INTO market(name) VALUES ('Doble oportunidad');
INSERT INTO market(name) VALUES ('Empate no válido');
INSERT INTO market(name) VALUES ('Especiales');
INSERT INTO market(name) VALUES ('Goles');
INSERT INTO market(name) VALUES ('Hándicap Europeo');
INSERT INTO market(name) VALUES ('Marcador exacto');
INSERT INTO market(name) VALUES ('Over/Under');
INSERT INTO market(name) VALUES ('Resultado Final');
INSERT INTO market(name) VALUES ('Tarjetas');

CREATE TABLE tipster
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50)
);

INSERT INTO tipster(name) VALUES ('');

CREATE TABLE bank
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(30),
    bank REAL
);

INSERT INTO bank (id, name, bank) VALUES (1, 'Banco', 0.0);
INSERT INTO bank (id, name, bank) VALUES (2, 'Paypal', 0.0);
INSERT INTO bank (id, name, bank) VALUES (3, 'Skrill', 0.0);

CREATE TABLE movement
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE,
    account INTEGER,
    bookie INTEGER,
    money REAL
);

CREATE TABLE bonus
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE,
    bookie INTEGER,
    money REAL,
    free BOOLEAN
);

create table tipster_month
(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	month INTEGER,
	year INTEGER,
	tipster INTEGER,
	money REAL
);


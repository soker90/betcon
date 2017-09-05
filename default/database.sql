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
    quota REAL,
    free BOOLEAN
);


CREATE TABLE sport
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50)
);

INSERT INTO sport (id, name) VALUES (1, '');
INSERT INTO sport (id, name) VALUES (2, 'Baloncesto');
INSERT INTO sport (id, name) VALUES (3, 'Balonmano');
INSERT INTO sport (id, name) VALUES (4, 'Béisbol');
INSERT INTO sport (id, name) VALUES (5, 'Boxeo');
INSERT INTO sport (id, name) VALUES (6, 'Críquet');
INSERT INTO sport (id, name) VALUES (7, 'Fútbol');
INSERT INTO sport (id, name) VALUES (8, 'Fútbol Americano');
INSERT INTO sport (id, name) VALUES (9, 'Futbol Sala');
INSERT INTO sport (id, name) VALUES (10, 'Golf');
INSERT INTO sport (id, name) VALUES (11, 'Hockey');
INSERT INTO sport (id, name) VALUES (12, 'Hockey sobre hielo');
INSERT INTO sport (id, name) VALUES (13, 'Rugby');
INSERT INTO sport (id, name) VALUES (14, 'Squash');
INSERT INTO sport (id, name) VALUES (15, 'Tenis');
INSERT INTO sport (id, name) VALUES (16, 'Tenis de mesa');
INSERT INTO sport (id, name) VALUES (17, 'Voleibol');
INSERT INTO sport (id, name) VALUES (18, 'Voley playa');
INSERT INTO sport (id, name) VALUES (19, 'Caballos');
INSERT INTO sport (id, name) VALUES (20, 'E-Sports');


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
INSERT INTO competition (id, name, region, sport) VALUES (13, '', 1, 13);
INSERT INTO competition (id, name, region, sport) VALUES (14, '', 1, 14);
INSERT INTO competition (id, name, region, sport) VALUES (15, '', 1, 15);
INSERT INTO competition (id, name, region, sport) VALUES (16, '', 1, 16);
INSERT INTO competition (id, name, region, sport) VALUES (17, '', 1, 17);
INSERT INTO competition (id, name, region, sport) VALUES (18, '', 1, 18);
INSERT INTO competition (id, name, region, sport) VALUES (19, '', 1, 19);
INSERT INTO competition (id, name, region, sport) VALUES (20, '', 1, 20);

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
INSERT INTO bookie(name) VALUES ('Marca Apuestas');
INSERT INTO bookie(name) VALUES ('Paf');
INSERT INTO bookie(name) VALUES ('Interwetten');
INSERT INTO bookie(name) VALUES ('Wanabet');
INSERT INTO bookie(name) VALUES ('Codere');
INSERT INTO bookie(name) VALUES ('Suertia');
INSERT INTO bookie(name) VALUES ('Circus');

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

create table conjunta
(
	id INTEGER
		primary key
		 autoincrement,
	name VARCHAR(30),
	month INTEGER,
	year INTEGER,
	money REAL
);

create table conjunta_tipster
(
	conjunta INTEGER,
	tipster INTEGER,
	constraint conjunta_tipster_conjunta_tipster_pk
		primary key (conjunta, tipster)
);

create table combined
(
	id INTEGER primary key autoincrement,
  bet INTEGER,
	date DATETIME,
	sport INTEGER,
	competition INTEGER,
	region INTEGER,
	player1 VARCHAR(150),
	player2 VARCHAR(150),
	pick VARCHAR(150),
	result VARCHAR(50)
);

create table variable
(
	key VARCHAR(20) primary key,
	value VARCHAR(100)
);

INSERT INTO bank VALUES ('version', '1.6');
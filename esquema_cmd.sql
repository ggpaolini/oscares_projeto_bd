create table FILM
(
  FilmId TEXT,
  FilmName TEXT, 
  PRIMARY KEY(FilmId, FilmName)
);

create table NOMINATION
(
  NomId TEXT ,
  ClassName TEXT,
  CeremonyNumber INTEGER,
  CategoryName TEXT,
  NominationName TEXT,
  Winner TEXT,
  Detail TEXT,
  Note TEXT,
  Citation TEXT,
  PRIMARY KEY (NomId),
  foreign key (ClassName, CategoryName) references CATEGORY(ClassName, CategoryName),
  foreign key (CeremonyNumber) references CEREMONY(CeremonyNumber)
);

 create table CEREMONY
(
  CeremonyNumber INTEGER PRIMARY KEY,
  Year TEXT
);

create table CLASS
(
  ClassName TEXT PRIMARY KEY
);

create table NOMINEE
(
  NomineeId TEXT PRIMARY KEY,
  Name TEXT
);

create table CATEGORY
(
  ClassName TEXT,
  CategoryName TEXT,
  CanonicalCategory,
  primary key (ClassName, CategoryName),
  FOREIGN KEY(ClassName) REFERENCES CLASS(ClassName)
);

create table NOMINATION_FILM
(
  NomId TEXT,
  FilmId TEXT,
  FilmName TEXT,
  PRIMARY KEY(NomId, FilmId, FilmName),
  FOREIGN KEY(NomId)
    REFERENCES NOMINATION(NomId),
  FOREIGN KEY(FilmId, FilmName) references FILM(FilmId, FilmName)
);

create table NOMINATION_NOMINEE
(
  NomId TEXT,
  NomineeId TEXT,
  PRIMARY KEY(NomId, NomineeId),
  FOREIGN KEY(NomId)
    REFERENCES NOMINATION(NomId),
  FOREIGN KEY(NomineeId) references NOMINEE(NomineeId)
);
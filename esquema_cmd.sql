create table FILM
(
  FilmId TEXT,
  FilmName TEXT, 
  PRIMARY KEY(FilmId, FilmName)
);

create table NOMINATION
(
  ClassName TEXT,
  NomId TEXT,
  CeremonyNumber INTEGER,
  CanonicalCategory TEXT,
  NominationName TEXT,
  Winner TEXT,
  Detail TEXT,
  Note TEXT,
  Citation TEXT,
  primary key (ClassName, NomId, CeremonyNumber, CanonicalCategory),
  foreign key (ClassName, CanonicalCategory) references CATEGORY(ClassName, CanonicalCategory),
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
  CanonicalCategory TEXT,
  CategoryName TEXT,
  primary key (ClassName, CanonicalCategory),
  FOREIGN KEY(ClassName) REFERENCES CLASS(ClassName)
);

create table NOMINATION_FILM
(
  ClassName TEXT,
  CanonicalCategory TEXT,
  CeremonyNumber INTEGER,
  NomId TEXT,
  FilmId TEXT,
  FilmName TEXT,
  PRIMARY KEY(ClassName, NomId, CeremonyNumber, CanonicalCategory, FilmId, FilmName),
  FOREIGN KEY(ClassName, NomId, CeremonyNumber, CanonicalCategory)
    REFERENCES NOMINATION(ClassName, NomId, CeremonyNumber, CanonicalCategory),
  FOREIGN KEY(FilmId, FilmName) references FILM(FilmId, FilmName)
);

create table NOMINATION_NOMINEE
(
  ClassName TEXT,
  CanonicalCategory TEXT,
  CeremonyNumber INTEGER,
  NomId TEXT,
  NomineeId TEXT,
  PRIMARY KEY(ClassName, NomId, CeremonyNumber, CanonicalCategory, NomineeId),
  FOREIGN KEY(ClassName, NomId, CeremonyNumber, CanonicalCategory)
    REFERENCES NOMINATION(ClassName, NomId, CeremonyNumber, CanonicalCategory),
  FOREIGN KEY(NomineeId) references NOMINEE(NomineeId)
);

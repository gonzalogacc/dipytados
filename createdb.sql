
CREATE TABLE sesiones (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  url       TEXT,
  periodo   INT,
  reunion    INT,
  n         INT,
  fecha     DATE,
  status    TEXT,
  descripcion TEXT,
  html_text BLOB,
  proc_status TEXT
);

CREATE TABLE diputado (
  id      INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre  TEXT,
  FOREIGN KEY(id) REFERENCES sesiones(id)
);

CREATE TABLE intervencion (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  sesion    INT,
  diputado  INT,
  texto     TEXT,
  FOREIGN KEY(sesion) REFERENCES sesiones(id),
  FOREIGN KEY(diputado) REFERENCES diputado(id)
);

CREATE TABLE proyecto_ley (
  id      INTEGER PRIMARY KEY AUTOINCREMENT,
  sesion  INT,
  numero  TEXT,
  texto   TEXT,
  FOREIGN KEY (id) REFERENCES sesiones(id)
);

CREATE TABLE voto (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  proyecto_ley INT,
  sesion       INT,
  diputado     INT,
  voto         TEXT,
  FOREIGN KEY (proyecto_ley) REFERENCES proyecto_ley(id),
  FOREIGN KEY (sesion) REFERENCES sesion(id),
  FOREIGN KEY (diputado) REFERENCES diputado(id)
);
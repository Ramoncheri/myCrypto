CREATE TABLE "resumen" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"Fecha"	TEXT,
	"de_cripto"	TEXT NOT NULL,
	"volumen"	INTEGER NOT NULL,
	"a_cripto"	TEXT NOT NULL,
	"cotizacion"	INTEGER NOT NULL,
	"importe"	INTEGER NOT NULL
)
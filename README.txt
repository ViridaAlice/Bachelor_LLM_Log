Erstellt im Rahmen der Bachelorarbeit "Large Language Modelle zur Logdaten-Analyse und Angriffserkennung"
der Rheinischen Friedrich-Wilhelms-Universität Bonn von Elisabeth Alice Rahn (s27erahn@uni-bonn.de).
Dieser Datensatz basiert auf Daten aus dem "AIT Log Dataset V2.0" (https://zenodo.org/records/5789064).

Layout:
/[sysname]: 
	-> attacks.log : Alle Angriffe, die auf das System während Runtime getätigt wurden
/[sysname]/gather/:
	-> label_[logname] : Groundtruth der entsprechenden Log-Datei aller verdächtigen Zeilen
/[sysname]/gather/ganze_dateien: 
	-> /true_pos/: Originale Log-Dateien
	-> /true_neg/: Log-Dateien, gekürzt um Zeilen, die Angriffe verzeichnen
/[sysname]/gather/ausschnitte:
	-> /true_pos/: Ausschnitte der Länge [LogAusschnittLaenge] (siehe unten), 
		       mit aber nicht ausschließlich verdächtigen Zeilen des Groundtruth
	-> /true_neg/: Ausschnitte der Länge [LogAusschnittLaenge] oder kürzer,
		       ohne jegliche verdächtige Zeilen

[sysname]: Der Datensatz besteht aus 8 Systemen: 
	   "fox", "harrison", "russellmitchell", "santos", "shaw", "wardbeck", "wheeler", "wilson"
[logname]: Jeder Datensatz besitzt 7 verschiedene Log-Typen:
	   "dnsmasq.log", "audit.log", "auth.log", "cpu.log", "openvpn.log", "access.log", "error.log"
	   -> zwei audit.logs: des Internal Shares und des Intranet Servers 
	   -> "wheeler" besitzt keinen cpu.log
[LogAusschnittLaenge]: Die Ausschnittlänge jedes Logs ist angepasst, sodass sie insgesamt ca. 4000 Tokens
		       der meisten LLMs entsprechen (siehe 1.2 "Tokenizer" für mehr Informationen)
Erstellt im Rahmen der Bachelorarbeit "Large Language Modelle zur Logdaten-Analyse und Angriffserkennung"
der Rheinischen Friedrich-Wilhelms-Universität Bonn von Elisabeth Alice Rahn (s27erahn@uni-bonn.de).
Dieser Datensatz basiert auf Daten aus dem "AIT Log Dataset V2.0" (https://zenodo.org/records/5789064).

Layout:
/[sysname]: 
	-> attacks.log : Alle Angriffe, die auf das System während Runtime getätigt wurden
/[sysname]/gather/:
	-> label_[logname] : Grundwahrheit der entsprechenden Log-Datei aller verdächtigen Zeilen
/[sysname]/gather/ganze_dateien: 
	-> /true_pos/: Originale Log-Dateien
	-> /true_neg/: Log-Dateien, gekürzt um Zeilen, die Angriffe verzeichnen
/[sysname]/gather/ausschnitte:
	-> /true_pos/: Ausschnitte der Länge [LogAusschnittLaenge] (siehe unten), mit aber nicht ausschließlich verdächtigen Zeilen der Grundwahrheit
	-> /true_neg/: Ausschnitte der Länge [LogAusschnittLaenge] oder kürzer, ohne jegliche verdächtige Zeilen

[sysname]: Der Datensatz besteht aus 8 Systemen: 
	   "fox", "harrison", "russellmitchell", "santos", "shaw", "wardbeck", "wheeler", "wilson"
[logname]: Jeder Datensatz besitzt 7 verschiedene Log-Typen:
	   "dnsmasq.log", "audit.log", "auth.log", "cpu.log", "openvpn.log", "access.log", "error.log"
	   -> zwei audit.logs: des Internal Shares und des Intranet Servers 
	   -> "wheeler" besitzt keinen cpu.log
[LogAusschnittLaenge]: Die Ausschnittlänge jedes Logs ist angepasst, sodass sie insgesamt ca. 4000 Tokens
		       der meisten LLMs entsprechen (siehe 5.5.1 "Preprocessing der Log-Ausschnitte" für mehr Informationen)

/fox/gather/ausschnitte/natural_language_queries/ enthält alle Ausschnitte und Anfragen, die mit diesem gegebenen Kontext ausgewertet wurden. (Siehe english_log_type.txt für Kapitel 6: Log-Typ Bestimmung und english_queries.txt Kapitel 7: Natural Language Abfragen)

/[sysname]/gather/ausschnitte/ enthält alle Ausschnitte, die im Rahmen von Kapitel 8: Der Angriffserkennung in Log-Ausschnitten untersucht wurden. Alle Dateien sind als json strukturiert:
    - "data": Die tatsächlichen Zeilen des Ausschnittes
    - "lines": Anfang und End-Zeile des Ausschnittes bezogen auf die originale Datei
    - "labels": Alle Angriffslabels der Grundwahrheit, aufgelistet mit den entsprechenden Zeilen

Innerhalb des Ordners "LLM_Screenshots" sind Screenshots aller LLM-Antworten der durchgeführten Aufgaben auffindbar. Die Screenshots sind nach folgendem Schema benannt:

Log-Typ Erkennung: logtyp_[logname]_[llmname]_[0-9] 
NL Abfragen: [Level-Nr]_[logname]_[llmname]_[0-9]
Angriffserkennung: [tn/tp]_[logname]_[System und Ausschnitt-Nr]_[0-5]

[logname]: Name des untersuchten Logs
[llmname]: Name der verwendeten LLM
[Level-Nr]: lvl0, lvl1, lvl2 oder lvl3, je nach Level der behandelten Abfrage
[tn/tp]: tn für True Negative Ausschnitte, tp für True Positive Ausschnitte
[system und nr]: System (Fox, Harrison, etc.) und Nummer des durchgeführten Ausschnittes; zum Beispiel fox2

Die Zahl am Ende jeder Datei zählt die Durchläufe, die im Falle der Log-Typ Erkennung und NL Abfragen pro Log-Typ und LLM zehn Mal ausgeführt wird; im Falle der Angriffserkennung fünf Mal.





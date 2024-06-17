# Voorraadsysteem-
Het doel van dit project is om een eenvoudig voorraadsysteem te ontwerpen en te bouwen. 

# Omschrijving:
Het doel van dit project is om een voorraadsysteem te ontwerpen en te bouwen. Het systeem bestaat uit drie onderdelen:
- pc_x: databaseserver (MySQL database via het programma XAMPP)
- pc_y: pc met daaraan een scanner gekoppeld (scant voor artikel toevoegen aan database)
- pc_z: pc met daaraan een scanner gekoppeld (scant voor artikel verwijderen uit database)

Wanneer pc_y of pc_z een artikel gescand heeft, dan stuurt deze pc de barcode door naar pc_x. Vervolgens voert pc_x de mutatie in de mySQL database door. Omdat pc_y en pc_z gelijktijdig scannen en informatie doorsturen, wordt pc_x gebouwd als een multi-connection server. Alle wijzigingen die in de database worden opgeslagen, worden ook automatisch gedocumenteerd in een logboek. Er worden aparte logboeken bijgehouden op pc_x, pc_y en pc_z. 

# Gebruiksaanwijzing:
Voor pc_x:
Hiervoor is het nodig om XAMPP te installeren op de PC. Om de database te kunnen gebruiken, moet de gebruiker via XAMPP zowel de Apache app als de MySQL app starten. 
Verder zijn de volgende drie bestanden nodig (en dienen in dezelfde map opgeslagen te worden):
- article_database.py
- try_except_multi_connection_versie.py
- writing_to_txt.py

Voor pc_y (en pc_z):
PC2 bevat 3 bestanden die van elkaar afhankelijk zijn en dus samen in een folder geplaatst moeten worden.
Main.py bevat de main loop waarmee je het programma start.
BarcodeScanner.py bevat code voor het openen van de camera, het scannen van barcodes, het versturen van de barcode naar de Database-pc, en het schrijven van een logboek.
BarcodeScanner_GUI.py bevat de grafische interface dat het programma toegankelijk maakt, en bestaat uit een menu met een optie om de scanner/camera aan en uit te zetten, een optie om het logboek te laten zien, en een optie om de snelheid van de scanner te veranderen (de delay geeft het aantal secondes aan tussen elke scan die de camera maakt)

LET OP: 
1. Naast het downloaden van de bestanden moet ook een logboek-bestand aangemaakt worden VOORDAT je het programma start, onder de naam 'barcode_logbook.txt', dat in dezelfde folder geplaatst moet worden.
2. De scanner kan zowel gebruikt worden om exemplaren van een artikel aan de database toe te voegen als om exemplaren van een artikel uit de database te verwijderen. Hiervoor is het nodig om in de code een “+” te veranderen in “-” of omgekeerd. 

# Programmeertaal + versie:
Python

# Gebruikte modules:
asyncio
json
mysql.connector
datetime (date, datetime)
os


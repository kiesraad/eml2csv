# Hoe te gebruiken

Hieronder staat per besturingssysteem uitgelegd hoe je de EML-bestanden kan omzetten naar CSV-bestanden.

## Windows

Dit is de aanbevolen (en makkelijkste) methode.
- Op de hoofdpagina van de eml2csv-repository klik je aan de rechterkant op [Releases](https://github.com/kiesraad/eml2csv/releases).
- Klik bij de bovenste release op `Assets` en klik vervolgens op het installatiebestand `eml2csv-[versienummer].exe` om het te downloaden.
- Kopieer het installatiebestand naar een aparte map.
- Kopieer de volgende EML-bestanden naar dezelfde map als het installatiebestand:
    - Tellingbestand (EML 510b)
    - Kandidatenlijstenbestand (EML 230b)
- Selecteer eerst het tellingbestand.
- Houd `CTRL` ingedrukt om ook het kandidatenlijstenbestand te selecteren.
- Sleep de 2 EML-bestanden nu naar het installatiebestand.
- Het programma zet de EML-bestanden nu om naar een CSV-bestand. Dit CSV-bestand wordt in dezelfde map opgeslagen.
Het CSV-bestand heet `osv4-3_telling_{naam_verkiezing}_{gemeente/openbaar_lichaam}_{gemeentenaam}.csv`.

Bovenstaande stappen zijn ook terug te kijken op deze video:
https://github.com/user-attachments/assets/86053e07-e164-49a4-bb6e-c28dde467fbc

### Windows (geavanceerd)

Deze methode is alleen geschikt voor gebruikers die overweg kunnen met PowerShell.
- Op de hoofdpagina van de eml2csv-repository klik je aan de rechterkant op [Releases](https://github.com/kiesraad/eml2csv/releases).
- Klik bij de bovenste release op `Assets` en klik vervolgens op het installatiebestand `eml2csv-[versienummer].exe` om het te downloaden.
- Kopieer het installatiebestand naar een aparte map.
- Kopieer de volgende EML-bestanden naar dezelfde map als het installatiebestand:
    - Tellingbestand (EML 510b)
    - Kandidatenlijstenbestand (EML 230b).
- Open PowerShell.
- Navigeer naar deze map in PowerShell.
- Voer het volgende commando uit om de EML-bestanden om te zetten.
Vervang hierbij alles wat in blokhaken `[]` staat door de juiste bestandsnamen.
`eml2csv-[versienummer].exe [TELLING_BESTAND].eml.xml [KANDIDATENLIJSTEN_BESTAND].eml.xml`
- Het programma zet de EML-bestanden nu om naar een CSV-bestand. Dit CSV-bestand wordt in dezelfde map opgeslagen.
Het CSV-bestand heet `osv4-3_telling_{naam_verkiezing}_{gemeente/openbaar_lichaam}_{gemeentenaam}.csv`.

- Het is ook mogelijk om nog een derde parameter mee te geven; hiermee kan je de naam van het CSV-bestand aanpasssen:
`eml2csv-[versienummer].exe [TELLING_BESTAND].eml.xml [KANDIDATENLIJSTEN_BESTAND].eml.xml andere_naam_csv_bestand.csv`
Het CSV-bestand heet nu `andere_naam_csv_bestand.csv`.

Uitleg over de 3 parameters is hiermee te raadplegen: `eml2csv-[versienummer].exe --help`

## Linux/MacOS

- Op de hoofdpagina van de eml2csv-repository klik je aan de rechterkant op [Releases](https://github.com/kiesraad/eml2csv/releases).
- Klik bij de bovenste release op `Assets` en klik vervolgens op de extensieloze binary `eml2csv-[versienummer]` om het te downloaden.
- Kopieer de binary naar een aparte map.
- Kopieer de volgende EML-bestanden naar dezelfde map als de binary:
    - Tellingbestand (EML 510b)
    - Kandidatenlijstenbestand (EML 230b).
- Open de terminal.
- Navigeer naar deze map in de terminal.
- Voer het volgende commando uit om de EML-bestanden om te zetten.
  Vervang hierbij alles wat in blokhaken `[]` staat door de juiste bestandsnamen.
  `eml2csv-[versienummer] [TELLINGBESTAND].eml.xml [KANDIDATENLIJSTENBESTAND].eml.xml`
- Het programma zet de EML-bestanden nu om naar een CSV-bestand. Dit CSV-bestand wordt in dezelfde map opgeslagen.
  Het CSV-bestand heet `osv4-3_telling_{naam_verkiezing}_{gemeente/openbaar_lichaam}_{gemeentenaam}.csv`.

- Het is ook mogelijk om nog een derde parameter mee te geven. Dit is een optionele parameter. Hiermee kan je de naam van het CSV-bestand aanpasssen:
  `eml2csv-[versienummer] [TELLING_BESTAND].eml.xml [KANDIDATENLIJSTEN_BESTAND].eml.xml andere_naam_csv_bestand.csv`
  Het CSV-bestand heet nu `andere_naam_csv_bestand.csv`.

Uitleg over de 3 parameters is hiermee te raadplegen: `eml2csv-[versienummer] --help`.

# CSV-bestanden bekijken in Excel

Hieronder staat uitgelegd hoe je de CSV-bestanden het beste kan importeren in Excel.

- Open Microsoft Excel.
- Ga naar **Bestand > Openen** en blader naar de locatie met het CSV-bestand.
- In de vervolgkeuzelijst **Bestandstype** selecteer je **Tekstbestanden** .
- Zoek naar het CSV-bestand dat je wilt openen en dubbelklik hierop.

Het CSV-bestand is nu geïmporteerd in Excel.

_Opmerking:_ Het wordt afgeraden om het CSV-bestand te importeren via **Gegevens** > **Gegevens ophalen**. Dit resulteert in een incomplete import.

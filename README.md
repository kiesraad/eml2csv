# eml2csv
Python package for converting an [EML_NL](https://github.com/kiesraad/EML_NL) file to a csv file (osv4-3) format.

[![PyPI - Version](https://img.shields.io/pypi/v/eml2csv.svg)](https://pypi.org/project/eml2csv)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/eml2csv.svg)](https://pypi.org/project/eml2csv)

-----

**Table of Contents**

- [Background](#background)
- [Installation](#installation)
- [How to use](#how-to-use)
- [License](#license)

## Background
Since [Abacus](https://github.com/kiesraad/abacus) will output only the [EML_NL](https://github.com/kiesraad/EML_NL) and PV (PDF) files, the code in this repository can be used to generate a (legacy) osv4-3 CSV file. This is because we (Kiesraad) still want to facilitate the creation of these CSV files, while Abacus can focus on outputting files according to the official [EML_NL](https://github.com/kiesraad/EML_NL) standard.

This CSV file is published by municipalities and is openable in standard spreadsheet software for some simple analysis or visualisations.

## Installation
To install the package in your local environment:
```console
pip install eml2csv
```

## How to use
The package defines a function `eml2csv` which takes three parameters:

- `counts_eml_path: str`: path to the `EML 510b` file for which you want to create the csv file
- `candidates_eml_path: str`: path to the `EML 230b` file containing the candidate information. This file has to match the election and 'contest' (Kieskring) of the `EML 510b` file and is needed for adding the names of the candidates to the csv file
- `output_csv_path: str`: output filename for the csv file. **Note: if the file already exists, it will be overwritten!**

Example usage:
```python
from eml2csv import eml2csv

eml2csv(
    counts_eml_path="Telling_EP2024_gemeente_Juinen.eml.xml",
    candidates_eml_path="Kandidatenlijsten_EP2024.eml.xml",
    output_csv_path="osv4-3_telling_ep2024_juinen.csv",
)
```

## License

`eml2csv` is distributed under the terms of the [EUPL-1.2](https://spdx.org/licenses/EUPL-1.2.html) license.


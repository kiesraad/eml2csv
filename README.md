# eml2csv
Python package for converting an [EML_NL](https://github.com/kiesraad/EML_NL) file to a csv file (osv4-3) format.

-----

**Table of Contents**

- [Installation](#installation)
- [How to use](#how-to-use)
- [License](#license)

## Installation
To install the package in your local environment, download the [latest built version](https://github.com/kiesraad/eml2csv/releases/latest) (`.whl`)
```console
pip install eml2csv-{version}-py3-none-any.whl
```

Alternatively, you can run the script locally with uv `uv run eml2csv --help` or download [one of the packaged binaries](https://github.com/kiesraad/eml2csv/releases/latest) which ship with a python interpreter and required dependencies for use on airgapped systems.

## How to use
### Drag and drop
If you've downloaded the latest binary release you can generate a .csv file by simply dragging the required files (Telling and Kandidatenlijsten) on the executable. **Make sure that you drag both files, and drag from the 'Telling_' file to ensure that it is passed as the first argument**.

https://github.com/user-attachments/assets/86053e07-e164-49a4-bb6e-c28dde467fbc



### As a library
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

### CLI util
The package also includes a CLI utility for ease of use, run the following from your terminal for help
```console
eml2csv --help
```

## License

`eml2csv` is distributed under the terms of the [EUPL-1.2](https://spdx.org/licenses/EUPL-1.2.html) license.


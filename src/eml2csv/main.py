from typing import Annotated

import typer

from eml2csv import eml2csv


def main(
    counts_eml: Annotated[
        str,
        typer.Argument(
            help="Path to the counts EML file to generate the csv for (EML-510b)"
        ),
    ],
    candidates_eml: Annotated[
        str,
        typer.Argument(
            help="Path to the candidates EML file which corresponds to the specified counts EML (EML-230b)"
        ),
    ],
    output: Annotated[
        str | None,
        typer.Option(
            help="""CSV file to write to. NOTE: if the file already exists then it will be overwritten!\n
            If left blank, filename will be automatically generated and written to the current working directory"""
        ),
    ] = None,
):
    eml2csv(counts_eml, candidates_eml, output)


def start() -> None:
    typer.run(main)


if __name__ == "__main__":
    start()

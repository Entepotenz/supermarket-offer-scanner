import io
import urllib.request
import pprint
from typing import Optional, List

import typer
from typing_extensions import Annotated

from PdfPatternMatching import PdfPatterMatching
from ActionProspectusPdfScraper import ActionProspectusPdfScraper

app = typer.Typer(add_completion=False)


shop_names = ["lidl", "aldi"]


def get_name():
    return pprint.pformat(shop_names)


@app.command()
def main(
    shop_name: Annotated[str, typer.Argument(help=get_name())],
    matchers: Annotated[Optional[List[str]], typer.Option()],
    headless: Annotated[
        Optional[bool],
        typer.Option("--headless/--not-headless", help="selenium headless mode"),
    ] = True,
    pushover_token: Annotated[Optional[str], typer.Option()] = None,
    pushover_user_key: Annotated[Optional[str], typer.Option()] = None,
):
    if not shop_name or not shop_name.lower() in shop_names:
        print("No valid provided SHOP_NAME")
        raise typer.Abort()
    typer.echo(f"ShopName: {shop_name}")
    if not matchers:
        print("No provided matcher - at least one matcher is required")
        raise typer.Abort()
    typer.echo(f"Matchers: {matchers}")

    if (pushover_token and not pushover_user_key) or (
        not pushover_token and pushover_user_key
    ):
        print("if using pushover you need to provide the token AND user_key")
        raise typer.Abort()
    typer.echo(f"pushover_token: {pushover_token}")
    typer.echo(f"pushover_user_key: {pushover_user_key}")

    regex_pattern_collection = ["({})".format(item) for item in matchers]

    scraper = ActionProspectusPdfScraper(headless=headless)

    for url in scraper.get_urls():
        # Download PDF and read response
        response = urllib.request.urlopen(url)
        pdf_file = io.BytesIO(response.read())

        result = PdfPatterMatching.run_and_get_results(
            pdf_file, regex_pattern_collection
        )

        pprint.pprint(result)


if __name__ == "__main__":
    app()

import io
import os
import pprint
import urllib.request
from typing import Optional, List

import typer
from typing_extensions import Annotated

from PdfPatternMatching import PdfPatterMatching
from PromotionLeafletPdfScraper.PdfScraper import PdfScraper
from Pushover import Pushover

app = typer.Typer(add_completion=False)

shop_names = ["lidl", "aldinord"]

ENVIRONMENT_VARIABLE_PUSHOVER_USER_KEY = "PUSHOVER_USER_KEY"
ENVIRONMENT_VARIABLE_PUSHOVER_TOKEN = "PUSHOVER_TOKEN"


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
    regex_pattern_collection = matchers

    pushover_service = None

    pushover_user_key = os.getenv(
        ENVIRONMENT_VARIABLE_PUSHOVER_USER_KEY, pushover_user_key
    )
    pushover_token = os.getenv(ENVIRONMENT_VARIABLE_PUSHOVER_TOKEN, pushover_token)

    if (pushover_token and not pushover_user_key) or (
        not pushover_token and pushover_user_key
    ):
        print(
            f"if using pushover you need to provide the ${ENVIRONMENT_VARIABLE_PUSHOVER_USER_KEY} AND ${ENVIRONMENT_VARIABLE_PUSHOVER_TOKEN}"
        )
        raise typer.Abort()

    if pushover_token and pushover_user_key:
        print("using pushover notification service")
        pushover_service = Pushover(token=pushover_token, user_key=pushover_user_key)

    scraper = PdfScraper.get_pdf_scraper(shop_name=shop_name, headless=headless)

    for url in scraper.get_urls():
        # Download PDF and read response
        response = urllib.request.urlopen(url)
        pdf_file = io.BytesIO(response.read())

        result = PdfPatterMatching.run_and_get_results(
            pdf_file, regex_pattern_collection
        )

        if [item for item in result if (item and item != [])]:
            pprint.pprint(result)

            if pushover_service:
                pretty_result = pprint.pformat(result, indent=4)
                pushover_service.send_notification(pretty_result)
        else:
            print("no matches")


if __name__ == "__main__":
    app()

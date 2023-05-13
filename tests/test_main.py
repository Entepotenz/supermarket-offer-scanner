import logging
import os
import sys
import unittest

from hamcrest import equal_to, assert_that, contains_string
from typer.testing import CliRunner

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "source"))
)

from source import main

runner = CliRunner()

logger = logging.getLogger(__name__)


class TestMain(unittest.TestCase):
    def test_app_lidl(self):
        result = runner.invoke(
            main.app,
            [
                "lidl",
                "--matchers",
                "montag",
                "--matchers",
                "dienstag",
                "--loglevel",
                "debug",
            ],
        )
        assert_that(result.exit_code, equal_to(0))
        assert_that(result.stdout, contains_string("ShopName: lidl"))
        assert_that(result.stdout, contains_string("Matchers: ['montag', 'dienstag']"))
        assert_that(result.stdout, contains_string("Montag"))
        assert_that(result.stdout, contains_string("Dienstag"))

    def test_app_aldinord(self):
        result = runner.invoke(
            main.app,
            [
                "aldinord",
                "--matchers",
                "mon",
                "--matchers",
                "die",
                "--loglevel",
                "debug",
            ],
        )
        assert_that(result.exit_code, equal_to(0))
        assert_that(result.stdout, contains_string("ShopName: aldinord"))
        assert_that(result.stdout, contains_string("Matchers: ['mon', 'die']"))
        assert_that(result.stdout, contains_string("Mon"))
        assert_that(result.stdout, contains_string("Die"))

    def test_app_hit(self):
        result = runner.invoke(
            main.app,
            ["hit", "--matchers", "mon", "--matchers", "die", "--loglevel", "debug"],
        )
        assert_that(result.exit_code, equal_to(0))
        assert_that(result.stdout, contains_string("ShopName: hit"))
        assert_that(result.stdout, contains_string("Matchers: ['mon', 'die']"))
        assert_that(result.stdout, contains_string("Mon"))
        assert_that(result.stdout, contains_string("Die"))


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, format="%(name)s %(levelname)s %(message)s"
    )
    unittest.main()

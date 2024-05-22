from plone import api
from typing import Any

import pytest

class TestPortalSettings:

    @pytest.mark.parametrize(
        "setting,expected",
        [
            ["plone.site_title", "Nova Intranet TRE-MS"],
            ["plone.portal_timezone", "America/Campo_Grande"],
            ["plone.enable_sitemap", True],
            ["plone.email_charset", "utf-8"],
            ["plone.email_from_name", "Nova Intranet TRE-MS"],
            ["plone.email_from_address", "intranet@tre-ms.jus.br"],
            ["plone.smtp_host", "localhost"],
            ["plone.smtp_port", 25],
            ["plone.default_language", "pt-br"],
            ["plone.twitter_username", "Jota"],
        ]
    )
    def test_portal_settings(self, portal, setting: str, expected: Any):
        value = api.portal.get_registry_record(setting)
        assert value == expected, (
            f"Valor incorreto para {setting}: {value} ao invés de {expected}"
        )

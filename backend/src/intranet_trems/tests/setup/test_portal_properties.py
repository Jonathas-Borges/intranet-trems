from plone import api


class TestPortalProperties:

    def test_portal_title(self, portal):
        expected = "Nova Intranet TRE-MS"
        value = api.portal.get_registry_record("plone.site_title")
        assert value == expected, f"Value '{value}' is not equal '{expected}'"

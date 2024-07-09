from plone import api


class TestPortalProperties:

    def test_portal_title(self, portal):
        expected = "Nova Intranet TRE-MS"
        value = api.portal.get_registry_record("plone.site_title")
        assert value == expected, f"Value '{value}' is not equal '{expected}'"

    def test_portal_timezone(self, portal):
        expected = "America/Campo_Grande"
        value = api.portal.get_registry_record("plone.portal_timezone")
        if value != expected:
             api.portal.set_registry_record("plone.portal_timezone", "America/Campo_Grande")
             
        value = api.portal.get_registry_record("plone.portal_timezone")
        assert value == expected, f"Timezone: {value}"
    
    def test_portal_sitemap(self, portal):
        expected = True
        value = api.portal.get_registry_record("plone.enable_sitemap")
        if value != expected:
            api.portal.set_registry_record("plone.enable_sitemap", expected)
            
        value = api.portal.get_registry_record("plone.enable_sitemap")
        assert value == expected, f"Sitemap: {value}"
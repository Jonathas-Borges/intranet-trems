from intranet_trems import logger
from intranet_trems.services.clima import openmeteo
from plone import api
from plone.restapi.services import Service


class ClimaGet(Service):
    @property
    def coordinates(self) -> tuple:
        """Retorna latitude e longitude de Campo Grande."""
        return (-20.440078701095434, -54.55944068419852)

    @property
    def timezone(self) -> str:
        return api.portal.get_registry_record("plone.portal_timezone")

    def reply(self):
        portal = api.portal.get()
        portal_url = portal.absolute_url()
        latitude, longitude = self.coordinates
        timezone = self.timezone
        dados = openmeteo.dados_clima(latitude, longitude, timezone)
        dados["@id"] = f"{portal_url}/@clima"
        logger.info("Retorna dados do clima")
        return dados

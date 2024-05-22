from intranet_trems import logger
from intranet_trems.setuphandlers.content import populate_portal
from plone import api


def cria_estrutura(context):
    portal = api.portal.get()
    populate_portal(
        portal,
        [
            "TRE-MS",
        ],
    )
    logger.info("Criando testes de perssionamento para Área")


def alterar_permissionamento_estrutura(context):
    portal = api.portal.get()
    estrutura = portal["estrutura"]
    permission_id = "intranet_trems: Add Area"
    roles = [
        "Contributor",
        "Editor",
        "Manager",
        "Site Administrator",
    ]
    estrutura.manage_permission(permission_id, roles=roles)
    logger.info(f"Alterado permissionamento em {estrutura}.")

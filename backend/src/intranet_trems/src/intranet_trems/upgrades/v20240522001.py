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
    logger.info("Criados conteúdos para organizar Áreas e Pessoas.")


def alterar_permissionamento_colaboradores(context):
    portal = api.portal.get()
    colaboradores = portal["colaboradores"]
    permission_id = "intranet_trems: Add Pessoa"
    roles = [
        "Contributor",
        "Editor",
        "Manager",
        "Site Administrator",
    ]
    colaboradores.manage_permission(permission_id, roles=roles)
    logger.info(f"Alterado permissionamento em {colaboradores}.")

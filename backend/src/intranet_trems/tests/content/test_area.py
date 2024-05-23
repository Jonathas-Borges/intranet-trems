from intranet_trems.content.area import Area
from plone import api
from plone.dexterity.fti import DexterityFTI
from zope.component import createObject
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent


import pytest


CONTENT_TYPE = "Area"


@pytest.fixture
def payload() -> dict:
    """Payload to create a new Area."""
    return {
       "type": CONTENT_TYPE,
        "title": "STI",
        "description": "Secretária de Tecnologia da Informação",
        "email": "sti@plone.org",
        "ramal": "1234",
        "id": "sti",
    }


class TestArea:
    @pytest.fixture(autouse=True)
    def _fti(self, get_fti, integration):
        self.fti = get_fti(CONTENT_TYPE)

    def test_fti(self):
        assert isinstance(self.fti, DexterityFTI)

    def test_factory(self):
        factory = self.fti.factory
        obj = createObject(factory)
        assert obj is not None
        assert isinstance(obj, Area)

    @pytest.mark.parametrize(
        "behavior",
        [
            "plone.namefromtitle",
            "plone.shortname",
            "plone.excludefromnavigation",
            "plone.versioning",
        ],
    )
    def test_has_behavior(self, get_behaviors, behavior):
        assert behavior in get_behaviors(CONTENT_TYPE)

    @pytest.mark.parametrize(
    "roles",
        [
            ["Manager"],
            ["Editor"],
            ["Contributor"],
            ["Site Administrator"],
        ]
    )

    def test_cant_create_outsite_estrutura(self, portal, payload, roles):
        from AccessControl.unauthorized import Unauthorized

        with pytest.raises(Unauthorized) as exc:
            with api.env.adopt_roles(roles):
                api.content.create(container=portal, **payload)
        assert "Cannot create Area" in str(exc)

    @pytest.mark.parametrize(
        "roles",
        [
            ["Manager"],
            ["Editor"],
            ["Contributor"],
            ["Site Administrator"],
        ]
    )
    def test_create_inside_estrutura(self, portal, payload, roles):
        container = portal["estrutura"]
        with api.env.adopt_roles(roles):
            content = api.content.create(container=container, **payload)
        assert content.portal_type == CONTENT_TYPE
        assert isinstance(content, Area)

        def test_review_state(self, portal, payload):
            container = portal["estrutura"]
            with api.env.adopt_roles(["Manager"]):
                content = api.content.create(container=container, **payload)
            assert api.content.get_state(content) == "internal"
        
    def test_transition_editor_cannot_publish_internally(self, portal, payload):
        container = portal["estrutura"]
        with api.env.adopt_roles(["Editor"]):
            content = api.content.create(container=container, **payload)
            with pytest.raises(api.exc.InvalidParameterError) as exc:
                api.content.transition(content, "publish_internally")
        assert "Invalid transition 'publish_internally'" in str(exc)
        assert api.content.get_state(content) == "internal"

    def test_transition_reviewer_can_publish_internally(self, portal, payload):
        container = portal["estrutura"]
        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=container, **payload)
        with api.env.adopt_roles(["Reviewer", "Member"]):
            api.content.transition(content, "publish_internally")
        assert api.content.get_state(content) == "internally_published"
    
    def test_review_state(self, portal, payload):
        container = portal["estrutura"]
        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=container, **payload)
        assert api.content.get_state(content) == "internal"

    def test_subscriber_added_with_description_value(self, portal):
        container = portal["estrutura"]
        with api.env.adopt_roles(["Manager"]):
            area = api.content.create(
                container=container,
                type=CONTENT_TYPE,
                title="Comunicação",
                description="Área de Comunicação",
                email="secom@tre-ms.jus.br",
                tipo_email="corporativo",
                ramal="2022",
            )
        assert area.exclude_from_nav is False

    def test_subscriber_added_without_description_value(self, portal):
        container = portal["estrutura"]
        with api.env.adopt_roles(["Manager"]):
            area = api.content.create(
                container=container,
                type=CONTENT_TYPE,
                title="Comunicação",
                description="",
                email="secom@tre-ms.jus.br",
                ramal="2022",
            )
        assert area.exclude_from_nav is True

    def test_subscriber_modified(self, portal):
            container = portal["estrutura"]
            with api.env.adopt_roles(["Manager"]):
                area = api.content.create(
                    container=container,
                    type=CONTENT_TYPE,
                    title="Comunicação",
                    description="",
                    email="secom@tre-ms.jus.br",
                    ramal="2022",
                )
            assert area.exclude_from_nav is True
            # Altera a descricao
            area.description = "Nossa área"
            # Dispara o evento de modificacao
            notify(ObjectModifiedEvent(area))
            # Agora o objeto aparece na navegação
            assert area.exclude_from_nav is False
    
    def test_subscriber_added_creates_group(self, portal, payload):
        from Products.PlonePAS.tools.groupdata import GroupData

        container = portal["estrutura"]
        with api.env.adopt_roles(["Manager"]):
            area = api.content.create(container=container, **payload)
        area_uuid = api.content.get_uuid(area)
        group_name = f"{area_uuid}_editors"
        group = api.group.get(groupname=group_name)
        assert isinstance(group, GroupData)
        roles = api.group.get_roles(group=group, obj=area)
        assert "Editor" in roles

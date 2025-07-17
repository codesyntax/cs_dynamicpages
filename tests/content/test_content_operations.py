from plone import api
import pytest
from ..base import TestBase


class TestContent(TestBase):

    @pytest.fixture(autouse=True)
    def create_content(self, portal):
        with api.env.adopt_roles(["Manager"]):
            self.folder = api.content.create(
                container=portal,
                type="Folder",
                id="folder",
            )

            assert self.folder is not None
            assert self.folder.id == "folder"

            self.dpf = api.content.create(
                container=self.folder, type="DynamicPageFolder", id="dpf", title="DPF"
            )

            assert self.dpf is not None
            assert self.dpf.id == "dpf"

            self.row1 = api.content.create(
                container=self.dpf, type="DynamicPageRow", id="row-1", title="Row 1"
            )
            assert self.row1 is not None
            assert self.row1.id == "row-1"

            self.row2 = api.content.create(
                container=self.dpf, type="DynamicPageRow", id="row-2", title="Row 2"
            )
            assert self.row2 is not None
            assert self.row2.id == "row-2"

    def test_view(self, portal, my_request):
        self.folder.setLayout('dynamic-view')

        view = api.content.get_view(
            context=self.folder, name="dynamic-view", request=my_request
        )

        assert view().find('Add row') != -1

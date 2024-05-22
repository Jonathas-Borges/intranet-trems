from intranet_trems import PACKAGE_NAME


class TestSetupInstall:
    def test_addon_installed(self, installer):
        """Test if intranet_trems is installed."""
        assert installer.is_product_installed(PACKAGE_NAME) is True

    def test_browserlayer(self, browser_layers):
        """Test that IIntranetTremsLayer is registered."""
        from intranet_trems.interfaces import IIntranetTremsLayer

        assert IIntranetTremsLayer in browser_layers

    def test_latest_version(self, profile_last_version):
        """Test latest version of default profile."""
        assert profile_last_version(f"{PACKAGE_NAME}:default") == "20240522001"

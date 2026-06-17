import pytest


@pytest.mark.smoke
class TestEnvironment:
    def test_environment_file_loaded(self):
        assert self.reportTitle == "Web_EMS_NewCase"
        assert self.node_name == "NODE1"
        assert self.dutName == "DUT_NODE1"

    def test_runtime_paths_are_ready(self):
        assert self.downloadpath
        assert self.reportPath


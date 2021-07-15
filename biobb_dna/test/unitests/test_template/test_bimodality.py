from biobb_common.tools import test_fixtures as fx
from biobb_dna.dna.bimodality import helparbimodality


class TestBimodality():
    def setUp(self):
        fx.test_setup(self, 'bimodality')

    def tearDown(self):
        fx.test_teardown(self)

    def test_helparbimodality(self):
        returncode = helparbimodality(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_file_path'])
        assert fx.exe_success(returncode)
        assert fx.equal(
            self.paths['output_file_path'],
            self.paths['ref_output_file_path'])

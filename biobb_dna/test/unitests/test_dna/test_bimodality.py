# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_dna.dna.dna_bimodality import dna_bimodality


class TestBimodality():
    def setup_class(self):
        fx.test_setup(self, 'dna_bimodality')

    def teardown_class(self):
        fx.test_teardown(self)
        pass

    def test_helparbimodality(self):
        returncode = dna_bimodality(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_csv_path'])
        assert fx.not_empty(self.paths['output_jpg_path'])
        assert fx.exe_success(returncode)

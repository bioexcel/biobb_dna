from biobb_common.tools import test_fixtures as fx
from biobb_dna.dna.dna_timeseries_unzip import dna_timeseries_unzip


class TestCanalUnzip():
    def setup_class(self):
        fx.test_setup(self, 'dna_timeseries_unzip')

    def teardown_class(self):
        fx.test_teardown(self)

    def test_dna_timeseries_unzip(self):
        returncode = dna_timeseries_unzip(
            properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_path_csv'])
        assert fx.not_empty(self.paths['output_path_jpg'])
        assert fx.not_empty(self.paths['output_list_path'])
        assert fx.exe_success(returncode)
        assert fx.equal(
            self.paths['output_path_csv'],
            self.paths['ref_output_path_csv'])
        assert fx.equal(
            self.paths['output_list_path'],
            self.paths['ref_output_list_path'])
        assert fx.equal(self.paths['output_path_jpg'], self.paths['ref_output_path_jpg'])

# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_dna.curvesplus.canal_unzip import canal_unzip


class TestCanalUnzip():
    def setup_class(self):
        fx.test_setup(self, 'canal_unzip')

    def teardown_class(self):
        fx.test_teardown(self)

    def test_canal_unzip(self):
        returncode = canal_unzip(
            properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_path'])
        assert fx.not_empty(self.paths['output_list_path'])
        assert fx.exe_success(returncode)
        assert fx.equal(
            self.paths['output_path'],
            self.paths['ref_output_path'])
        assert fx.equal(
            self.paths['output_list_path'],
            self.paths['ref_output_list_path'])

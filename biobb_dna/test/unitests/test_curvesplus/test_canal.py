from biobb_common.tools import test_fixtures as fx
from biobb_dna.curvesplus.biobb_canal import biobb_canal


class TestCanal():
    def setUp(self):
        fx.test_setup(self, 'biobb_canal')

    def tearDown(self):
        fx.test_teardown(self)

    def test_canal(self):
        returncode = biobb_canal(
            properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_zip_path'])
        assert fx.exe_success(returncode)
        assert fx.equal(
            self.paths['output_zip_path'],
            self.paths['ref_output_zip_path'])

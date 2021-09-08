from biobb_common.tools import test_fixtures as fx
from biobb_dna.curvesplus.biobb_curves import curves


class TestCurves():
    def setUp(self):
        fx.test_setup(self, 'biobb_curves')

    def tearDown(self):
        fx.test_teardown(self)

    def test_curves(self):
        returncode = curves(
            properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_cda_path'])
        assert fx.not_empty(self.paths['output_lis_path'])
        assert fx.exe_success(returncode)
        assert fx.equal(
            self.paths['output_cda_path'],
            self.paths['ref_cda_output'])

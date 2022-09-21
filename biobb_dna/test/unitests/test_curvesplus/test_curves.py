from biobb_common.tools import test_fixtures as fx
from biobb_dna.curvesplus.biobb_curves import biobb_curves


class TestCurves():
    def setup_class(self):
        fx.test_setup(self, 'biobb_curves')

    def teardown_class(self):
        fx.test_teardown(self)

    def test_curves(self):
        returncode = biobb_curves(
            properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_cda_path'])
        assert fx.not_empty(self.paths['output_lis_path'])
        assert fx.exe_success(returncode)
        assert fx.equal(
            self.paths['output_cda_path'],
            self.paths['ref_cda_output'])
        assert fx.equal(
            self.paths['output_lis_path'],
            self.paths['ref_lis_output'])
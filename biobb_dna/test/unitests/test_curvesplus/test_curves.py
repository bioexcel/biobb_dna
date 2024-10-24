# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_dna.curvesplus.biobb_curves import biobb_curves
import platform


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
        assert fx.not_empty(self.paths['output_zip_path'])
        assert fx.exe_success(returncode)
        if platform.system() == 'Darwin':
            assert fx.equal(self.paths['output_cda_path'], self.paths['ref_cda_output'])
        assert fx.compare_line_by_line(self.paths['output_lis_path'], self.paths['ref_lis_output'], [2])
        assert fx.equal(self.paths['output_zip_path'], self.paths['ref_zip_output'])

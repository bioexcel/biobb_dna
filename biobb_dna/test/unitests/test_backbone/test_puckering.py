# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_dna.backbone.puckering import puckering
import platform


class TestPuckering():
    def setup_class(self):
        fx.test_setup(self, 'puckering')

    def teardown_class(self):
        fx.test_teardown(self)

    def test_puckering(self):
        returncode = puckering(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_csv_path'])
        assert fx.not_empty(self.paths['output_jpg_path'])
        assert fx.exe_success(returncode)
        if platform.system() == 'Darwin':
            assert fx.equal(self.paths['output_csv_path'], self.paths['ref_csv_output'])
        assert fx.equal(self.paths['output_jpg_path'], self.paths['ref_jpg_output'], percent_tolerance=20)

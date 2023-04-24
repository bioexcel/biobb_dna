from biobb_common.tools import test_fixtures as fx
from biobb_dna.dna.dna_averages import dna_averages
from biobb_dna.test.unitests.common import compare_images
import platform

import logging
mpl_logger = logging.getLogger("matplotlib")
mpl_logger.setLevel(logging.ERROR)


class TestAverages():
    def setup_class(self):
        fx.test_setup(self, 'dna_averages')

    def teardown_class(self):
        fx.test_teardown(self)

    def test_helparaverages(self):
        returncode = dna_averages(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_csv_path'])
        assert fx.not_empty(self.paths['output_jpg_path'])
        assert fx.exe_success(returncode)
        if platform.system() == 'Darwin':
            assert fx.equal(self.paths['output_csv_path'], self.paths['ref_csv_output'])
        assert compare_images(self.paths['output_jpg_path'], self.paths['ref_jpg_output'])

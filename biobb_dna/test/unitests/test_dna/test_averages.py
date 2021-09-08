from biobb_common.tools import test_fixtures as fx
from biobb_dna.dna.dna_averages import helparaverages

import logging
mpl_logger = logging.getLogger("matplotlib")
mpl_logger.setLevel(logging.ERROR)


class TestAverages():
    def setUp(self):
        fx.test_setup(self, 'dna_averages')

    def tearDown(self):
        fx.test_teardown(self)

    def test_helparaverages(self):
        returncode = helparaverages(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_csv_path'])
        assert fx.not_empty(self.paths['output_jpg_path'])
        assert fx.exe_success(returncode)
        assert fx.equal(
            self.paths['output_csv_path'],
            self.paths['ref_csv_output'])
        assert fx.equal(
            self.paths['output_jpg_path'],
            self.paths['ref_jpg_output'])

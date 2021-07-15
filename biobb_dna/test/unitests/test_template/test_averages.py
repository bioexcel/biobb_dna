from biobb_common.tools import test_fixtures as fx
from biobb_common.tools import file_utils as fu
from biobb_dna.dna.averages import helparaverages

import logging
mpl_logger = logging.getLogger("matplotlib")
mpl_logger.setLevel(logging.ERROR)


class TestAverages():
    def setUp(self):
        fx.test_setup(self, 'averages')

    def tearDown(self):
        fx.test_teardown(self)

    def test_helparaverages(self):
        returncode = helparaverages(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_file_path'])
        assert fx.exe_success(returncode)
        assert fx.equal(
            self.paths['output_file_path'],
            self.paths['ref_output_file_path'])

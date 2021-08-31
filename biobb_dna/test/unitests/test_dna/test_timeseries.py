from biobb_common.tools import test_fixtures as fx
from biobb_dna.dna.timeseries import helpartimeseries


import logging
mpl_logger = logging.getLogger("matplotlib")
mpl_logger.setLevel(logging.ERROR)


class TestTimeSeries():
    def setUp(self):
        fx.test_setup(self, 'timeseries')

    def tearDown(self):
        fx.test_teardown(self)

    def test_helpartimeseries(self):
        returncode = helpartimeseries(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_zip_path'])
        assert fx.exe_success(returncode)
        assert fx.equal(
            self.paths['output_zip_path'],
            self.paths['ref_output_zip_path'])

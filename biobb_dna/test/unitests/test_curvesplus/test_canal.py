from biobb_common.tools import test_fixtures as fx
from biobb_dna.curvesplus.canal import canal


class TestCanal():
    def setUp(self):
        fx.test_setup(self, 'canal')

    def tearDown(self):
        fx.test_teardown(self)

    def test_canal(self):
        returncode = canal(
            properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_zip_path'])
        assert fx.exe_success(returncode)

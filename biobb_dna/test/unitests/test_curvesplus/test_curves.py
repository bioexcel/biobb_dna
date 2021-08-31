from biobb_common.tools import test_fixtures as fx
from biobb_dna.curvesplus.curves import curves


class TestCurvesTRJ():
    def setUp(self):
        fx.test_setup(self, 'curves_trj')

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


class TestCurvesNC():
    def setUp(self):
        fx.test_setup(self, 'curves_nc')

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


class TestCurvesPDB():
    def setUp(self):
        fx.test_setup(self, 'curves_pdb')

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

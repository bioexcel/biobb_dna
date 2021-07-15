from biobb_common.tools import test_fixtures as fx
from biobb_dna.dna.stiffness import helparstiffness


class TestStiffness():
    def setUp(self):
        fx.test_setup(self, 'stiffness')

    def tearDown(self):
        fx.test_teardown(self)

    def test_helparstiffness(self):
        returncode = helparstiffness(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_covariance_path'])
        assert fx.not_empty(self.paths['output_stiffness_path'])
        assert fx.not_empty(self.paths['output_fctes_path'])
        assert fx.not_empty(self.paths['output_averages_path'])
        assert fx.exe_success(returncode)
        assert fx.equal(
            self.paths['output_covariance_path'],
            self.paths['ref_output_covariance_path'])
        assert fx.equal(
            self.paths['output_stiffness_path'],
            self.paths['ref_output_stiffness_path'])
        assert fx.equal(
            self.paths['output_fctes_path'],
            self.paths['ref_output_fctes_path'])
        assert fx.equal(
            self.paths['output_averages_path'],
            self.paths['ref_output_averages_path'])

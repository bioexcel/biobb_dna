from biobb_common.tools import test_fixtures as fx
from biobb_dna.stiffness.average_stiffness import averagestiffness
from biobb_dna.stiffness.basepair_stiffness import bpstiffness


class TestAvgStiffness():
    def setUp(self):
        fx.test_setup(self, 'avgstiffness')

    def tearDown(self):
        fx.test_teardown(self)

    def test_averagestiffness(self):
        returncode = averagestiffness(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_csv_path'])
        assert fx.not_empty(self.paths['output_jpg_path'])
        assert fx.exe_success(returncode)
        assert fx.equal(
            self.paths['output_csv_path'],
            self.paths['ref_csv_output'])
        assert fx.equal(
            self.paths['output_jpg_path'],
            self.paths['ref_jpg_output'])


class TestBasePairStiffness():
    def setUp(self):
        fx.test_setup(self, 'bpstiffness')

    def tearDown(self):
        fx.test_teardown(self)

    def test_basepairstiffness(self):
        returncode = bpstiffness(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_csv_path'])
        assert fx.not_empty(self.paths['output_jpg_path'])
        assert fx.exe_success(returncode)
        assert fx.equal(
            self.paths['output_csv_path'],
            self.paths['ref_csv_output'])
        assert fx.equal(
            self.paths['output_jpg_path'],
            self.paths['ref_jpg_output'])

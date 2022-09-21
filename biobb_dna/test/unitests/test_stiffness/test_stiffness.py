from biobb_common.tools import test_fixtures as fx
from biobb_dna.stiffness.average_stiffness import average_stiffness
from biobb_dna.stiffness.basepair_stiffness import basepair_stiffness


class TestAvgStiffness():
    def setup_class(self):
        fx.test_setup(self, 'average_stiffness')

    def teardown_class(self):
        fx.test_teardown(self)

    def test_averagestiffness(self):
        returncode = average_stiffness(
            properties=self.properties, **self.paths)
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
    def setup_class(self):
        fx.test_setup(self, 'basepair_stiffness')

    def teardown_class(self):
        fx.test_teardown(self)

    def test_basepairstiffness(self):
        returncode = basepair_stiffness(
            properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_csv_path'])
        assert fx.not_empty(self.paths['output_jpg_path'])
        assert fx.exe_success(returncode)
        assert fx.equal(
            self.paths['output_csv_path'],
            self.paths['ref_csv_output'])
        assert fx.equal(
            self.paths['output_jpg_path'],
            self.paths['ref_jpg_output'])

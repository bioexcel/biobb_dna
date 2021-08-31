from biobb_common.tools import test_fixtures as fx
from biobb_dna.correlations.helparcorrelation import helparcorrelation
from biobb_dna.correlations.sequencecorrelation import sequencecorrelation
from biobb_dna.correlations.basepaircorrelation import basepaircorrelation


class TestHelparCorrelation():
    def setUp(self):
        fx.test_setup(self, 'hpcorrelation')

    def tearDown(self):
        fx.test_teardown(self)

    def test_helparcorrelation(self):
        returncode = helparcorrelation(**self.paths)
        assert fx.not_empty(self.paths['output_csv_path'])
        assert fx.not_empty(self.paths['output_jpg_path'])
        assert fx.exe_success(returncode)
        assert fx.equal(
            self.paths['output_csv_path'],
            self.paths['ref_csv_output'])
        assert fx.equal(
            self.paths['output_jpg_path'],
            self.paths['ref_jpg_output'])


class TestSequenceCorrelation():
    def setUp(self):
        fx.test_setup(self, 'seqcorrelation')

    def tearDown(self):
        fx.test_teardown(self)

    def test_sequencecorrelation(self):
        returncode = sequencecorrelation(
            properties=self.properties,
            **self.paths)
        assert fx.not_empty(self.paths['output_csv_path'])
        assert fx.not_empty(self.paths['output_jpg_path'])
        assert fx.exe_success(returncode)
        assert fx.equal(
            self.paths['output_csv_path'],
            self.paths['ref_csv_output'])
        assert fx.equal(
            self.paths['output_jpg_path'],
            self.paths['ref_jpg_output'])


class TestBasepairCorrelation():
    def setUp(self):
        fx.test_setup(self, 'bpcorrelation')

    def tearDown(self):
        fx.test_teardown(self)

    def test_basepaircorrelation(self):
        returncode = basepaircorrelation(
            properties=self.properties,
            **self.paths)
        assert fx.not_empty(self.paths['output_csv_path'])
        assert fx.not_empty(self.paths['output_jpg_path'])
        assert fx.exe_success(returncode)
        assert fx.equal(
            self.paths['output_csv_path'],
            self.paths['ref_csv_output'])
        assert fx.equal(
            self.paths['output_jpg_path'],
            self.paths['ref_jpg_output'])

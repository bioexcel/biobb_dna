from biobb_common.tools import test_fixtures as fx
from biobb_dna.interbp_correlations.interhpcorr import interhelparcorrelation
from biobb_dna.interbp_correlations.interseqcorr import intersequencecorrelation
from biobb_dna.interbp_correlations.interbpcorr import interbasepaircorrelation
from biobb_dna.intrabp_correlations.intrahpcorr import intrahelparcorrelation
from biobb_dna.intrabp_correlations.intraseqcorr import intrasequencecorrelation
from biobb_dna.intrabp_correlations.intrabpcorr import intrabasepaircorrelation


class TestInterHelparCorrelation():
    def setUp(self):
        fx.test_setup(self, 'interhpcorr')

    def tearDown(self):
        fx.test_teardown(self)

    def test_helparcorrelation(self):
        returncode = interhelparcorrelation(**self.paths)
        assert fx.not_empty(self.paths['output_csv_path'])
        assert fx.not_empty(self.paths['output_jpg_path'])
        assert fx.exe_success(returncode)
        assert fx.equal(
            self.paths['output_csv_path'],
            self.paths['ref_csv_output'])
        assert fx.equal(
            self.paths['output_jpg_path'],
            self.paths['ref_jpg_output'])


class TestInterSequenceCorrelation():
    def setUp(self):
        fx.test_setup(self, 'interseqcorr')

    def tearDown(self):
        fx.test_teardown(self)

    def test_sequencecorrelation(self):
        returncode = intersequencecorrelation(
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


class TestInterBasepairCorrelation():
    def setUp(self):
        fx.test_setup(self, 'interbpcorr')

    def tearDown(self):
        fx.test_teardown(self)

    def test_basepaircorrelation(self):
        returncode = interbasepaircorrelation(
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


class TestIntraHelparCorrelation():
    def setUp(self):
        fx.test_setup(self, 'intrahpcorr')

    def tearDown(self):
        fx.test_teardown(self)

    def test_helparcorrelation(self):
        returncode = intrahelparcorrelation(**self.paths)
        assert fx.not_empty(self.paths['output_csv_path'])
        assert fx.not_empty(self.paths['output_jpg_path'])
        assert fx.exe_success(returncode)
        assert fx.equal(
            self.paths['output_csv_path'],
            self.paths['ref_csv_output'])
        assert fx.equal(
            self.paths['output_jpg_path'],
            self.paths['ref_jpg_output'])


class TestIntraSequenceCorrelation():
    def setUp(self):
        fx.test_setup(self, 'intraseqcorr')

    def tearDown(self):
        fx.test_teardown(self)

    def test_sequencecorrelation(self):
        returncode = intrasequencecorrelation(
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


class TestIntraBasepairCorrelation():
    def setUp(self):
        fx.test_setup(self, 'intrabpcorr')

    def tearDown(self):
        fx.test_teardown(self)

    def test_basepaircorrelation(self):
        returncode = intrabasepaircorrelation(
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

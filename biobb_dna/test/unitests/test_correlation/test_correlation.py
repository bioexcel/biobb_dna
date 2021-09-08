from biobb_common.tools import test_fixtures as fx
from biobb_dna.interbp_correlations.intersequencecorrelation import interhelparcorrelation
from biobb_dna.interbp_correlations.intersequencecorrelation import intersequencecorrelation
from biobb_dna.interbp_correlations.interbasepaircorrelation import interbasepaircorrelation
from biobb_dna.intrabp_correlations.intrahelparcorrelation import intrahelparcorrelation
from biobb_dna.intrabp_correlations.intrasequencecorrelation import intrasequencecorrelation
from biobb_dna.intrabp_correlations.intrabasepaircorrelation import intrabasepaircorrelation


class TestInterHelparCorrelation():
    def setUp(self):
        fx.test_setup(self, 'interhelparcorrelation')

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
        fx.test_setup(self, 'intersequencecorrelation')

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
        fx.test_setup(self, 'interbasepaircorrelation')

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
        fx.test_setup(self, 'intrahelparcorrelation')

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
        fx.test_setup(self, 'intrasequencecorrelation')

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
        fx.test_setup(self, 'intrabasepaircorrelation')

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

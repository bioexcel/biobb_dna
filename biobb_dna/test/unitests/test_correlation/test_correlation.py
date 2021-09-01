from biobb_common.tools import test_fixtures as fx
from biobb_dna.interbp_correlations.helparcorrelation import helparcorrelation as inter_helparcorrelation
from biobb_dna.interbp_correlations.sequencecorrelation import sequencecorrelation as inter_sequencecorrelation
from biobb_dna.interbp_correlations.basepaircorrelation import basepaircorrelation as inter_basepaircorrelation
from biobb_dna.intrabp_correlations.helparcorrelation import helparcorrelation as intra_helparcorrelation
from biobb_dna.intrabp_correlations.sequencecorrelation import sequencecorrelation as intra_sequencecorrelation
from biobb_dna.intrabp_correlations.basepaircorrelation import basepaircorrelation as intra_basepaircorrelation


class TestInterHelparCorrelation():
    def setUp(self):
        fx.test_setup(self, 'inter_hpcorrelation')

    def tearDown(self):
        fx.test_teardown(self)

    def test_helparcorrelation(self):
        returncode = inter_helparcorrelation(**self.paths)
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
        fx.test_setup(self, 'inter_seqcorrelation')

    def tearDown(self):
        fx.test_teardown(self)

    def test_sequencecorrelation(self):
        returncode = inter_sequencecorrelation(
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
        fx.test_setup(self, 'inter_bpcorrelation')

    def tearDown(self):
        fx.test_teardown(self)

    def test_basepaircorrelation(self):
        returncode = inter_basepaircorrelation(
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
        fx.test_setup(self, 'intra_hpcorrelation')

    def tearDown(self):
        fx.test_teardown(self)

    def test_helparcorrelation(self):
        returncode = intra_helparcorrelation(**self.paths)
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
        fx.test_setup(self, 'intra_seqcorrelation')

    def tearDown(self):
        fx.test_teardown(self)

    def test_sequencecorrelation(self):
        returncode = intra_sequencecorrelation(
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
        fx.test_setup(self, 'intra_bpcorrelation')

    def tearDown(self):
        fx.test_teardown(self)

    def test_basepaircorrelation(self):
        returncode = intra_basepaircorrelation(
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

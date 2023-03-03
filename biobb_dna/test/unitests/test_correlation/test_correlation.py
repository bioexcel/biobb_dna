from biobb_common.tools import test_fixtures as fx
from biobb_dna.interbp_correlations.interhpcorr import interhpcorr
from biobb_dna.interbp_correlations.interseqcorr import interseqcorr
from biobb_dna.interbp_correlations.interbpcorr import interbpcorr
from biobb_dna.intrabp_correlations.intrahpcorr import intrahpcorr
from biobb_dna.intrabp_correlations.intraseqcorr import intraseqcorr
from biobb_dna.intrabp_correlations.intrabpcorr import intrabpcorr
import platform

class TestInterHelparCorrelation():
    def setup_class(self):
        fx.test_setup(self, 'interhpcorr')

    def teardown_class(self):
        fx.test_teardown(self)

    def test_helparcorrelation(self):
        returncode = interhpcorr(**self.paths)
        assert fx.not_empty(self.paths['output_csv_path'])
        assert fx.not_empty(self.paths['output_jpg_path'])
        assert fx.exe_success(returncode)
        if platform.system() == 'Darwin':
            assert fx.equal(
                self.paths['output_csv_path'],
                self.paths['ref_csv_output'])
            assert fx.equal(
                self.paths['output_jpg_path'],
                self.paths['ref_jpg_output'])


class TestInterSequenceCorrelation():
    def setup_class(self):
        fx.test_setup(self, 'interseqcorr')

    def teardown_class(self):
        fx.test_teardown(self)

    def test_sequencecorrelation(self):
        returncode = interseqcorr(
            properties=self.properties,
            **self.paths)
        assert fx.not_empty(self.paths['output_csv_path'])
        assert fx.not_empty(self.paths['output_jpg_path'])
        assert fx.exe_success(returncode)
        if platform.system() == 'Darwin':
            assert fx.equal(
                self.paths['output_csv_path'],
                self.paths['ref_csv_output'])
            assert fx.equal(
                self.paths['output_jpg_path'],
                self.paths['ref_jpg_output'])


class TestInterBasepairCorrelation():
    def setup_class(self):
        fx.test_setup(self, 'interbpcorr')

    def teardown_class(self):
        fx.test_teardown(self)

    def test_basepaircorrelation(self):
        returncode = interbpcorr(
            properties=self.properties,
            **self.paths)
        assert fx.not_empty(self.paths['output_csv_path'])
        assert fx.not_empty(self.paths['output_jpg_path'])
        assert fx.exe_success(returncode)
        if platform.system() == 'Darwin':
            assert fx.equal(
                self.paths['output_csv_path'],
                self.paths['ref_csv_output'])
            assert fx.equal(
                self.paths['output_jpg_path'],
                self.paths['ref_jpg_output'])


class TestIntraHelparCorrelation():
    def setup_class(self):
        fx.test_setup(self, 'intrahpcorr')

    def teardown_class(self):
        fx.test_teardown(self)

    def test_helparcorrelation(self):
        returncode = intrahpcorr(**self.paths)
        assert fx.not_empty(self.paths['output_csv_path'])
        assert fx.not_empty(self.paths['output_jpg_path'])
        assert fx.exe_success(returncode)
        if platform.system() == 'Darwin':
            assert fx.equal(
                self.paths['output_csv_path'],
                self.paths['ref_csv_output'])
            assert fx.equal(
                self.paths['output_jpg_path'],
                self.paths['ref_jpg_output'])


class TestIntraSequenceCorrelation():
    def setup_class(self):
        fx.test_setup(self, 'intraseqcorr')

    # def teardown_class(self):
    #     fx.test_teardown(self)

    def test_sequencecorrelation(self):
        returncode = intraseqcorr(
            properties=self.properties,
            **self.paths)
        assert fx.not_empty(self.paths['output_csv_path'])
        assert fx.not_empty(self.paths['output_jpg_path'])
        assert fx.exe_success(returncode)
        if platform.system() == 'Darwin':
            assert fx.equal(
                self.paths['output_csv_path'],
                self.paths['ref_csv_output'])
            assert fx.equal(
                self.paths['output_jpg_path'],
                self.paths['ref_jpg_output'])


class TestIntraBasepairCorrelation():
    def setup_class(self):
        fx.test_setup(self, 'intrabpcorr')

    def teardown_class(self):
        fx.test_teardown(self)

    def test_basepaircorrelation(self):
        returncode = intrabpcorr(
            properties=self.properties,
            **self.paths)
        assert fx.not_empty(self.paths['output_csv_path'])
        assert fx.not_empty(self.paths['output_jpg_path'])
        assert fx.exe_success(returncode)
        if platform.system() == 'Darwin':
            assert fx.equal(
                self.paths['output_csv_path'],
                self.paths['ref_csv_output'])
            assert fx.equal(
                self.paths['output_jpg_path'],
                self.paths['ref_jpg_output'])

# type: ignore
from biobb_common.tools import test_fixtures as fx
from biobb_dna.curvesplus.biobb_canal import biobb_canal
import pytest
import sys


class TestCanalDocker():
    def setup_class(self):
        fx.test_setup(self, 'biobb_canal_docker')

    def teardown_class(self):
        fx.test_teardown(self)

    def test_canal_docker(self):
        returncode = biobb_canal(
            properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_zip_path'])
        assert fx.exe_success(returncode)
        # assert fx.equal(self.paths['output_zip_path'], self.paths['ref_output_zip_path'])


@pytest.mark.skipif(sys.platform == 'darwin', reason="singularity not available on macOS")
class TestCanalSingularity():
    def setup_class(self):
        fx.test_setup(self, 'biobb_canal_singularity')

    def teardown_class(self):
        fx.test_teardown(self)

    def test_canal_singularity(self):
        returncode = biobb_canal(
            properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_zip_path'])
        assert fx.exe_success(returncode)
        # assert fx.equal(self.paths['output_zip_path'], self.paths['ref_output_zip_path'])

from biobb_common.tools import test_fixtures as fx
from biobb_dna.backbone.canonicalag import canonicalag
from biobb_dna.test.unitests.common import compare_images
import platform


class TestCanonicalAlphaGamma():
    def setup_class(self):
        fx.test_setup(self, 'canonicalag')

    def teardown_class(self):
        fx.test_teardown(self)

    def test_canonicalag(self):
        returncode = canonicalag(properties=self.properties, **self.paths)
        assert fx.not_empty(self.paths['output_csv_path'])
        assert fx.not_empty(self.paths['output_jpg_path'])
        assert fx.exe_success(returncode)
        if platform.system() == 'Darwin':
            assert fx.equal(self.paths['output_csv_path'], self.paths['ref_csv_output'])
        assert compare_images(self.paths['output_jpg_path'], self.paths['ref_jpg_output'])

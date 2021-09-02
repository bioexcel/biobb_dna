import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb_dna",
    version="1.1.0",
    author="Biobb developers",
    author_email="lucia.fabio@irbbarcelona.com",
    description="Biobb_dna is a package composed of different analyses for nucleic acid trajectories.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="Bioinformatics Workflows BioExcel Compatibility",
    url="https://github.com/bioexcel/biobb_dna",
    project_urls={
        "Documentation": "http://biobb_dna.readthedocs.io/en/latest/",
        "Bioexcel": "https://bioexcel.eu/"
    },
    packages=setuptools.find_packages(exclude=['adapters', 'docs', 'test']),
    install_requires=[
        'biobb_common>=3.5.1',
        'pandas>=1.3',
        'matplotlib>=3.4',
        'numpy>=1.21',
        'scikit-learn>=0.24'],
    python_requires='==3.7.*',
    entry_points={
        "console_scripts": [
            "biobb_curves = biobb_dna.curvesplus.curves:main",
            "biobb_canal = biobb_dna.curvesplus.canal:main",
            "dna_averages = biobb_dna.dna.averages:main",
            "dna_timeseries = biobb_dna.dna.timeseries:main",
            "dna_bimodality = biobb_dna.dna.bimodality:main",
            "bipopulations = biobb_dna.backbone.bipopulations:main",
            "canonicalag = biobb_dna.backbone.canonical_alpha_gamma:main",
            "puckering = biobb_dna.backbone.puckering:main",
            "inter_bpcorr = biobb_dna.interbp_correlations.basepaircorrelation:main",
            "inter_hpcorr = biobb_dna.interbp_correlations.helparcorrelation:main",
            "inter_seqcorr = biobb_dna.interbp_correlations.sequencecorrelation:main",
            "intra_bpcorr = biobb_dna.intrabp_correlations.basepaircorrelation:main",
            "intra_hpcorr = biobb_dna.intrabp_correlations.helparcorrelation:main",
            "intra_seqcorr = biobb_dna.intrabp_correlations.sequencecorrelation:main",
            "avgstiff = biobb_dna.stiffness.average_stiffness:main",
            "bpstiff = biobb_dna.stiffness.basepair_stiffness:main"
        ]
    },
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
    ),
)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb_dna",
    version="5.3.0",
    author="Biobb developers",
    author_email="genis.bayarri@irbbarcelona.com",
    description="Biobb_dna is a package composed of different analyses for nucleic acid trajectories.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="Bioinformatics Workflows BioExcel Compatibility",
    url="https://github.com/bioexcel/biobb_dna",
    project_urls={
        "Documentation": "http://biobb-dna.readthedocs.io/en/latest/",
        "Bioexcel": "https://bioexcel.eu/",
    },
    packages=setuptools.find_packages(exclude=["adapters", "docs", "test"]),
    package_data={"biobb_dna": ["py.typed"]},
    install_requires=["biobb_common==5.3.1", "pandas>=1.3.0", "scikit-learn>=0.24.2"],
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "biobb_curves = biobb_dna.curvesplus.biobb_curves:Curves.main",
            "biobb_canal = biobb_dna.curvesplus.biobb_canal:Canal.main",
            "canal_unzip = biobb_dna.curvesplus.canal_unzip:CanalUnzip.main",
            "biobb_canion = biobb_dna.curvesplus.biobb_canion:Canion.main",
            "dna_averages = biobb_dna.dna.dna_averages:HelParAverages.main",
            "dna_timeseries = biobb_dna.dna.dna_timeseries:HelParTimeSeries.main",
            "dna_timeseries_unzip = biobb_dna.dna.dna_timeseries_unzip:DnaTimeseriesUnzip.main",
            "dna_bimodality = biobb_dna.dna.dna_bimodality:HelParBimodality.main",
            "bipopulations = biobb_dna.backbone.bipopulations:BIPopulations.main",
            "canonicalag = biobb_dna.backbone.canonicalag:CanonicalAG.main",
            "puckering = biobb_dna.backbone.puckering:Puckering.main",
            "interbpcorr = biobb_dna.interbp_correlations.interbpcorr:InterBasePairCorrelation.main",
            "interhpcorr = biobb_dna.interbp_correlations.interhpcorr:InterHelParCorrelation.main",
            "interseqcorr = biobb_dna.interbp_correlations.interseqcorr:InterSequenceCorrelation.main",
            "intrabpcorr = biobb_dna.intrabp_correlations.intrabpcorr:IntraBasePairCorrelation.main",
            "intrahpcorr = biobb_dna.intrabp_correlations.intrahpcorr:IntraHelParCorrelation.main",
            "intraseqcorr = biobb_dna.intrabp_correlations.intraseqcorr:IntraSequenceCorrelation.main",
            "average_stiffness = biobb_dna.stiffness.average_stiffness:AverageStiffness.main",
            "basepair_stiffness = biobb_dna.stiffness.basepair_stiffness:BPStiffness.main",
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: Unix",
    ],
)

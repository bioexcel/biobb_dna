def inverse_complement(sequence, dna=True):
    """compute inverse complement sequence."""
    if dna:
        A_complement = "T"
    else:
        A_complement = "U"
    complement = {
        "A": A_complement,
        A_complement: "A",
        "G": "C",
        "C": "G"
    }
    return "".join([complement[b] for b in sequence])[::-1]

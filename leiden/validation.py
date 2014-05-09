import re


def is_concordant(protein_change_1, protein_change_2):

    protein_change_1 = normalize_protein_notation(protein_change_1)
    protein_change_2 = normalize_protein_notation(protein_change_2)

    if protein_change_1 == '' or protein_change_2 == '':
        return False

    return protein_change_1 == protein_change_2


def normalize_protein_notation(protein_change_notation):
    if ':' in protein_change_notation:
        protein_change_notation = protein_change_notation.split(':')[1]

    protein_change_notation = protein_change_notation.lower()
    protein_change_notation = re.sub('xaa', '*', protein_change_notation)
    protein_change_notation = re.sub('x', '*', protein_change_notation)
    protein_change_notation = re.sub('ter', '*', protein_change_notation)
    protein_change_notation = remove_p_dot_notation(protein_change_notation)

    return protein_change_notation

def get_ucsc_location_link(chromosome_number, start_coordinate, end_coordinate):
    """
    Returns link to relevant range in the UCSC genome browser. All parameters must be in valid range.

    Args:
        chromosome_number (str): the chromosome number of the range to link to
        start_coordinate (str): the start coordinate of range to link to
        end_coordinate (str): the end coordinate of range to link to

    Returns:
        str: URL link to display region in UCSC genome browser

    """
    return ''.join(['http://genome.ucsc.edu/cgi-bin/hgTracks?db=hg19&position=chr', chromosome_number, '%3A',
                    start_coordinate, '-', end_coordinate])


def remove_p_dot_notation(annotation_text):
    """
    Removes the p-dot notation from a description of protein change. Accepted formats are p.change, p.(change,
    or p.[change], where change is returned and is the description of the protein change.

    Args:
        annotation_text (str): p-dot notation describing the protein change

    Returns:
        str: Annotation_text with the p-dot notation removed

    Exceptiom:
        ValueError: if the p-dot notation is not in one of the expected formats.

    """

    search_pattern = re.compile('[p]\.[\(\[]?([^\)\]]+)[\)\]]?', re.IGNORECASE)
    match = re.search(search_pattern, annotation_text)

    if match:
        return match.group(1)
    elif annotation_text == '-':
        return annotation_text
    else:
        return annotation_text
import json

from tagalog.parsing import get_tokens_and_labels


def test_json_parsing():
    test_file = "tests/data/data.json"
    reference_file = "tests/data/data.conll"

    # Parse the reference CONLL file
    reference_tokens = []
    reference_labels = []

    with open(reference_file) as i:
        for line in i:
            line = line.strip().split("\t")

            if len(line) == 2 and line[0] != "-DOCSTART-":
                reference_tokens[-1].append(line[0])
                reference_labels[-1].append(line[1])
            elif line[0] == "-DOCSTART-":
                reference_tokens.append([])
                reference_labels.append([])

    # Parse the Montague JSON file
    with open(test_file) as i:
        montague_json = json.load(i)

    document_tokens = []
    document_labels = []
    for text, tokens, labels in get_tokens_and_labels(montague_json):
        document_tokens.append(tokens)
        document_labels.append(labels)

    # Test for equality
    assert document_tokens == reference_tokens
    assert document_labels == reference_labels

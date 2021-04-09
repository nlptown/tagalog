BEGIN_PREFIX = "B"
INSIDE_PREFIX = "I"
OUTSIDE_LABEL = "O"


def get_id2label(tagalog_json):
    """ Get a dictionary that maps the id of a label to the label text. """

    id2label = {}
    for label_set in tagalog_json["label_sets"]:
        for label in label_set["labels"]:
            id2label[label["id"]] = label["text"]

    return id2label


def iterate_tokens(document_metrics):
    """ Iterate through all the tokens in a document. """

    tcl = list(map(int, document_metrics["tcl"].split(",")))  # token lengths
    tci = list(map(int, document_metrics["tci"].split(",")))  # character offsets of all tokens, relative to their block
    bci = list(map(int, document_metrics["bci"].split(",")))  # index of the first character in every block
    bti = list(map(int, document_metrics["bti"].split(",")))  # index of the first token in every block
    pbi = list(map(int, document_metrics["pbi"].split(",")))  # index of the first block in every page

    pbi.append(len(bti))
    bti.append(len(tci))

    for page_idx in range(len(document_metrics["pbi"])):
        for block_idx_rel, block_idx_abs in enumerate(range(pbi[page_idx], pbi[page_idx + 1])):
            for token_idx_rel, token_idx_abs in enumerate(range(bti[block_idx_abs], bti[block_idx_abs + 1])):
                yield page_idx, block_idx_rel, token_idx_rel, token_idx_abs, \
                      bci[block_idx_abs] + tci[token_idx_abs], tcl[token_idx_abs]


def get_best_document_annotation(document_annotations):
    """
    Return the review annotation for a document if there is one.
    Otherwise return the first annotation.
    """
    for annotation in document_annotations:
        if annotation["is_review"]:
            return annotation

    if len(document_annotations) == 0:
        return None
    else:
        return document_annotations[0]


def get_tokens_and_labels(tagalog_json):
    """ Get all tokens and their labels from a Tagalog JSON.
    For every document, this yields the document text, a list of the tokens
    and a list of the corresponding labels.
    """

    id2label = get_id2label(tagalog_json)

    for document in tagalog_json["documents"]:
        text = document["content"]
        best_document_annotation = get_best_document_annotation(document["document_annotations"])

        if best_document_annotation is None:
            continue

        tok2label = {}
        for annotation in best_document_annotation["annotations"]:

            # Get the coordinates and the label id for the annotation
            coordinates = [map(int, c.split(":"))
                           for c in annotation["coordinates"].split(",")]

            page_idxs, block_idxs, token_idxs = zip(*coordinates)
            label_id = annotation["label_id"]

            for position, token_idx in enumerate(token_idxs):
                token_idx = token_idxs[position]
                prefix = BEGIN_PREFIX if position == 0 else INSIDE_PREFIX
                tok2label[token_idx] = (prefix, label_id)

        tokens, labels = [], []
        for _, _, _, token_idx, token_offset, token_length in iterate_tokens(document["metrics"]):

            token_text = text[token_offset:token_offset+token_length]
            tokens.append(token_text)

            prefix, token_label_id = tok2label.get(token_idx, (OUTSIDE_LABEL, None))
            if token_label_id is not None:
                label = f"{prefix}-{id2label[token_label_id]}"
            else:
                label = OUTSIDE_LABEL
            labels.append(label)

        yield text, tokens, labels

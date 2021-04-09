import click
import json
import csv

from tagalog import parsing


@click.command()
@click.argument('filename', type=click.Path(exists=True))
def json2conll(filename):
    with open(filename) as input_file:
        montague_json = json.load(input_file)

    output_filename = filename.replace(".json", ".conll")
    with open(output_filename, "w") as output_file:
        writer = csv.writer(output_file, delimiter="\t")

        for text, tokens, labels in parsing.get_tokens_and_labels(montague_json):

            writer.writerow(["-DOCSTART-", "0"])
            writer.writerow([f"# text = {text}"])

            for token, label in zip(tokens, labels):
                writer.writerow([token, label])
            writer.writerow([])


if __name__ == '__main__':
    json2conll()


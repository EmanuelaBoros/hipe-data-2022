"""Export train/dev documents without splitting entities at sentence markers.

JSONL documents are variable length. A model-specific tokenizer must handle
overflow using overlapping windows, keeping document identity and token indices.
Invalid BIO is rejected rather than silently relabelled. Test data is excluded.
"""
import argparse
import json
from pathlib import Path
from curate import read, audit


def documents(rows):
    current, tokens, labels = None, [], []
    for _, doc, cells in rows:
        if doc != current and tokens:
            yield dict(document_id=current, tokens=tokens, labels=labels)
            tokens, labels = [], []
        current = doc
        tokens.append(cells[0])
        labels.append(cells[1])
    if tokens:
        yield dict(document_id=current, tokens=tokens, labels=labels)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input', type=Path)
    p.add_argument('output', type=Path)
    args = p.parse_args()
    if not any('-'+s+'-' in args.input.name for s in ('train', 'dev', 'dev2')):
        raise ValueError('Only explicit train/dev/dev2 inputs accepted')
    _, rows = read(args.input)
    invalid = [f for f in audit(rows) if f['column'] == 1 and f['kind'] == 'invalid_bio']
    if invalid:
        raise ValueError(f'{len(invalid)} invalid coarse BIO transitions; adjudicate before training. First: {invalid[0]}')
    if any(c[1] == '_' for _, _, c in rows):
        raise ValueError('Missing coarse supervision')
    with args.output.open('x') as stream:
        for doc in documents(rows):
            doc['source'] = args.input.name
            stream.write(json.dumps(doc, ensure_ascii=False)+'\n')


if __name__ == '__main__':
    main()

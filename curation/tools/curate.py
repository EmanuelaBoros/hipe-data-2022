"""Reproducible HIPE v3.0 release from v2.1 annotation overlays and document-level BIO audit."""
import argparse
import collections
import hashlib
import json
import shutil
from pathlib import Path


def read(path):
    lines = path.read_text().splitlines()
    rows = []
    doc = None
    for n, line in enumerate(lines):
        if line.startswith('# hipe2022:document_id'):
            doc = line.split('=', 1)[1].strip()
        elif line and not line.startswith('#') and not line.startswith('TOKEN\t'):
            cells = line.split('\t')
            if len(cells) != 10:
                raise ValueError(f'{path}:{n+1}: expected 10 columns')
            rows.append((n, doc, cells))
    return lines, rows


def audit(rows):
    findings = []
    prev = None
    for n, doc, cells in rows:
        for col in range(1, 7):
            tag = cells[col]
            if not tag.startswith('I-'):
                continue
            valid = prev and prev[1] == doc and prev[2][col] in ('B-'+tag[2:], tag)
            if not valid:
                findings.append(dict(line=n+1, document=doc, column=col,
                                     kind='invalid_bio', token=cells[0], tag=tag))
            elif 'EndOfSentence' in prev[2][9].split('|'):
                findings.append(dict(line=n+1, document=doc, column=col,
                                     kind='entity_crosses_sentence', token=cells[0], tag=tag))
        prev = (n, doc, cells)
    return findings


def apply(lines, rows, edits):
    """All edits are exact-row guarded and checked before any output is written."""
    by_line = {n+1: (doc, cells) for n, doc, cells in rows}
    for edit in edits:
        doc, cells = by_line[edit['line']]
        if doc != edit['document'] or cells != edit['before']:
            raise ValueError(f"Stale correction: {edit['line']}")
    for edit in edits:
        lines[edit['line']-1] = '\t'.join(edit['after'])
    return '\n'.join(lines)+'\n'


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--manifest', type=Path, default=Path(__file__).resolve().parents[1]/'corrections.json')
    args = p.parse_args()
    source = (args.repo/'data/v2.1').resolve()
    output = args.output.resolve()
    if output == source or source in output.parents or output in source.parents:
        raise ValueError('Output must be separate from original release')
    if output.exists():
        raise ValueError('Choose a new output directory to avoid overwriting results')
    manifest = json.loads(args.manifest.read_text())
    edits = collections.defaultdict(list)
    for e in manifest['edits']:
        edits[e['file']].append(e)
    results, payloads = {}, {}
    for path in sorted(source.rglob('HIPE-2022-*.tsv')):
        relative = str(path.relative_to(source))
        lines, rows = read(path)
        changes = edits.pop(relative, [])
        target = relative.replace('HIPE-2022-v2.1-', 'HIPE-2022-v3.0-')
        payloads[target] = apply(lines, rows, changes)
        results[target] = dict(source_file='data/v2.1/'+relative, sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                                 edits=len(changes), findings=audit(rows))
    if edits:
        raise ValueError(f'Missing files: {list(edits)}')
    output.mkdir(parents=True)
    for relative, payload in payloads.items():
        dest = output/relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(payload)
        results[relative]['after_findings'] = audit(read(dest)[1])
    for path in source.rglob('*'):
        if path.is_file() and not path.name.startswith('HIPE-2022-'):
            dest = output/path.relative_to(source)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)
    shutil.copy2(Path(__file__).resolve().parents[1]/'RELEASE-v3.0.md', output/'README.md')
    (output/'audit.json').write_text(json.dumps(results, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps(dict(files=len(results), edits=sum(v['edits'] for v in results.values()),
                         before=dict(collections.Counter(f['kind'] for v in results.values() for f in v['findings'])),
                         after=dict(collections.Counter(f['kind'] for v in results.values() for f in v['after_findings']))), indent=2))


if __name__ == '__main__':
    main()

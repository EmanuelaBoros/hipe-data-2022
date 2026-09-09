import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'tools'))
from curate import audit, apply


def row(tag, misc='_'):
    return ['Name', tag, 'O', 'O', 'O', 'O', 'O', '_', '_', misc]


class AuditTests(unittest.TestCase):
    def test_sentence_inside_entity_is_not_invalid_bio(self):
        result = audit([(1, 'a', row('B-pers', 'EndOfSentence')), (2, 'a', row('I-pers'))])
        self.assertEqual([x['kind'] for x in result], ['entity_crosses_sentence'])

    def test_document_boundary_does_reset_bio(self):
        result = audit([(1, 'a', row('B-pers')), (2, 'b', row('I-pers'))])
        self.assertEqual(result[0]['kind'], 'invalid_bio')

    def test_type_mismatch(self):
        self.assertEqual(audit([(1, 'a', row('B-loc')), (2, 'a', row('I-org'))])[0]['kind'], 'invalid_bio')

    def test_stale_correction_fails(self):
        with self.assertRaises(ValueError):
            apply([''], [(0, 'a', row('B-pers'))], [dict(line=1, document='b', before=row('B-pers'), after=row('B-loc'))])


if __name__ == '__main__':
    unittest.main()

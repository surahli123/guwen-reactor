"""Task 4a.3 — required-beat coverage from VALIDATED supported-fact-ids (Contract C / C4).
TDD: written before guwen_core/coverage.py. A beat is covered iff ALL its fact_ids are
in supported_fact_ids — never self-reported, never keyword."""
from guwen_core.coverage import beat_coverage
from guwen_core.schema_validator import CanonScene


def _scene():
    return CanonScene.model_validate({
        "scene_id": "G01", "title_en": "x", "title_zh": "管寧割席", "source_id": "s",
        "source_chunks": [{"chunk_id": "C0", "text_zh": "x"}],
        "atomic_facts": [{"id": "F01", "text": "a", "source_chunk_ids": ["C0"]},
                         {"id": "F05", "text": "b", "source_chunk_ids": ["C0"]},
                         {"id": "F08", "text": "c", "source_chunk_ids": ["C0"]}],
        "required_beats": [{"beat_id": "B01", "fact_ids": ["F01"], "description": "garden"},
                           {"beat_id": "B02", "fact_ids": ["F05"], "description": "carriage"},
                           {"beat_id": "B03", "fact_ids": ["F08"], "description": "mat"}],
        "forbidden_claims": []})


def test_full_coverage():
    frac, val = beat_coverage({"F01", "F05", "F08"}, _scene())
    assert frac == "3/3" and val == 1.0


def test_omission_drops_below_gate():
    frac, val = beat_coverage({"F01", "F08"}, _scene())   # carriage beat (F05) unsupported
    assert frac == "2/3" and val < 0.85

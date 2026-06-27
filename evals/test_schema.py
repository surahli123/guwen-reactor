import pytest
from guwen_core.schema_validator import (
    CanonScene, StructuredClaim, ClaimLabel, AssertionType, Hedging,
)


def test_canon_scene_requires_chunk_anchored_facts_and_beats():
    scene = CanonScene(
        scene_id="G01", title_en="Guan Ning Cuts the Mat", title_zh="管寧割席",
        source_id="shishuo_xinyu_de_xing_guan_ning",
        source_chunks=[{"chunk_id": "C01", "text_zh": "管寧、華歆共園中鋤菜"}],
        atomic_facts=[{"id": "F01", "text": "They garden together.", "source_chunk_ids": ["C01"]}],
        required_beats=[{"beat_id": "B01", "fact_ids": ["F01"], "description": "Gold test."}],
        forbidden_claims=["Hua Xin keeps the gold."],
    )
    assert scene.atomic_facts[0].source_chunk_ids == ["C01"]   # Contract D: required anchor


def test_atomic_fact_requires_source_chunk_ids():
    with pytest.raises(ValueError):              # missing source_chunk_ids -> reject (Contract D)
        from guwen_core.schema_validator import AtomicFact
        AtomicFact(id="F1", text="x")


def test_structured_claim_carries_audit_fields():
    c = StructuredClaim(
        claim_id="X1", beat_id="B03", claim_text="t",
        source_fact_ids=["F08"], assertion_type=AssertionType.MOTIVE,
        hedging=Hedging.ASSERTED, artifact_path="storyboard.panels.P06.caption_en",
    )
    assert c.assertion_type is AssertionType.MOTIVE and c.hedging is Hedging.ASSERTED


def test_claim_label_enum_rejects_unknown():
    with pytest.raises(ValueError):
        ClaimLabel("NOT_A_LABEL")


def test_canon_gold_loads_chunk_anchored():
    from guwen_core.schema_validator import CanonScene
    import yaml, pathlib
    raw = yaml.safe_load(pathlib.Path("data/gold/canon_gold.yaml").read_text(encoding="utf-8"))
    scene = CanonScene.model_validate(raw["scenes"][0])
    assert scene.scene_id == "G01"
    assert {f.id for f in scene.atomic_facts} >= {"F08"}
    chunk_ids = {ch.chunk_id for ch in scene.source_chunks}
    # Contract D: every fact anchors to a real chunk
    for f in scene.atomic_facts:
        assert set(f.source_chunk_ids) <= chunk_ids


def test_all_canon_scenes_valid_and_anchored():
    """Every scene validates, anchors resolve, beats reference real facts, no dup fact ids."""
    from guwen_core.schema_validator import CanonScene
    import yaml, pathlib
    raw = yaml.safe_load(pathlib.Path("data/gold/canon_gold.yaml").read_text(encoding="utf-8"))
    scenes = raw["scenes"]
    assert {s["scene_id"] for s in scenes} >= {"G01", "G02", "G03"}
    for s in scenes:
        scene = CanonScene.model_validate(s)
        chunk_ids = {c.chunk_id for c in scene.source_chunks}
        fact_ids = [f.id for f in scene.atomic_facts]
        assert len(fact_ids) == len(set(fact_ids)), f"{scene.scene_id}: duplicate fact ids"
        for f in scene.atomic_facts:
            assert set(f.source_chunk_ids) <= chunk_ids, f"{scene.scene_id}/{f.id}: bad anchor"
        for b in scene.required_beats:
            assert set(b.fact_ids) <= set(fact_ids), f"{scene.scene_id}/{b.beat_id}: dangling beat ref"

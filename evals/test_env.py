"""Phase 0.2 environment smoke test.

Proves the pinned toolchain imports cleanly and that pydantic resolved to
the 2.x major line — the schema layer (Task 1.1) depends on pydantic v2.
This is the first 'fail loudly if the runtime is wrong' gate.
"""


def test_core_imports():
    import pydantic  # noqa: F401
    import yaml  # noqa: F401  (PyYAML)
    import typer  # noqa: F401
    import jinja2  # noqa: F401
    import rich  # noqa: F401

    assert pydantic.VERSION.startswith("2."), f"expected pydantic 2.x, got {pydantic.VERSION}"

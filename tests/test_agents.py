import pytest

from agents import coder_node, researcher_node


@pytest.fixture(autouse=True)
def set_test_env(monkeypatch):
    monkeypatch.setenv("USE_FAKE_OPENAI", "true")


def test_researcher_node_mock():
    result = researcher_node({"input": "Explain a neural network."})
    assert "research" in result and isinstance(result["research"], str)


def test_coder_node_mock():
    result = coder_node({"research": "Build a transformer model."})
    assert "code" in result and result["code"].startswith("def")

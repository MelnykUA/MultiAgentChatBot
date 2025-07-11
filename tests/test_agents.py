import pytest

from agents import coder_node, researcher_node


@pytest.fixture(autouse=True)
def enable_fake_openai(monkeypatch):
    monkeypatch.setenv("USE_FAKE_OPENAI", "true")


def test_researcher_node_mock():
    data = {"input": "Explain a neural network."}
    result = researcher_node(data)
    assert "research" in result
    assert isinstance(result["research"], str)


def test_coder_node_mock():
    data = {"research": "Build a transformer model."}
    result = coder_node(data)
    assert "code" in result
    assert result["code"].startswith("def")

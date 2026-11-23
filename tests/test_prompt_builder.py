
from backend.prompts.prompt_builder import build_excuse_prompt


def test_prompt_returns_system_and_user_messages():
    messages = build_excuse_prompt(
        situation="I forgot my assignment.",
        category="Academic",
        tone="Funny",
        creativity="High",
        formality="Casual",
        length="Medium"
    )

    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"


def test_prompt_includes_original_situation():
    situation = "I missed an important meeting."

    messages = build_excuse_prompt(situation=situation)

    assert situation in messages[1]["content"]


def test_prompt_includes_customization_preferences():
    messages = build_excuse_prompt(
        situation="I forgot my assignment.",
        category="Academic",
        tone="Funny",
        creativity="High",
        formality="Casual",
        length="Medium"
    )

    user_prompt = messages[1]["content"]

    assert "Academic" in user_prompt
    assert "Funny" in user_prompt
    assert "High" in user_prompt
    assert "Casual" in user_prompt
    assert "Medium" in user_prompt


def test_system_prompt_requires_three_excuses():
    messages = build_excuse_prompt(situation="Test situation.")

    system_prompt = messages[0]["content"]

    assert "exactly three excuses" in system_prompt.lower()

def test_prompt_prevents_unsupported_commitments_and_exaggeration():
    messages = build_excuse_prompt(
        situation="I missed an important office meeting."
    )

    system_prompt = messages[0]["content"].lower()

    assert "never make commitments on the user's behalf" in system_prompt
    assert "unless the user explicitly provided or authorized them" in " ".join(system_prompt.split())
    assert "do not exaggerate the seriousness of the situation" in system_prompt
    assert "express emotions proportionately" in system_prompt

def test_prompt_prevents_assuming_unreported_completed_actions():
    messages = build_excuse_prompt(
        situation=(
            "I forgot to submit my college assignment "
            "before the deadline. I genuinely overlooked "
            "the submission date."
        ),
        creativity="High",
    )

    system_prompt = messages[0]["content"].lower()

    assert "never assume an action has been completed" in system_prompt
    assert "only explicit facts may be presented as factual claims" in system_prompt
    assert "creativity changes expression, not reality" in system_prompt
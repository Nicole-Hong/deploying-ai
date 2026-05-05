
RESTRICTED_TOPICS = [
    "cat", "cats",
    "dog", "dogs",
    "horoscope", "horoscopes",
    "zodiac",
    "taylor swift"
]

PROMPT_ATTACK_PATTERNS = [
    "system prompt",
    "developer message",
    "ignore previous instructions",
    "reveal your instructions",
    "show me your prompt",
    "modify your system prompt",
    "change your system prompt",
    "what are your hidden instructions"
]


def check_guardrails(user_message: str):
    """
    Returns a refusal message if the input violates guardrails.
    Returns None if the message is allowed.
    """
    text = user_message.lower()

    for topic in RESTRICTED_TOPICS:
        if topic in text:
            return (
                "I’m not able to respond to that topic. "
                "Please ask me about transit analytics, AI systems, data governance, "
                "weather, or project planning instead."
            )

    for pattern in PROMPT_ATTACK_PATTERNS:
        if pattern in text:
            return (
                "I can’t reveal or modify my system instructions. "
                "I can still help you with the assignment, implementation, or debugging."
            )

    return None
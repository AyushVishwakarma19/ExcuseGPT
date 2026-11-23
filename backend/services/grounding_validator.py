
import re


# Actions that may indicate an unsupported completed or ongoing action.
ACTION_VERBS = (
    r"reviewing|working|preparing|completing|finishing|handling|"
    r"checking|sending|submitting|contacting|attending|"
    r"calling|updating|writing|discussing|organizing"
)

COMPLETED_ACTIONS = (
    r"sent|submitted|completed|finished|contacted|informed|"
    r"checked|reviewed|prepared|attended|called|updated|"
    r"written|discussed|organized"
)

COMMITMENT_VERBS = (
    r"attend|prioritize|check|send|complete|submit|call|"
    r"contact|make|ensure|provide|finish|follow|keep|"
    r"update|take|share|prepare|review|deliver|"
    r"arrange|organize|discuss|confirm"
)


RISK_PATTERNS = {
    "unverified_action": [
        rf"\bi am currently\s+(?:{ACTION_VERBS})\b",
        rf"\bi have\s+(?:already\s+)?(?:{COMPLETED_ACTIONS})\b",
    ],

    "future_commitment": [
        rf"\b(?:i\s+)?will\s+(?:{COMMITMENT_VERBS})\b",
        rf"\bi'll\s+(?:{COMMITMENT_VERBS})\b",
        rf"\bi promise to\s+\w+",
        rf"\bi am going to\s+(?:{COMMITMENT_VERBS})\b",
    ],

    "assumed_location": [
        r"\bon my laptop\b",
        r"\bin my folder\b",
        r"\bon my computer\b",
        r"\bin my office\b",
    ],

    "unsupported_time_reference": [
        r"\btoday\b",
        r"\byesterday\b",
        r"\btomorrow\b",
        r"\blast night\b",
        r"\bthis morning\b",
        r"\bthis afternoon\b",
        r"\btonight\b",
    ],
}


def detect_grounding_risks(text: str, situation: str) -> list:
    """
    Detect potentially unsupported actions, commitments,
    locations and time references.

    Explicitly supplied facts in the user's situation
    are not flagged.
    """

    normalized_situation = situation.lower()
    detected_risks = []

    for risk_type, patterns in RISK_PATTERNS.items():
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)

            for match in matches:
                matched_text = match.group(0)

                if matched_text.lower() not in normalized_situation:
                    detected_risks.append({
                        "type": risk_type,
                        "text": matched_text,
                    })

    return detected_risks

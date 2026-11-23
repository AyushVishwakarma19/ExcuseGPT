from backend.services.grounding_validator import detect_grounding_risks


def test_detects_unsupported_current_action():
    risks = detect_grounding_risks(
        text="I am currently reviewing the meeting notes.",
        situation="I missed an office meeting."
    )

    assert any(
        risk["type"] == "unverified_action"
        for risk in risks
    )


def test_detects_future_commitment():
    risks = detect_grounding_risks(
        text="I will attend every future meeting.",
        situation="I missed an office meeting."
    )

    assert any(
        risk["type"] == "future_commitment"
        for risk in risks
    )


def test_detects_assumed_location():
    risks = detect_grounding_risks(
        text="My assignment is sitting on my laptop.",
        situation="I forgot to submit my assignment."
    )

    assert any(
        risk["type"] == "assumed_location"
        for risk in risks
    )


def test_does_not_flag_creative_expression():
    risks = detect_grounding_risks(
        text="My brain took an unscheduled vacation.",
        situation="I forgot to submit my assignment."
    )

    assert risks == []


def test_does_not_flag_action_explicitly_in_situation():
    risks = detect_grounding_risks(
        text="I will attend the meeting tomorrow.",
        situation="I missed today's meeting, but I will attend tomorrow."
    )

    assert risks == []

def test_detects_unsupported_completed_action():
    risks = detect_grounding_risks(
        text="I have already sent the assignment.",
        situation="I forgot to submit my assignment."
    )
    assert any(
        risk["type"] == "unverified_action"
        for risk in risks
    )


def test_does_not_flag_known_fact_without_risk_phrase():
    risks = detect_grounding_risks(
        text="I forgot to submit the assignment.",
        situation="I forgot to submit my assignment."
    )
    assert risks == []


def test_detects_unsupported_location_variant():
    risks = detect_grounding_risks(
        text="The document is on my computer.",
        situation="I forgot to submit the report."
    )
    assert any(
        risk["type"] == "assumed_location"
        for risk in risks
    )

def test_detects_commitment_without_explicit_subject():
    risks = detect_grounding_risks(
        text="I missed the meeting and will prioritize checking for updates.",
        situation="I missed an important office meeting."
    )
    assert any(
        risk["type"] == "future_commitment"
        for risk in risks
    )


def test_detects_unsupported_time_reference():
    risks = detect_grounding_risks(
        text="I missed the office meeting today.",
        situation="I missed an important office meeting."
    )
    assert any(
        risk["type"] == "unsupported_time_reference"
        for risk in risks
    )


def test_allows_time_reference_provided_by_user():
    risks = detect_grounding_risks(
        text="I missed the office meeting today.",
        situation="I missed an important office meeting today."
    )
    assert not any(
        risk["type"] == "unsupported_time_reference"
        for risk in risks
    )
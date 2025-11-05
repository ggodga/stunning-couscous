from fastapi import HTTPException
from src import app as application


def test_get_activities():
    data = application.get_activities()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_unregister_flow():
    activity = "Chess Club"
    email = "testuser@example.com"

    participants = application.activities[activity]["participants"]
    # ensure clean state
    if email in participants:
        participants.remove(email)

    before = len(participants)

    # signup should succeed
    res = application.signup_for_activity(activity, email)
    assert isinstance(res, dict)
    assert email in participants
    assert len(participants) == before + 1

    # duplicate signup should raise HTTPException with status 400
    try:
        application.signup_for_activity(activity, email)
        assert False, "Expected HTTPException for duplicate signup"
    except HTTPException as e:
        assert e.status_code == 400

    # unregister should succeed
    res = application.unregister_from_activity(activity, email)
    assert isinstance(res, dict)
    assert email not in participants
    assert len(participants) == before

    # unregister again -> 404
    try:
        application.unregister_from_activity(activity, email)
        assert False, "Expected HTTPException for removing non-existent participant"
    except HTTPException as e:
        assert e.status_code == 404


def test_activity_not_found():
    import pytest

    with pytest.raises(HTTPException) as exc:
        application.signup_for_activity("NoSuchActivity", "a@b.com")
    assert exc.value.status_code == 404

    with pytest.raises(HTTPException) as exc2:
        application.unregister_from_activity("NoSuchActivity", "a@b.com")
    assert exc2.value.status_code == 404

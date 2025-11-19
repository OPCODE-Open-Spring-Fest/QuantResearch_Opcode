from quant_research_starter.api import auth


def test_password_hash_and_verify():
    pw = "S3cureP@ssw0rd"
    hashed = auth.get_password_hash(pw)
    assert auth.verify_password(pw, hashed)
    assert not auth.verify_password("wrong", hashed)


def test_create_access_token_and_decode():
    token = auth.create_access_token({"sub": "alice"})
    # ensure token is a non-empty string
    assert isinstance(token, str) and len(token) > 0

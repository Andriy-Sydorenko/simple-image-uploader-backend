from api.models import BlackListedToken


def add_token_to_blacklisted(token, db):
    blacklisted_token = BlackListedToken(token=token)
    db.add(blacklisted_token)
    db.commit()

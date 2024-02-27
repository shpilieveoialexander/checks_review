from service.core import settings


def is_test_session(session) -> bool:
    """Check DB session"""
    uri = session.session_factory.__dict__["kw"]["bind"].url
    current_db = uri.__str__().split("/")[-1]
    return current_db == settings.PSQL_TEST_DB_NAME

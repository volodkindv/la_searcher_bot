def test_real_db_is_enabled(use_real_db: bool):
    """
    remember turn on using real db if it was temporarily disabled for speed up tests
    """
    assert use_real_db

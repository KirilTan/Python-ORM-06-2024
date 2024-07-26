def session_decorator(session, autoclose_session=True):
    """
    A decorator to manage database session lifecycle for a function.

    This decorator ensures that the session is committed if the function
    executes successfully, and rolled back if an exception occurs. Optionally,
    it can also close the session after the function execution.

    Parameters:
        session (Session): The database session to be managed.
        autoclose_session (bool): If True, the session will be closed after the function
                                  execution. Default is True.

    Returns:
        function: The decorated function with session management.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                session.commit()

                return result

            except Exception as e:
                session.rollback()
                raise e

            finally:
                if autoclose_session:
                    session.close()

        return wrapper
    return decorator

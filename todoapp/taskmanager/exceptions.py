"""Exceptions for taskmanager app."""


class UnauthorizedUsername(Exception):
    """Request method is unauthorized."""

    def __init__(self):
        """Initial values."""
        self.message = 'Unauthorized Username.'
        self.code = 'u-1'
        self.status_code = 401

    def __str__(self):
        """Object returning."""
        return self.message


class UnauthorizedPassword(Exception):
    """Request method is unauthorized."""

    def __init__(self):
        """Initial values."""
        self.message = 'Password is invalid.'
        self.code = 'u-2'
        self.status_code = 401

    def __str__(self):
        """Object returning."""
        return self.message


class UserNotActive(Exception):
    """Request method is forbidden."""

    def __init__(self):
        """Initial values."""
        self.message = 'User Not Active.'
        self.code = 'u-3'
        self.status_code = 403

    def __str__(self):
        """Object returning."""
        return self.message


class InvalidUserParameters(Exception):
    """Request method is invalid."""

    def __init__(self):
        """Initial values."""
        self.message = 'Invalid User Parameters.'
        self.code = 'u-4'
        self.status_code = 400

    def __str__(self):
        """Object returning."""
        return self.message


class UsernameExists(Exception):
    """Request method is conflict."""

    def __init__(self):
        """Initial values."""
        self.message = 'Username Exists.'
        self.code = 'u-5'
        self.status_code = 409

    def __str__(self):
        """Object returning."""
        return self.message


class UnauthorizedUser(Exception):
    """Request method is iunauthorized."""

    def __init__(self):
        """Initial values."""
        self.message = 'Unauthorized User.'
        self.code = 'u-6'
        self.status_code = 401

    def __str__(self):
        """Object returning."""
        return self.message


class InvalidTaskParameters(Exception):
    """Request method is invalid."""

    def __init__(self):
        """Initial values."""
        self.message = 'Invalid Task Parameters.'
        self.code = 't-1'
        self.status_code = 400

    def __str__(self):
        """Object returning."""
        return self.message


class InvalidSubTaskParameters(Exception):
    """Request method is invalid."""

    def __init__(self):
        """Initial values."""
        self.message = 'Invalid SubTask Parameters.'
        self.code = 't-2'
        self.status_code = 400

    def __str__(self):
        """Object returning."""
        return self.message


class InvalidDueDate(Exception):
    """Request method is invalid."""

    def __init__(self):
        """Initial values."""
        self.message = 'Invalid Due date.'
        self.code = 't-3'
        self.status_code = 400

    def __str__(self):
        """Object returning."""
        return self.message

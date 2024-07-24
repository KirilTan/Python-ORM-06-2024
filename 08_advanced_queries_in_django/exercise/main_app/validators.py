from django.core.exceptions import ValidationError


class RangeValueValidator:
    """
    A validator that checks if a given value falls within a specified range.

    Attributes:
        min_value (int): The minimum allowable value.
        max_value (int): The maximum allowable value.
        message (str): The error message to be displayed if validation fails.
    """

    def __init__(self, min_value: int, max_value: int, message=None):
        """
        Initializes the RangeValueValidator with a minimum value, maximum value, and an optional custom message.

        Args:
            min_value (int): The minimum allowable value.
            max_value (int): The maximum allowable value.
            message (str, optional): The error message to be displayed if validation fails. Defaults to None.
        """
        self.min_value = min_value
        self.max_value = max_value
        self.message = message

    @property
    def message(self):
        """
        Gets the current error message.

        Returns:
            str: The current error message.
        """
        return self.__message

    @message.setter
    def message(self, value):
        """
        Sets the error message. If no message is provided, a default message is generated.

        Args:
            value (str): The error message to be set. If None, a default message is generated.
        """
        if value is None:
            self.__message = f"The rating must be between {self.min_value:.1f} and {self.max_value:.1f}"
        else:
            self.__message = value

    def __call__(self, value: int):
        """
        Validates that the given value falls within the specified range.

        Args:
            value (int): The value to be validated.

        Raises:
            ValidationError: If the value is not within the specified range.
        """
        if not self.min_value <= value <= self.max_value:
            raise ValidationError(self.message)

    def deconstruct(self):
        """
        Deconstructs the validator into a serializable format.

        Returns:
            tuple: A tuple containing the path to the validator class, a list of positional arguments, and a dictionary of keyword arguments.
        """
        return (
            'main_app.validators.RangeValueValidator',
            [self.min_value, self.max_value],
            {'message': self.message},
        )
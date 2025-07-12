class Cell:
    """
    A class representing a cell in a Sudoku grid.

    Attributes:
        value (int | None): The value of the cell.
        candidates (set): A set of possible candidates for the cell's value.
    """

    def __init__(self, value: int | None = None):
        """
        Initializes a Cell instance.

        Args:
            value (int | None): The initial value of the cell. Defaults to None.
        """
        self._value: int | None = None
        self._candidates = set(range(1, 10))
        self.value = value

    @property
    def value(self) -> int | None:
        """
        Returns the value of the cell.

        Returns:
            int | None: The value of the cell.
        """
        return self._value

    @value.setter
    def value(self, value: int | None):
        """
        Sets the value of the cell unless it already has a value.

        Args:
            value (int): The new value for the cell.
        """
        if self._value is not None:
            raise ValueError("Cannot set value of a cell that already has a value.")
        if value is not None and not (1 <= value <= 9):
            raise ValueError("Value must be between 1 and 9.")

        self._value = value
        if value is not None:
            self._candidates.clear()

    @property
    def candidates(self) -> set:
        """
        Returns the set of candidates for the cell.
        Note that modifying the returned set will not affect the cell's candidates.

        Returns:
            set: The set of candidates for the cell.
        """
        return self._candidates.copy()

    @candidates.setter
    def candidates(self, candidates: set):
        """
        Sets the candidates for the cell.

        Args:
            candidates (set): The new set of candidates for the cell.
        """
        if self._value is not None:
            raise ValueError(
                "Cannot set candidates for a cell that already has a value."
            )
        if not all(1 <= candidate <= 9 for candidate in candidates):
            raise ValueError("All candidates must be between 1 and 9.")

        self._candidates = set(candidates)

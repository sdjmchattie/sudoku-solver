from model.point import Point


class Cell:
    """
    A class representing a cell in a Sudoku grid.

    Attributes:
        value (int | None): The value of the cell.
        candidates (set): A set of possible candidates for the cell's value.
    """

    def __init__(
        self,
        coord: Point,
        block: Point,
        coord_in_block: Point,
        value: int | None = None,
    ):
        """
        Initializes a Cell instance.

        Args:
            coord (Point): The coordinates of the cell in the grid.
            block (Point): The coordinates of the cell's 3x3 block.
            coord_in_block (Point): The coordinates of the cell within its 3x3 block.
            value (int | None): The initial value of the cell. Defaults to None.
        """
        self._coord = coord
        self._block = block
        self._coord_in_block = coord_in_block
        self._value: int | None = None
        self._candidates = set(range(1, 10))
        self.value = value

    @property
    def coord(self) -> Point:
        """
        Returns the coordinates of the cell in the grid.

        Returns:
            Point: The coordinates of the cell relative to the global grid.
        """
        return self._coord

    @property
    def block(self) -> Point:
        """
        Returns the coordinates of the cell's 3x3 block.

        Returns:
            Point: The coordinates of the cell's block relative to the global grid.
        """
        return self._block

    @property
    def coord_in_block(self) -> Point:
        """
        Returns the coordinates of the cell within its 3x3 block.

        Returns:
            Point: The coordinates of the cell within its block.
        """
        return self._coord_in_block

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
    def candidates(self) -> set[int]:
        """
        Returns the set of candidates for the cell.
        Note that modifying the returned set will not affect the cell's candidates.

        Returns:
            set: The set of candidates for the cell.
        """
        return self._candidates.copy()

    @candidates.setter
    def candidates(self, candidates: set[int]):
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

import enum


class BraceStyle(enum.Enum):
    COLLAPSE = enum.auto()
    EXPAND = enum.auto()
    END_EXPAND = enum.auto()


class Settings:
    def __init__(self) -> None:
        self._brace_style = BraceStyle.EXPAND

    @property
    def brace_style(self) -> BraceStyle:
        """Sets the style of braces around code blocks.

        Values:
            COLLAPSE: Put braces on the same line as the control statement.
                ```
                if () {
                } else if () {
                }
                ```
            EXPAND: Put both braces on their own line.
                ```
                if ()
                {
                }
                else if()
                {
                }
                ```
            END_EXPAND: Put the starting brace on the same line as the control statement, and the ending brace on its own line.
                ```
                if () {
                }
                else if () {
                }
                ```
        """
        return self._brace_style

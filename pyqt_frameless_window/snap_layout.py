from enum import Enum


class SnapState(Enum):
    HIDDEN = 0
    NORMAL = 1
    MAXIMIZED = 2
    LEFT = 3
    RIGHT = 4
    TOP_LEFT = 5
    TOP_RIGHT = 6
    BOTTOM_LEFT = 7
    BOTTOM_RIGHT = 8


class ButtonKey(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


snap_states: dict[tuple[SnapState, ButtonKey], SnapState] = {
    (SnapState.HIDDEN, ButtonKey.UP): SnapState.NORMAL,
    (SnapState.NORMAL, ButtonKey.UP): SnapState.MAXIMIZED,
    (SnapState.NORMAL, ButtonKey.DOWN): SnapState.HIDDEN,
    (SnapState.NORMAL, ButtonKey.LEFT): SnapState.LEFT,
    (SnapState.NORMAL, ButtonKey.RIGHT): SnapState.RIGHT,
    (SnapState.MAXIMIZED, ButtonKey.DOWN): SnapState.NORMAL,
    (SnapState.MAXIMIZED, ButtonKey.LEFT): SnapState.LEFT,
    (SnapState.MAXIMIZED, ButtonKey.RIGHT): SnapState.RIGHT,
    (SnapState.LEFT, ButtonKey.DOWN): SnapState.BOTTOM_LEFT,
    (SnapState.LEFT, ButtonKey.UP): SnapState.TOP_LEFT,
    (SnapState.LEFT, ButtonKey.RIGHT): SnapState.NORMAL,
    (SnapState.LEFT, ButtonKey.LEFT): SnapState.RIGHT,  # next screen
    (SnapState.RIGHT, ButtonKey.DOWN): SnapState.BOTTOM_RIGHT,
    (SnapState.RIGHT, ButtonKey.UP): SnapState.TOP_RIGHT,
    (SnapState.RIGHT, ButtonKey.LEFT): SnapState.NORMAL,
    (SnapState.RIGHT, ButtonKey.RIGHT): SnapState.LEFT,  # next screen
    (SnapState.TOP_LEFT, ButtonKey.UP): SnapState.MAXIMIZED,
    (SnapState.TOP_LEFT, ButtonKey.DOWN): SnapState.LEFT,
    (SnapState.TOP_LEFT, ButtonKey.RIGHT): SnapState.TOP_RIGHT,
    (SnapState.TOP_LEFT, ButtonKey.LEFT): SnapState.TOP_RIGHT,  # next scren
    (SnapState.TOP_RIGHT, ButtonKey.UP): SnapState.MAXIMIZED,
    (SnapState.TOP_RIGHT, ButtonKey.DOWN): SnapState.RIGHT,
    (SnapState.TOP_RIGHT, ButtonKey.LEFT): SnapState.TOP_LEFT,
    (SnapState.TOP_RIGHT, ButtonKey.RIGHT): SnapState.TOP_LEFT,  # next scren
    (SnapState.BOTTOM_LEFT, ButtonKey.UP): SnapState.LEFT,
    (SnapState.BOTTOM_LEFT, ButtonKey.DOWN): SnapState.HIDDEN,
    (SnapState.BOTTOM_LEFT, ButtonKey.RIGHT): SnapState.BOTTOM_RIGHT,
    (SnapState.BOTTOM_LEFT, ButtonKey.LEFT): SnapState.BOTTOM_RIGHT,  # next scren
    (SnapState.BOTTOM_RIGHT, ButtonKey.UP): SnapState.RIGHT,
    (SnapState.BOTTOM_RIGHT, ButtonKey.DOWN): SnapState.HIDDEN,
    (SnapState.BOTTOM_RIGHT, ButtonKey.RIGHT): SnapState.BOTTOM_LEFT,
    (SnapState.BOTTOM_RIGHT, ButtonKey.LEFT): SnapState.BOTTOM_LEFT,  # next scren
}

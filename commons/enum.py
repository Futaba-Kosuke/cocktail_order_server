from typing import Literal, Tuple

UnitType = Literal["ml", "tea_spoon", "dash", "drop", "slice", "any"]
MethodType = Literal["stir", "shake", "build"]
StyleType = Literal["short", "long"]
OrderStatusType = Literal["processing", "calling", "complete"]

unit_enum: Tuple[UnitType, ...] = (
    "ml",
    "tea_spoon",
    "dash",
    "drop",
    "slice",
    "any",
)
method_enum: Tuple[MethodType, ...] = ("stir", "shake", "build")
style_enum: Tuple[StyleType, ...] = ("short", "long")
order_status_enum: Tuple[OrderStatusType, ...] = (
    "processing",
    "calling",
    "complete",
)

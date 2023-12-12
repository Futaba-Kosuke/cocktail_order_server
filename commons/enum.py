from typing import Literal

unit_enum = ("ml", "tea_spoon", "dash", "drop", "slice")
method_enum = ("stir", "shake", "build")
style_enum = ("short", "long")
order_status_enum = ("processing", "calling", "already")

UnitType = Literal["ml", "tea_spoon", "dash", "drop", "slice"]
MethodType = Literal["stir", "shake", "build"]
StyleType = Literal["short", "long"]
OrderStatusType = Literal["processing", "calling", "already"]

# %%
import math
from build123d import *
from build123d.build_common import *
from build123d.objects_part import *
from ocp_vscode import *
from gridfinity_build123d import *
from dataclasses import dataclass
import modal

app = modal.App("wrench_organizer")

dockerfile_image = modal.Image.from_dockerfile("Dockerfile")

# %%


global_wrench_width = 20
wrench_above_top_ratio = 0.25

wrench_x_min_padding = 5
wrench_y_min_padding = 15


@dataclass
class WrenchSpec:
    label: str
    total_length: float
    body_length: float
    head_width: float
    body_width: float

    def total_slot_length(self) -> float:
        return self.total_length + 10


def bin_width_units(num_wrenches: int):
    minimum_width = (global_wrench_width * num_wrenches) + (
        (num_wrenches + 1) * wrench_x_min_padding
    )
    return math.ceil(minimum_width / 42.0)


@dataclass
class WrenchPlacement:
    wrenches: list[WrenchSpec]
    bin_width_units: int
    bin_height_units: int

    def num_wrenches(self) -> int:
        return len(self.wrenches)

    def bin_width_mm(self) -> int:
        return self.bin_width_units * 42

    def bin_height_mm(self) -> int:
        return self.bin_height_units * 42

    def wrench_x_padding(self) -> float:
        return (self.bin_width_mm() - global_wrench_width * self.num_wrenches()) / (
            (self.num_wrenches()) + 1
        )

    def x_start_pos(self, idx: int) -> float:
        return (
            (-self.bin_width_mm() / 2)
            + (global_wrench_width * idx)
            + ((idx + 1) * self.wrench_x_padding())
        )

    def y_start_pos(self, idx: int) -> float:
        return (
            (-self.bin_height_mm() / 2)
            + wrench_y_min_padding
            + (self.wrenches[idx].total_slot_length() / 2.0)
        )


class Wrench(BasePartObject):
    def __init__(
        self,
        spec: WrenchSpec,
        mode: Mode,
    ):
        with BuildPart() as wrench:
            with BuildSketch() as full_wrench_sketch:
                Rectangle(
                    width=global_wrench_width,
                    height=spec.total_slot_length(),
                    align=(Align.MIN, Align.CENTER),
                )
            head_extrude_amount = (1 - wrench_above_top_ratio) * spec.head_width
            extrude(
                to_extrude=full_wrench_sketch.sketch, amount=-1 * head_extrude_amount
            )

            with BuildSketch() as body_sides_sketch:
                Rectangle(
                    width=global_wrench_width,
                    height=spec.body_length,
                    align=(Align.MIN, Align.CENTER),
                )
                with Locations(((global_wrench_width - spec.body_width) / 2, 0)):
                    Rectangle(
                        width=spec.body_width,
                        height=spec.body_length,
                        align=(Align.MIN, Align.CENTER),
                        mode=Mode.SUBTRACT,
                    )
            extrude(
                to_extrude=body_sides_sketch.sketch,
                amount=-head_extrude_amount,
                mode=Mode.SUBTRACT,
            )

            body_extrude_amount = head_extrude_amount / 2.0
            # with Locations((0, 0, -body_extrude_amount)):
            with Locations(
                (
                    (global_wrench_width - spec.body_width) / 2,
                    0,
                    -body_extrude_amount,
                )
            ):
                with BuildSketch() as body_bottom_sketch:
                    Rectangle(
                        width=spec.body_width,
                        height=spec.body_length,
                        align=(Align.MIN, Align.CENTER),
                    )
                extrude(
                    to_extrude=body_bottom_sketch.sketch,
                    amount=body_extrude_amount,
                    mode=Mode.SUBTRACT,
                )

        # chamfer(objects=wrench.edges(), length=1)
        super().__init__(part=wrench.part, mode=mode)


# blah @app.function(image=dockerfile_image)

# TODO: DELETE
XXXX = 260

wrenches: list[list[WrenchSpec]] = [
    # [
    #     WrenchSpec(
    #         '1/4"', total_length=132, body_length=95, head_width=15, body_width=3.5
    #     ),
    #     WrenchSpec(
    #         '5/16"', total_length=150, body_length=105, head_width=19, body_width=4.0
    #     ),
    #     WrenchSpec(
    #         '11/32"', total_length=162, body_length=115, head_width=19, body_width=4.0
    #     ),
    #     WrenchSpec(
    #         '3/8"', total_length=170, body_length=125, head_width=21, body_width=4.0
    #     ),
    #     # WrenchSpec(
    #     #     '7/16"', total_length=186, body_length=135, head_width=25, body_width=5
    #     # ),
    #     # WrenchSpec(
    #     #     '1/2"', total_length=208, body_length=150, head_width=28, body_width=5.5
    #     # ),
    #     # WrenchSpec(
    #     #     '9/16"', total_length=226, body_length=165, head_width=31, body_width=5.5
    #     # ),
    #     # WrenchSpec(
    #     #     '5/8"', total_length=244, body_length=175, head_width=36, body_width=6
    #     # ),
    #     # WrenchSpec(
    #     #     '11/16"', total_length=263, body_length=190, head_width=38, body_width=6
    #     # ),
    #     # WrenchSpec(
    #     #     '3/4"', total_length=280, body_length=195, head_width=42, body_width=7
    #     # ),
    #     # WrenchSpec(
    #     #     '13/16"', total_length=302, body_length=210, head_width=46, body_width=7
    #     # ),
    #     # WrenchSpec(
    #     #     '7/8"', total_length=XXXX, body_length=225, head_width=48, body_width=7.5
    #     # ),
    #     # WrenchSpec(
    #     #     '15/16"', total_length=XXXX, body_length=235, head_width=52, body_width=8
    #     # ),
    #     # WrenchSpec(
    #     #     '1"', total_length=XXXX, body_length=250, head_width=55, body_width=9
    #     # ),
    # ],
    [
        ###################################
        ####### METRIC
        ###################################
        WrenchSpec(
            "6MM", total_length=132, body_length=95, head_width=15, body_width=3.5
        ),
        WrenchSpec(
            "7MM", total_length=136, body_length=100, head_width=17, body_width=4
        ),
        WrenchSpec(
            "8MM", total_length=150, body_length=110, head_width=18.5, body_width=4
        ),
        WrenchSpec(
            "9MM", total_length=160, body_length=120, head_width=19, body_width=4
        ),
        WrenchSpec(
            "10MM", total_length=175, body_length=125, head_width=22, body_width=4.5
        ),
        WrenchSpec(
            "11MM", total_length=188, body_length=132, head_width=25, body_width=5
        ),
        WrenchSpec(
            "12MM", total_length=198, body_length=140, head_width=27, body_width=5
        ),
        WrenchSpec(
            "13MM", total_length=210, body_length=150, head_width=28, body_width=5
        ),
        WrenchSpec(
            "14MM", total_length=225, body_length=160, head_width=31, body_width=5.5
        ),
        WrenchSpec(
            "15MM", total_length=235, body_length=165, head_width=33, body_width=5.5
        ),
        WrenchSpec(
            "16MM", total_length=245, body_length=170, head_width=35, body_width=5.5
        ),
        WrenchSpec(
            "17MM", total_length=265, body_length=175, head_width=35, body_width=6
        ),
        WrenchSpec(
            "18MM", total_length=273, body_length=190, head_width=40, body_width=6.5
        ),
        WrenchSpec(
            "19MM", total_length=281, body_length=195, head_width=42, body_width=6.5
        ),
    ],
]


max_wrenches_width = max([len(wrenches) for wrenches in wrenches])
grid_x = bin_width_units(num_wrenches=max_wrenches_width)
grid_y = 8

# %%

bin = Bin(
    BaseEqual(
        grid_x=grid_x,
        grid_y=grid_y,
        #   features=[MagnetHole(BottomCorners())]
    ),
    height_in_units=9,
    # lip=StackingLip(),
    # compartments=CompartmentsEqual(compartment_list=[Compartment()]),
)

# %%


class Wrench(BasePartObject):
    def __init__(
        self,
        spec: WrenchSpec,
        mode: Mode,
    ):
        with BuildPart() as wrench:
            with BuildSketch() as full_wrench_sketch:
                Rectangle(
                    width=global_wrench_width,
                    height=spec.total_slot_length(),
                    align=(Align.MIN, Align.CENTER),
                )
            head_extrude_amount = (1 - wrench_above_top_ratio) * spec.head_width
            extrude(
                to_extrude=full_wrench_sketch.sketch, amount=-1 * head_extrude_amount
            )

            with BuildSketch() as body_sides_sketch:
                Rectangle(
                    width=global_wrench_width,
                    height=spec.body_length,
                    align=(Align.MIN, Align.CENTER),
                )
                with Locations(((global_wrench_width - spec.body_width) / 2, 0)):
                    Rectangle(
                        width=spec.body_width,
                        height=spec.body_length,
                        align=(Align.MIN, Align.CENTER),
                        mode=Mode.SUBTRACT,
                    )
            extrude(
                to_extrude=body_sides_sketch.sketch,
                amount=-head_extrude_amount,
                mode=Mode.SUBTRACT,
            )

            with BuildSketch(
                Location((0, 0, -head_extrude_amount / 2.0))
            ) as body_bottom_sketch:
                with Locations(
                    (
                        (global_wrench_width - spec.body_width) / 2,
                        0,
                    )
                ):
                    Rectangle(
                        width=spec.body_width,
                        height=spec.body_length,
                        align=(Align.MIN, Align.CENTER),
                    )
            extrude(
                to_extrude=body_bottom_sketch.sketch,
                amount=(-head_extrude_amount / 2.0),
                mode=Mode.SUBTRACT,
            )

        # chamfer(objects=wrench.edges(), length=1)
        super().__init__(part=wrench.part, mode=mode)


# def make_wrench_group(bin: Part, group_idx: int, wrenches: list[WrenchSpec]):
# with BuildPart() as part:
#     add(bin)

with BuildPart() as part:
    add(bin)
    top_face = (
        ### 3530 seconds (~60min) when find was:
        # part.faces().filter_by(GeomType.PLANE).filter_by_position(Axis.Z, 10,
        # 1000)
        bin.faces().sort_by(Axis.Z)[-1]
    )
    with Locations(top_face):
        for group_idx, wrench_group in enumerate(wrenches):
            wrench_placement = WrenchPlacement(
                wrenches=wrench_group, bin_width_units=grid_x, bin_height_units=grid_y
            )
            for wrench_idx, wrench in enumerate(wrench_group):
                with Locations(
                    (
                        wrench_placement.x_start_pos(idx=wrench_idx),
                        wrench_placement.y_start_pos(idx=wrench_idx),
                    )
                ) as location:
                    print(f"processing wrench {wrench_idx+1}")
                    Wrench(spec=wrench, mode=Mode.SUBTRACT)
                with BuildSketch(
                    Location(
                        (
                            wrench_placement.x_start_pos(idx=wrench_idx)
                            + (global_wrench_width / 2),
                            wrench_placement.y_start_pos(idx=wrench_idx)
                            - (
                                (
                                    wrench.total_slot_length()
                                    + wrench_placement.wrench_x_padding()
                                )
                                / 2
                            )
                            - 5,
                            top_face.center_location.position.Z,
                        )
                    )
                ) as label_sketch:
                    Text(
                        txt=wrench.label,
                        font_size=10,
                        font_path="./fonts/D-DINCondensed-Bold.otf",
                        font_style=FontStyle.BOLD,
                    )
                    # .rotate(0, 0, 90)
                extrude(to_extrude=label_sketch.sketch, amount=3, mode=Mode.ADD)

    chamfer(
        objects=part.faces()
        .filter_by(GeomType.PLANE)
        .filter_by_position(Axis.Z, 10, 1000)
        .edges(),
        length=1,
    )

show_all()
# %%
show(part)

# %%

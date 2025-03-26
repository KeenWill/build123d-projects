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

wrench_width_padding = 5
wrench_height_padding = 15


@dataclass
class WrenchSpec:
    label: str
    total_length: float
    body_length: float
    head_width: float
    body_width: float

    def width_start_pos(self, idx: int, bin_width_mm: int):
        return (
            (-bin_width_mm / 2)
            + (global_wrench_width * idx)
            + ((idx + 1) * wrench_width_padding)
        )

    def height_start_pos(self, bin_height_mm: int):
        return (-bin_height_mm / 2) + wrench_height_padding + (self.total_length / 2.0)


def bin_width_units(num_wrenches: int):
    minimum_width = (global_wrench_width * num_wrenches) + (
        (num_wrenches + 1) * wrench_width_padding
    )
    return math.ceil(minimum_width / 42.0)


# def bin_height_units


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
                    height=spec.total_length,
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
                    amount=-body_extrude_amount,
                    mode=Mode.SUBTRACT,
                )

        # chamfer(objects=wrench.edges(), length=1)
        super().__init__(part=wrench.part, mode=mode)


# blah @app.function(image=dockerfile_image)

# TODO: DELETE
XXXX = 260

wrenches = [
    WrenchSpec('1/4"', total_length=132, body_length=95, head_width=15, body_width=3.5),
    WrenchSpec(
        '5/16"', total_length=150, body_length=105, head_width=19, body_width=4.0
    ),
    WrenchSpec(
        '11/32"', total_length=162, body_length=115, head_width=19, body_width=4.0
    ),
    WrenchSpec(
        '3/8"', total_length=170, body_length=125, head_width=21, body_width=4.0
    ),
    WrenchSpec('7/16"', total_length=186, body_length=135, head_width=25, body_width=5),
    WrenchSpec(
        '1/2"', total_length=208, body_length=150, head_width=28, body_width=5.5
    ),
    WrenchSpec(
        '9/16"', total_length=226, body_length=165, head_width=31, body_width=5.5
    ),
    WrenchSpec('5/8"', total_length=244, body_length=175, head_width=36, body_width=6),
    WrenchSpec(
        '11/16"', total_length=263, body_length=190, head_width=38, body_width=6
    ),
    WrenchSpec('3/4"', total_length=280, body_length=195, head_width=42, body_width=7),
    WrenchSpec(
        '13/16"', total_length=302, body_length=210, head_width=46, body_width=7
    ),
    WrenchSpec(
        '7/8"', total_length=XXXX, body_length=225, head_width=48, body_width=7.5
    ),
    WrenchSpec(
        '15/16"', total_length=XXXX, body_length=235, head_width=52, body_width=8
    ),
    WrenchSpec('1"', total_length=XXXX, body_length=250, head_width=55, body_width=9),
    ###################################
    ####### METRIC
    ###################################
    WrenchSpec("6mm", total_length=132, body_length=95, head_width=15, body_width=3.5),
    WrenchSpec("7mm", total_length=136, body_length=100, head_width=17, body_width=4),
    WrenchSpec("8mm", total_length=150, body_length=110, head_width=18.5, body_width=4),
    WrenchSpec("9mm", total_length=160, body_length=120, head_width=19, body_width=4),
    WrenchSpec(
        "10mm", total_length=175, body_length=125, head_width=22, body_width=4.5
    ),
    WrenchSpec("11mm", total_length=188, body_length=132, head_width=25, body_width=5),
    WrenchSpec("12mm", total_length=198, body_length=140, head_width=27, body_width=5),
    WrenchSpec("13mm", total_length=210, body_length=150, head_width=28, body_width=5),
    WrenchSpec(
        "14mm", total_length=225, body_length=160, head_width=31, body_width=5.5
    ),
    WrenchSpec(
        "15mm", total_length=235, body_length=165, head_width=33, body_width=5.5
    ),
    WrenchSpec(
        "16mm", total_length=245, body_length=170, head_width=35, body_width=5.5
    ),
    WrenchSpec("17mm", total_length=265, body_length=XXXX, head_width=35, body_width=6),
    WrenchSpec(
        "18mm", total_length=273, body_length=190, head_width=40, body_width=6.5
    ),
    WrenchSpec(
        "19mm", total_length=281, body_length=195, head_width=42, body_width=6.5
    ),
]

grid_x = bin_width_units(num_wrenches=len(wrenches))
grid_y = 8

with BuildPart() as part:
    Bin(
        BaseEqual(grid_x=grid_x, grid_y=grid_y, features=[MagnetHole(BottomCorners())]),
        height_in_units=9,
        # lip=StackingLip(),
        # compartments=CompartmentsEqual(compartment_list=[Compartment()]),
    )

    top_face = (
        part.faces().filter_by(GeomType.PLANE).filter_by_position(Axis.Z, 10, 1000)
    )

    with Locations(top_face):
        for idx, wrench in enumerate(wrenches):
            with Locations(
                (
                    wrench.width_start_pos(idx=idx, bin_width_mm=grid_x * 42),
                    wrench.height_start_pos(bin_height_mm=grid_y * 42),
                )
            ) as location:
                Wrench(spec=wrench, mode=Mode.SUBTRACT)

    # chamfer(objects=part.faces().filter_by(GeomType.PLANE).filter_by_position(Axis.Z, 10, 1000).edges(), length=1)


show_all()
# %%

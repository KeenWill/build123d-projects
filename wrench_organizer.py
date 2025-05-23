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


wrench_above_top_ratio = 0.5

# wrench_x_min_padding = 0
min_x_center_to_center_spacing = 24
wrench_y_min_gap = 35
wrench_x_margin = 10


@dataclass
class WrenchSpec:
    label: str
    total_length: float
    body_length: float
    head_width: float
    body_width: float

    def total_slot_length(self) -> float:
        return self.total_length + 10

    def extrusion_depth(self) -> float:
        return (1 - wrench_above_top_ratio) * self.head_width


def bin_width_units(num_wrenches: int):
    minimum_width = min_x_center_to_center_spacing * num_wrenches + 2 * wrench_x_margin
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

    def wrench_width(self) -> float:
        return (self.bin_width_mm() - (2 * wrench_x_margin)) / self.num_wrenches()

    def wrench_x_center_to_center_spacing(self) -> float:
        return (
            self.bin_width_mm() - (min_x_center_to_center_spacing * self.num_wrenches())
        ) / (self.num_wrenches() + 1)

    def x_start_pos(self, idx: int) -> float:
        return (
            (-self.bin_width_mm() / 2) + wrench_x_margin + (self.wrench_width() * idx)
        )

    def y_start_pos(self, idx: int) -> float:
        return (
            (-self.bin_height_mm() / 2)
            + wrench_y_min_gap
            + (self.wrenches[idx].total_slot_length() / 2.0)
        )


imperial: list[WrenchSpec] = [
    WrenchSpec('1/4"', total_length=132, body_length=95, head_width=17, body_width=4.0),
    WrenchSpec(
        '5/16"', total_length=150, body_length=105, head_width=21, body_width=4.5
    ),
    WrenchSpec(
        '11/32"', total_length=162, body_length=115, head_width=21, body_width=5.0
    ),
    WrenchSpec(
        '3/8"', total_length=170, body_length=125, head_width=23, body_width=5.0
    ),
    WrenchSpec(
        '7/16"', total_length=186, body_length=135, head_width=27, body_width=5.5
    ),
    WrenchSpec(
        '1/2"', total_length=208, body_length=150, head_width=30, body_width=6.0
    ),
    WrenchSpec(
        '9/16"', total_length=226, body_length=165, head_width=33, body_width=6.8
    ),
    WrenchSpec(
        '5/8"', total_length=244, body_length=175, head_width=38, body_width=6.5
    ),
    WrenchSpec(
        '11/16"', total_length=263, body_length=190, head_width=40, body_width=6.5
    ),
    WrenchSpec(
        '3/4"', total_length=280, body_length=195, head_width=44, body_width=7.5
    ),
    WrenchSpec(
        '13/16"', total_length=302, body_length=210, head_width=50, body_width=7.5
    ),
    WrenchSpec(
        '7/8"', total_length=320, body_length=215, head_width=52, body_width=7.5
    ),
    WrenchSpec(
        '15/16"', total_length=337, body_length=235, head_width=56, body_width=8
    ),
    WrenchSpec('1"', total_length=356, body_length=250, head_width=58, body_width=9),
]
metric: list[WrenchSpec] = [
    ###################################
    ####### METRIC
    ###################################
    WrenchSpec("6MM", total_length=132, body_length=95, head_width=17, body_width=4),
    WrenchSpec("7MM", total_length=136, body_length=100, head_width=19, body_width=4.5),
    WrenchSpec("8MM", total_length=150, body_length=110, head_width=21, body_width=4.5),
    WrenchSpec("9MM", total_length=160, body_length=120, head_width=23, body_width=5.0),
    WrenchSpec(
        "10MM", total_length=175, body_length=125, head_width=24, body_width=5.0
    ),
    WrenchSpec(
        "11MM", total_length=188, body_length=132, head_width=26, body_width=5.5
    ),
    WrenchSpec(
        "12MM", total_length=198, body_length=140, head_width=28, body_width=5.5
    ),
    WrenchSpec(
        "13MM", total_length=210, body_length=150, head_width=30, body_width=5.5
    ),
    WrenchSpec(
        "14MM", total_length=225, body_length=160, head_width=33, body_width=6.0
    ),
    WrenchSpec(
        "15MM", total_length=235, body_length=165, head_width=35, body_width=6.0
    ),
    WrenchSpec(
        "16MM", total_length=245, body_length=170, head_width=38, body_width=6.0
    ),
    WrenchSpec("17MM", total_length=265, body_length=182, head_width=40, body_width=6),
    WrenchSpec(
        "18MM", total_length=273, body_length=190, head_width=43, body_width=6.5
    ),
    WrenchSpec(
        "19MM", total_length=281, body_length=195, head_width=46, body_width=6.5
    ),
]


max_wrenches_width = 14
grid_x = bin_width_units(num_wrenches=max_wrenches_width)
grid_y = 14

# %%

bin = Bin(
    BaseEqual(
        grid_x=grid_x,
        grid_y=grid_y,
        #   features=[MagnetHole(BottomCorners())]
    ),
    height_in_units=6,
    # lip=StackingLip(),
    # compartments=CompartmentsEqual(compartment_list=[Compartment()]),
)

# %%


class Wrench(BasePartObject):
    def __init__(
        self,
        spec: WrenchSpec,
        cut_width: float,
        mode: Mode,
    ):
        with BuildPart() as wrench:
            with BuildSketch() as full_wrench_sketch:
                Rectangle(
                    width=cut_width,
                    height=spec.total_slot_length(),
                    align=(Align.MIN, Align.CENTER),
                )
            head_extrude_amount = spec.extrusion_depth()
            extrude(
                to_extrude=full_wrench_sketch.sketch, amount=-1 * head_extrude_amount
            )

            with BuildSketch() as body_sides_sketch:
                Rectangle(
                    width=cut_width,
                    height=spec.body_length,
                    align=(Align.MIN, Align.CENTER),
                )
                with Locations(((cut_width - spec.body_width) / 2, 0)):
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
                        (cut_width - spec.body_width) / 2,
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
        super().__init__(part=wrench.part, mode=mode)  # type: ignore


class WrenchGroup:
    wrenches: list[WrenchSpec]
    placement: WrenchPlacement

    def __init__(self, wrenches: list[WrenchSpec]):
        self.wrenches = wrenches
        self.placement = WrenchPlacement(
            wrenches,
            bin_width_units=grid_x,
            bin_height_units=grid_y,
        )

    def wrench_slots(self):
        with BuildPart() as part:
            for wrench_idx, wrench in enumerate(self.wrenches):
                with Locations(
                    (
                        self.placement.x_start_pos(idx=wrench_idx),
                        self.placement.y_start_pos(idx=wrench_idx),
                    )
                ) as location:
                    print(f"processing wrench {wrench_idx+1}")
                    Wrench(
                        spec=wrench,
                        mode=Mode.ADD,
                        cut_width=self.placement.wrench_width(),
                    )
        return part

    def labels(self, flip: bool = False):
        with BuildPart() as part:
            with BuildSketch() as labels:
                for wrench_idx, wrench in enumerate(self.wrenches):
                    print(f"adding text for wrench {wrench_idx+1}")
                    with Locations(
                        (
                            self.placement.x_start_pos(idx=wrench_idx)
                            + (self.placement.wrench_width() / 2),
                            self.placement.y_start_pos(idx=wrench_idx)
                            - ((wrench.total_slot_length() + wrench_y_min_gap) / 2),
                            top_face.center_location.position.Z,
                        )
                    ):
                        Text(
                            txt=wrench.label,
                            font_size=14,
                            font_path="./fonts/D-DINCondensed-Bold.otf",
                            font_style=FontStyle.BOLD,
                            rotation=270 if flip else 90,
                        )
            extrude(to_extrude=labels.sketch, amount=3, mode=Mode.ADD)
        return part

    # def bridge_between_wrench_groups(self, other: Self):
    #     # TODO: fix range
    #     with BuildPart() as part:
    #         num_wrenches = 14
    #         for x_idx in range(num_wrenches):
    #             y_idx = num_wrenches - x_idx
    #             x = self.wrenches[x_idx]
    #             y = other.wrenches[num_wrenches - y_idx]
    #             depth = max(x.extrusion_depth(), y.extrusion_depth())
    #             x_bound = x.total_slot_length() + wrench_y_min_gap
    #             y_bound = other.placement.y_start_pos(idx=y_idx)
    #             left_bound, right_bound = min(x_bound, y_bound), max(x_bound, y_bound)
    #             with BuildSketch(
    #                 Location((self.placement.x_start_pos(idx=x_idx), left_bound))
    #             ):
    #                 Rectangle(
    #                     width=self.placement.wrench_width(),
    #                     height=right_bound - left_bound,
    #                 )
    #             extrude(amount=-depth)
    #     return part


# %%

with BuildPart() as part:
    add(bin)
    top_face = (
        ### 3530 seconds (~60min) when find was:
        # part.faces().filter_by(GeomType.PLANE).filter_by_position(Axis.Z, 10,
        # 1000)
        bin.faces().sort_by(Axis.Z)[-1]
    )
    with Locations(top_face):
        metric_group = WrenchGroup(metric)
        add(metric_group.wrench_slots(), mode=Mode.SUBTRACT)
        add(metric_group.labels(), mode=Mode.ADD)

        # with Locations((0, 150)):
        imperial_group = WrenchGroup(imperial)
        add(imperial_group.wrench_slots(), mode=Mode.SUBTRACT, rotation=(0, 0, 180))
        add(imperial_group.labels(flip=True), mode=Mode.ADD, rotation=(0, 0, 180))

        # add(
        #     metric_group.bridge_between_wrench_groups(other=imperial_group),
        #     mode=Mode.SUBTRACT,
        # )

# show_all()
# %%
# export_stl(part.part, "out.stl")  # type: ignore
export_stl(part.part, "wrench_organizer.stl")
export_step(part.part, "wrench_organizer.step")

# %%


# with BuildPart() as part_with_chamfers:
#     add(part_with_wrenches_cut_out)
#     print("adding chamfers")
#     print(f"num faces: {len(part_with_wrenches_cut_out.faces())}")
#     to_chamfer: set[Edge] = set()
#     num_faces_to_chamfer = 0
#     deepest_wrench = max(
#         [
#             max(
#                 [
#                     # TODO: this is head extrusion depth from above. should pull
#                     # out into a helper
#                     wrench.extrustion_depth()
#                     for wrench in wrench_group
#                 ]
#             )
#             for wrench_group in wrenches
#         ]
#     )
#     for face in part_with_wrenches_cut_out.faces():
#         if (
#             face.center_location.position.Z
#             >= top_face.center_location.position.Z - deepest_wrench + 1
#         ):
#             num_faces_to_chamfer += 1
#             for edge in face.edges():
#                 to_chamfer.add(edge)
#     print(f"num faces to chamfer: {num_faces_to_chamfer}")
#     fillet(
#         objects=list(to_chamfer),
#         radius=1,
#     )

# %%

# with BuildPart() as part:
#     add(part_with_wrenches_cut_out)
#     top_face = (
#         ### 3530 seconds (~60min) when find was:
#         # part.faces().filter_by(GeomType.PLANE).filter_by_position(Axis.Z, 10,
#         # 1000)
#         bin.faces().sort_by(Axis.Z)[-1]
#     )
#     with Locations(top_face):
#         for group_idx, wrench_group in enumerate(wrenches):
#             WrenchGroup(wrench_group, mode=Mode.PRIVATE).text()


# show_all()
# %%

# %%

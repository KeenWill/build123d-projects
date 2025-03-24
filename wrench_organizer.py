# %%
from math import pi, sin
from build123d import *
from ocp_vscode import *


# %%

from gridfinity_build123d import *

part = Bin(
    BaseEqual(grid_x=2, grid_y=1, features=[MagnetHole(BottomCorners())]),
    height_in_units=3,
    # lip=StackingLip(),
    # compartments=CompartmentsEqual(compartment_list=[Compartment()]),
)


# with BuildPart() as art:
#     slice_count = 10
#     for i in range(slice_count + 1):
#         with BuildSketch(Plane(origin=(0, 0, i * 3), z_dir=(0, 0, 1))) as slice:
#             Circle(10 * sin(i * pi / slice_count) + 5)
#     loft()
#     top_bottom = art.faces().filter_by(GeomType.PLANE)
#     offset(openings=top_bottom, amount=0.5)

# want = 1306.3405290344635
# got = art.part.volume
# delta = abs(got - want)
# tolerance = want * 1e-5
# assert delta < tolerance, f"{delta=} is greater than {tolerance=}; {got=}, {want=}"

# show(art, names=["art"])
top_face = part.faces().filter_by(GeomType.PLANE).filter_by_position(Axis.Z, 10, 1000)


with BuildSketch(top_face) as wrench_slot:
    Rectangle(width=5, height=5)

show_all()
# %%

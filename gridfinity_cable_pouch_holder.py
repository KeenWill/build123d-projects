# %%
import math
from build123d import *
from build123d.build_common import *
from build123d.objects_part import *
from ocp_vscode import *
from gridfinity_build123d import *
from dataclasses import dataclass

# %%

bin = Bin(
    BaseEqual(grid_x=3, grid_y=2, features=[MagnetHole(BottomCorners())]),
    height_in_units=18,
    lip=StackingLip(),
    compartments=CompartmentsEqual(compartment_list=[Compartment()]),
)
# %%

show_all()

# %%
export_stl(to_export=bin, file_path="./gridfinity_cable_pouch_holder.stl")

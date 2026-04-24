import matplotlib.pyplot as plt
from matplotlib.textpath import TextPath
from matplotlib.patches import PathPatch
from matplotlib.transforms import Affine2D

# Create figure and axis
fig, ax = plt.subplots(figsize=(6, 4))

# Create text paths
text1 = TextPath((0, 0), "Hello", size=1)
text2 = TextPath((0, 0), "World", size=1)

# Initial locations
pos1 = (1, 2)
pos2 = (4, 2)

# Create transforms for initial placement
trans1 = Affine2D().translate(*pos1)
trans2 = Affine2D().translate(*pos2)

# Create PathPatch objects
patch1 = PathPatch(text1, color="blue", transform=trans1 + ax.transData)
patch2 = PathPatch(text2, color="red", transform=trans2 + ax.transData)

ax.add_patch(patch1)
ax.add_patch(patch2)

# ---- SWAP LOCATIONS ----
# New transforms (swap positions)
patch1.set_transform(Affine2D().translate(*pos2) + ax.transData)
patch2.set_transform(Affine2D().translate(*pos1) + ax.transData)

# Plot settings
ax.set_xlim(0, 7)
ax.set_ylim(0, 4)
ax.set_aspect("equal")
ax.axis("off")

plt.show()
from typing import IO, Sequence
from bmesh.types import BMesh
import bpy
from bpy.types import Image, Mesh, MeshLoopColor
from mathutils import Matrix, Vector

COLOR_LAYER = "tint"

def add_mesh(mesh1: BMesh, mesh2: Mesh, matrix: Matrix=Matrix.Identity(4), color: list[float]=[1,1,1,1]):
    """Add the contents of a mesh into another mesh.

    Args:
        mesh1 (Mesh): The base mesh.
        mesh2 (Mesh): The mesh to add.
        offset (Sequence[float, float, float]): Offset vector
    """
    # Blender 4.0+: use color_attributes instead of deprecated vertex_colors
    if not COLOR_LAYER in mesh2.color_attributes:
        mesh2.color_attributes.new(name=COLOR_LAYER, type='BYTE_COLOR', domain='CORNER')
    
    vcolors = mesh2.color_attributes[COLOR_LAYER]
    for poly in mesh2.polygons.values():
        for idx in poly.loop_indices:
            vcolors.data[idx].color_srgb = (color[0], color[1], color[2], color[3])

    mesh2.transform(matrix)
    mesh1.from_mesh(mesh2)
    mesh2.transform(matrix.inverted())

def import_image(file: IO[bytes], name: str, alpha=True, is_data=False) -> Image:
    """Pack an image from an IO stream into the current blend.

    Args:
        file (IO[bytes]): Raw data of PNG file.
        name (str): Name to give the datablock.
        alpha (bool, optional): Use alpha channel. Defaults to True.
        is_data (bool, optional): Create image with non-color data color space. Defaults to False.

    Returns:

        [type]: Loaded image datablock.
    """
    data = file.read()

    image = bpy.data.images.new(name, 1024, 1024, alpha=alpha, is_data=is_data)
    image.file_format = 'PNG'
    image.pack(data=data, data_len=len(data))
    image.source = 'FILE'

    return image
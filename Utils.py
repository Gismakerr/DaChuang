import os

import zipfile
import pandas as pd

import geopandas as gpd
from pathlib import Path


def unzip_files(source_dir, target_dir):
    """
    解压 source_dir 文件夹下所有 .zip 文件到 target_dir 文件夹中。
    
    :param source_dir: 要查找 zip 文件的文件夹路径
    :param target_dir: 解压目标路径
    """
    source = Path(source_dir)
    target = Path(target_dir)
    target.mkdir(parents=True, exist_ok=True)  # 创建目标目录（如果不存在）

    for item in os.listdir(source):
        if item.endswith(".zip"):
            zip_path = source / item
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(target)
            print(f"已解压: {zip_path} 到 {target}")

def delete_empty_shapefiles(folder_path):
    """
    删除目录下所有空的 .shp 文件及其相关的配套文件（.shx, .dbf, .prj 等）。
    
    :param folder_path: shapefile 所在文件夹路径
    """
    folder = Path(folder_path)
    deleted_files = []

    for shp_file in folder.glob("*.shp"):
        try:
            gdf = gpd.read_file(shp_file)
            if gdf.empty:
                stem = shp_file.stem
                for ext in ['shp', 'shx', 'dbf', 'prj', 'cpg', 'sbx', 'sbn']:
                    file_to_delete = shp_file.with_suffix(f".{ext}")
                    if file_to_delete.exists():
                        file_to_delete.unlink()
                deleted_files.append(stem)
        except Exception as e:
            print(f"无法读取 {shp_file.name}，跳过。错误：{e}")

    print(f"已删除空 shapefile 数量：{len(deleted_files)}")
    if deleted_files:
        print("已删除文件：", deleted_files)

def split_shapefile(input_shapefile, output_folder, id_field=None):
    """
    将一个 shapefile 中的每个要素单独导出为一个新的 shapefile。
    
    参数：
    - input_shapefile: str，输入 shapefile 路径（.shp）
    - output_folder: str，输出文件夹路径（若不存在将自动创建）
    - id_field: str，可选，作为文件名的字段（否则使用索引）

    返回：
    - 输出文件列表
    """
    # 读取 shapefile
    gdf = gpd.read_file(input_shapefile)

    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    output_files = []

    for idx, row in gdf.iterrows():
        single_gdf = gpd.GeoDataFrame([row], columns=gdf.columns, crs=gdf.crs)

        # 决定文件名
        if id_field and id_field in row and pd.notna(row[id_field]):
            file_name = f"{row[id_field]}.shp"
        else:
            file_name = f"feature_{idx}.shp"

        out_path = os.path.join(output_folder, file_name)
        single_gdf.to_file(out_path)
        output_files.append(out_path)

    print(f"✅ 导出完成，共导出 {len(output_files)} 个文件。")
    return output_files

def list_subfolders(base_folder, level=1):
    """
    获取指定目录下的所有子文件夹路径，可控制层数。

    参数：
        base_folder : str
            根目录路径。
        level : int 或 None
            控制递归层数：
            - level=1 ：只列出第一层文件夹
            - level=2 ：列出前两层
            - level=None ：无限递归

    返回：
        folders : list
            所有符合层数条件的文件夹绝对路径列表
    """
    base_folder = os.path.abspath(base_folder)
    folders = []

    def walk_dir(current_path, current_level):
        # 计算相对层级（根目录为0）
        rel_level = current_path.replace(base_folder, "").count(os.sep)
        if level is not None and rel_level >= level:
            return  # 超出层数停止

        for entry in os.scandir(current_path):
            if entry.is_dir():
                folders.append(entry.path)
                walk_dir(entry.path, current_level + 1)

    walk_dir(base_folder, 0)
    return folders
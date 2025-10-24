import os
import earthaccess
import geopandas as gpd
from pathlib import Path
# def search_swot_data(start_date, end_date, shapefile_path=None, 
#                      granule_pattern=None, 
#                      short_name=None):
#     """
#     查询 SWOT 数据（可选 shapefile 空间过滤），不执行下载。
    
#     参数：
#     - start_date, end_date: str，时间范围（格式 'YYYY-MM-DD'）
#     - shapefile_path: str or None，shapefile 路径（可选）
#     - granule_pattern: str，通配符匹配 granule_name
#     - short_name: str，产品名称
    
#     返回：
#     - results: list of granules
#     """
#     bbox_filter = None

#     if shapefile_path:
#         print(f"📍 Using shapefile for spatial filter: {shapefile_path}")
#         gdf = gpd.read_file(shapefile_path)
#         bounds = gdf.total_bounds  # [minx, miny, maxx, maxy]
#         minx, miny, maxx, maxy = bounds 
#         bbox_filter = (float(minx), float(miny), float(maxx), float(maxy))
#         print(f"🗺️  Bounding box: {bbox_filter}")
#         results = earthaccess.search_data(
#         short_name=short_name,
#         temporal=(f"{start_date} 00:00:00", f"{end_date} 23:59:59"),
#         bounding_box=bbox_filter,  # ✅ 用 bbox 而不是 bounding_box 避开冲突
#         granule_name=granule_pattern
#     )

#     else:
#         print("📍 No shapefile provided. Skipping spatial filter.")
#         results = earthaccess.search_data(
#         short_name=short_name,
#         temporal=(f"{start_date} 00:00:00", f"{end_date} 23:59:59"),
#         granule_name=granule_pattern,
#     )

#     print(f"🔍 Searching data from {start_date} to {end_date}...")
#     total_files = len(results)
#     total_size = sum(float(r.size()) for r in results if hasattr(r, "size"))

#     print(f"✅ Found {total_files} matching files.")
#     print(f"📦 Estimated total size: {total_size:.2f} MB")

#     return results

def search_swot_data(start_date, end_date, shapefile_path=None, 
                     granule_pattern=None, 
                     short_name=None):
    """
    查询 SWOT 数据（可选 shapefile 空间过滤），不执行下载。

    参数：
    - start_date, end_date: str，时间范围（格式 'YYYY-MM-DD'）
    - shapefile_path: str or None，shapefile 路径（可选）
    - granule_pattern: str or None，通配符匹配 granule_name（可选）
    - short_name: str，产品名称

    返回：
    - results: list of granules
    """
    bbox_filter = None

    if shapefile_path:
        print(f"📍 Using shapefile for spatial filter: {shapefile_path}")
        gdf = gpd.read_file(shapefile_path)
        bounds = gdf.total_bounds  # [minx, miny, maxx, maxy]
        minx, miny, maxx, maxy = bounds 
        bbox_filter = (float(minx), float(miny), float(maxx), float(maxy))
        print(f"🗺️  Bounding box: {bbox_filter}")
    else:
        print("📍 No shapefile provided. Skipping spatial filter.")

    # 构造通用的搜索参数字典
    search_kwargs = {
        "short_name": short_name,
        "temporal": (f"{start_date} 00:00:00", f"{end_date} 23:59:59"),
    }

    if bbox_filter:
        search_kwargs["bounding_box"] = bbox_filter
    if granule_pattern:
        search_kwargs["granule_name"] = granule_pattern

    print(f"🔍 Searching data from {start_date} to {end_date}...")

    results = earthaccess.search_data(**search_kwargs)

    total_files = len(results)
    total_size = sum(float(r.size()) for r in results if hasattr(r, "size"))

    print(f"✅ Found {total_files} matching files.")
    print(f"📦 Estimated total size: {total_size:.2f} MB")

    return results


# def download_swot_granules(results, download_dir):
#     """
#     下载 SWOT granules 到指定目录，自动跳过已存在且大小一致的文件。
#     """

#     os.makedirs(download_dir, exist_ok=True)
#     to_download = []
#     skipped = 0

#     print(f"\n⬇️ Preparing download to: {download_dir}")
    
#     for granule in results:
#         url = granule.data_links()[0]
#         filename = url.split("/")[-1]
#         filepath = Path(download_dir) / filename

#         try:
#             remote_size = float(granule.size())
#         except:
#             remote_size = None

#         if filepath.exists() and remote_size is not None:
#             local_size = filepath.stat().st_size / (1024 * 1024)  # MB
#             if abs(local_size - remote_size) < 1:
#                 print(f"✅ Skipped (already downloaded): {filename}")
#                 skipped += 1
#                 continue

#         to_download.append(granule)

#     # 批量统一下载
#     print(f"\n⬇️ Downloading {len(to_download)} new files...")
#     downloaded_files = earthaccess.download(to_download, download_dir)

#     print("\n📊 Summary:")
#     print(f"🔢 Total granules in search: {len(results)}")
#     print(f"✅ Skipped (already downloaded): {skipped}")
#     print(f"⬇️ Newly downloaded: {len(downloaded_files)}")

#     return downloaded_files

def download_swot_granules(results, download_dir):
    """
    下载 SWOT granules 到指定目录，
    自动跳过已存在且大小一致的文件；
    如果已存在但大小不一致，先删除再重新下载。
    """

    os.makedirs(download_dir, exist_ok=True)
    to_download = []
    skipped = 0
    removed = 0

    print(f"\n⬇️ Preparing download to: {download_dir}")
    
    for granule in results:
        url = granule.data_links()[0]
        filename = url.split("/")[-1]
        filepath = Path(download_dir) / filename

        try:
            remote_size = float(granule.size())  # 单位 MB
        except:
            remote_size = None

        if filepath.exists() and remote_size is not None:
            local_size = filepath.stat().st_size / (1024 * 1024)  # MB
            if abs(local_size - remote_size) < 1:
                print(f"✅ Skipped (already downloaded): {filename}")
                skipped += 1
                continue
            else:
                print(f"⚠️ Size mismatch, removing corrupted file: {filename}")
                filepath.unlink()  # 删除坏文件
                removed += 1
                to_download.append(granule)
        else:
            to_download.append(granule)

    # 批量下载
    print(f"\n⬇️ Downloading {len(to_download)} new files...")
    downloaded_files = earthaccess.download(to_download, download_dir)

    # 总结
    print("\n📊 Summary:")
    print(f"🔢 Total granules in search: {len(results)}")
    print(f"✅ Skipped (already downloaded): {skipped}")
    print(f"🗑️ Removed corrupted files: {removed}")
    print(f"⬇️ Newly downloaded: {len(downloaded_files)}")

    return downloaded_files

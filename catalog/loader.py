import requests
import json

STAC_CATALOG_URL = "https://data.earth.jaxa.jp/stac/cog/v1/catalog.json"


def get_catalog() -> dict:
    """
    unused in plugin
    this method needs too long time to run everytime on launch plugin
    run when build this plugin and make dictionary with output of this script
    UPDATE 2024-05-30 : catalog can be retrieved through following URL:
    https://data.earth.jaxa.jp/app/qgis/catalog.json
    This script to be used only when above URL does not work.
    """
    catalog = {}

    res = requests.get(STAC_CATALOG_URL)
    res_json = res.json()

    children = list(filter(lambda d: d["rel"] == "child", res_json.get("links", [])))
    for child in children:
        res_child = requests.get(child["href"])
        res_child_json = res_child.json()

        dataset_id = res_child_json["id"]
        dataset_title = res_child_json["title"]
        dataset_bands = list(res_child_json["assets"].keys())
        dataset_keywords = res_child_json["keywords"]
        dataset_bbox = res_child_json["extent"]["spatial"]["bbox"]
        dataset_temporal = res_child_json["extent"]["temporal"]["interval"]

        catalog[dataset_id] = {
            "title": dataset_title,
            "bands": dataset_bands,
            "keywords": dataset_keywords,
            "bbox": dataset_bbox,
            "temporal": dataset_temporal,
        }
    return catalog


if __name__ == "__main__":
    catalog = get_catalog()
    with open("./catalog.json", mode="w") as f:
        json.dump(catalog, f, ensure_ascii=False)

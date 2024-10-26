import logging
import uuid
import pandas as pd
import requests
import solara
from solara import (
    Button,
    Column,
    DataFrame,
    FileDownload,
    Path,
    Select,
    Markdown,
    Sidebar,
)

logging.config.fileConfig("logging.ini")
logger = logging.getLogger()

category = solara.reactive("")

shown_data = solara.reactive(None)
saved_data = solara.reactive(None)
summary_label = solara.reactive("")


def show_data():
    try:
        select = [
            "id",
            "title",
            "description",
            "price",
            "rating",
            "sku",
            "minimumOrderQuantity",
        ]
        response = requests.get(
            f"https://dummyjson.com/products/category/{category.value}?select={','.join(select)}'"
        )
        if response.ok:
            data = response.json()
        response.raise_for_status()
    except requests.RequestException:
        logger.error("Couldn't fetch products.")
        data = []
    logger.debug(data)
    result = pd.DataFrame.from_records(data["products"])
    saved_data.value = result
    shown_data.value = result.head(10)
    summary_label.value = f"Queried DummyJson.com for {category.value} category. Whole dataset has {saved_data.value.shape[0]} products."


@solara.component
def Page():
    solara.Style(Path("style.css"))

    with solara.Head():
        solara.Title("Product Catalog")

    with Sidebar():
        try:
            response = requests.get("https://dummyjson.com/products/category-list")
            if response.ok:
                categories = response.json()
                Select(label="Category", value=category, values=categories)
            response.raise_for_status()
        except requests.RequestException as e:
            solara.Error(label="Couldn't load categories. Please, refresh the page.")
            logger.error("Couldn't load categories", exc_info=True)

        Button(label="Get data", on_click=show_data)

        solara.Info(
            "This is only gonna be sample data and first 10 products will be shown.",
            dense=True,
            classes=["my-3"],
        )

    with Column(classes=["container"]):
        Markdown("# Summary")
        if shown_data.value is not None:
            DataFrame(
                items_per_page=10,
                scrollable=False,
            )
            FileDownload(
                saved_data.value.to_csv(index=False),
                filename=f"{str(uuid.uuid5(name=f'{category.value}', namespace=uuid.NAMESPACE_URL))}.csv",
                label=f"Download list: {saved_data.value.shape[0]} products",
            )
        else:
            solara.Info("Search results will be shown here.")

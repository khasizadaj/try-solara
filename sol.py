import uuid
import pandas as pd
import solara
from solara import (
    Button,
    Column,
    DataFrame,
    FileDownload,
    Info,
    Path,
    Select,
    Markdown,
    Sidebar,
    Success,
)

LOG_IDS = [
    "SIG_REST",
    "NET_DISC",
    "SEC_ALERT",
    "SIG_LOST",
    "BATT_LOW",
    "DATA_START",
    "BATT_CHRG",
    "DATA_END",
    "NET_CONN",
    "FW_UPD",
]

CUSTOMERS = [
    "Verizon",
    "Sprint",
    "AT&T",
    "Orange",
    "Vodafone",
    "China Mobile",
    "Telefonica",
    "T-Mobile",
    "Telecom Italia",
    "Deutsche Telekom",
]

event_log_id = solara.reactive(LOG_IDS[0])
customer = solara.reactive(CUSTOMERS[0])

df = pd.read_csv("generated_log_data.csv")
shown_data = solara.reactive(None)
saved_data = solara.reactive(None)
summary_label = solara.reactive("")


def show_data():
    global df
    result = df[
        (df["Customer"] == customer.value) & (df["LogId"] == event_log_id.value)
    ]
    saved_data.value = result
    shown_data.value = result.head(10)
    summary_label.value = f"Parsed logs for {customer.value} with {event_log_id.value}. Whole dataset has {saved_data.value.shape[0]} event logs."


@solara.component
def Page():
    solara.Style(Path("style.css"))

    with solara.Head():
        solara.Title("Event Log Summarizer")

    with Sidebar():
        Select(label="Customer", value=customer, values=CUSTOMERS)
        Select(label="Event Log Identifier", value=event_log_id, values=LOG_IDS)
        Button(label="Get data", on_click=show_data)
        Info("This is only gonna be sample data and first 10 event logs will be shown.", dense=True, classes=["my-3"])

    with Column(classes=["container"]):
        Markdown("# Summary")

        if shown_data.value is not None:
            Success(summary_label.value)
            DataFrame(shown_data.value.reset_index(drop=True), items_per_page=10, scrollable=False)
            FileDownload(
                saved_data.value.to_csv(index=False),
                filename=f"{str(uuid.uuid5(name=f'{customer.value}+{event_log_id.value}', namespace=uuid.NAMESPACE_URL))}.csv",
                label=f"Download file: {saved_data.value.shape[0]} events",
            )

        
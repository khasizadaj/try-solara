import uuid
import pandas as pd
import solara
from solara import (
    Column,
    DataFrame,
    FileDownload,
    Path,
    Select,
    Markdown,
    Sidebar,
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


@solara.component
def Page():
    solara.Style(Path("style.css"))

    with solara.Head():
        solara.Title("Event Log Summarizer")

    with Sidebar():
        Select(label="Customer", value=customer, values=CUSTOMERS)
        Select(label="Event Log Identifier", value=event_log_id, values=LOG_IDS)

    with Column(classes=["container"]):
        Markdown("## Summary")
        Markdown(f"Parsed logs for {customer.value} with {event_log_id.value}")
        global df
        local_df = df[
            (df["Customer"] == customer.value) & (df["LogId"] == event_log_id.value)
        ]

        DataFrame(local_df, items_per_page=10)
        FileDownload(
            local_df.reset_index(drop=True).to_csv(index=False),
            filename=f"{str(uuid.uuid5(name=f'{customer.value}+{event_log_id.value}', namespace=uuid.NAMESPACE_URL))}.csv",
            label="Download file",
        )

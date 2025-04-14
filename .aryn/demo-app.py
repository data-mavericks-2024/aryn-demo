from aryn_sdk.client.client import Client
from aryn_sdk.client.exceptions import ArynSDKException
from aryn_sdk.client.client import Client
from aryn_sdk.types.docset import DocSetMetadata, DocSetUpdate 
from aryn_sdk.types.document import DocumentMetadata, ReplaceOperation, FieldUpdates 
from aryn_sdk.types.schema import SchemaField, Schema 
from aryn_sdk.types.search import SearchRequest, SearchResponse

import boto3
from aryn_sdk.partition import partition_file, tables_to_pandas

ARYN_API_KEY="eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3NDQwMTE3NDcsInN1YiI6eyJhY3QiOiIzMjU1MTY0MjA5NDUiLCJlbWwiOiJzdXNoaWwuam9zaGlAc2FhbWEuY29tIiwiZ2VuIjowLCJpZCI6MjA3ODc1NTY3MX19.WTm7scAbkBlegU_pX4dCzT-UpdAYsoxmmsygRM5lNiHZbyxIZZKmr-HAoidOPGyTWi1mfGwrk3eAiosZFPGEDw"


file_name = "3m_10k.pdf"
s3 = boto3.client("s3")
s3.download_file("aryn-public", "partitioner-blog-data/3m_10k.pdf", file_name)
f = open(file_name, "rb")

## Make a call to the partitioning service and set extract_table_structure and use_ocr to True.
## Also set selected_pages to 23 to just pull out that page.
partitioned_file = partition_file(f, aryn_api_key, extract_table_structure=True, use_ocr=True, selected_pages=[23])

pandas = tables_to_pandas(partitioned_file)

# pull out the tables from the list of elements
tables = []
for elt, dataframe in pandas:
    if elt["type"] == "table":
        tables.append(dataframe)

# pull out the first table
industry_geographic_breakdown = tables[0]

# display the dataframe
industry_geographic_breakdown

# pull out the sales data for 'Electronics and Energy' segment
industry_geographic_breakdown[
    [
        "",
        "Three months ended December 31, 2018 | United States",
        "Three months ended December 31, 2018 | Europe; Middle East Africa",
    ]
].iloc[[19]]
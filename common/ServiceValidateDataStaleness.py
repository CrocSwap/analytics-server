from .DataClasses import GraphMetadataBlock
from .ServiceBase import ServiceBase


class ServiceValidateDataStaleness(ServiceBase):
    FRESHNESS_BLOCK_NUMBER_THRESHOLD = 2

    def validate_graph_staleness(self):
        """
        Get subgraph metadata
        """
        query = """
        query GetGraphMetadata {
          _meta {
                block {
                    hash
                    number
                    timestamp
                }
            }
        }
        """
        graph_result = self.crocQuery.query_subgraph(query)
        graph_metadata = GraphMetadataBlock(**graph_result["data"]["_meta"]["block"])
        latest_chain_block_number = self.w3.eth.block_number

        return {
            "result": graph_metadata["number"]
            >= latest_chain_block_number - self.FRESHNESS_BLOCK_NUMBER_THRESHOLD,
            "graph_metadata": graph_metadata,
            "latest_chain_block_number": latest_chain_block_number,
        }

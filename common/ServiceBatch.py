from .ServiceFactory import ServiceFactory
from .ServiceBase import ServiceBase


class ServiceBatch(ServiceBase):
    def service_processes_batch(self, data):
        # Parse the JSON to get the list of requests
        req_list = data["req"]
        results = []

        # Iterate through the list of requests
        for req_item in req_list:
            config_path = req_item["config_path"]
            args = req_item["args"]
            
            result = ServiceFactory.invoke_dynamic_service(
                args,
                config=ServiceFactory.load_service(config_path),
                network=self.get_network_config(),
                include_data="0",
            )

            parsedResult = {"req_id": req_item["req_id"], "results": result}
            # parse into json
            results.append(parsedResult)
        return {"data": results}

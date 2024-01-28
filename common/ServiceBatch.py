from .ServiceFactory import ServiceFactory
from .ServiceBase import ServiceBase
import time

import random
class ServiceBatch(ServiceBase):
    def service_processes_batch(self, data):
        try:
            # Parse the JSON to get the list of requests
            req_list = data["req"]
            results = []
            time_start = time.time()
            time_end = time_start + 3.0 
            i = 0
            inds = list(range(0,len(req_list)))  
            random.shuffle(inds)   
            for i in inds:
                req_item = req_list[i]
                #print("calcing " + str(i))
                config_path = req_item["config_path"]
                args = req_item["args"]
                try:
                    result = ServiceFactory.invoke_dynamic_service(
                        args,
                        config=ServiceFactory.load_service(config_path),
                        network=self.get_network_config(),
                        include_data="0",
                    )
                    parsedResult = {"req_id": req_item["req_id"], "results": result}
                except:
                    import traceback as tb
                    parsedResult =   {"req_id": req_item["req_id"], "results": {"error":tb.format_exc()}}  
                    
                results.append(parsedResult)
                if time.time() > time_end:
                    
                    break
            return {"data": results}
        except:
            import traceback as tb
            tb.print_exc()
            return {"error":tb.format_exc()}

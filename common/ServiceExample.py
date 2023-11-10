from .ServiceBase import ServiceBase
class ServiceExample(ServiceBase):
    def serviceFunc(self,arg1,arg2): 
        return {"arg1":arg1,
                "arg2":arg2}

import win32service
import win32serviceutil


from pysrvany import utils


class WinService(win32serviceutil.ServiceFramework):
    CLASS_ARGS_PARAM = "class_args"
    CLASS_PATH_PARAM = "class_path"

    def __init__(self, args):
        self._svc_name_, = args
        service_class_path = win32serviceutil.GetServiceCustomOption(self._svc_name_, self.CLASS_PATH_PARAM)
        service_class_args = win32serviceutil.GetServiceCustomOption(self._svc_name_, self.CLASS_ARGS_PARAM)
        self.service = utils.Shell.create(service_class_path, service_class_args)
        super().__init__(args)

    def SvcDoRun(self):
        self.service.run()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.service.stop()

    @classmethod
    def install(cls, service_class_path, service_name, *args, **kwargs):
        service_class_args = utils.Shell.serialize_args(*args, **kwargs)
        win32serviceutil.InstallService(utils.ClassPath.serialize(cls), service_name, service_name)
        win32serviceutil.SetServiceCustomOption(service_name, cls.CLASS_PATH_PARAM, service_class_path)
        win32serviceutil.SetServiceCustomOption(service_name, cls.CLASS_ARGS_PARAM, service_class_args)

import sys

from pysrvany import services, utils


class InstallExe(utils.Install):
    NAME = "install_exe"

    def parse(self, *args):
        super().parse_constructor(utils.ClassPath.serialize(services.Executable))
        super().parse_arguments(*args)


def get_win_service():
    from pysrvany import win_service
    return win_service.WinService


def main(action, service_name, *cmd_args):
    call = utils.Call()
    parser = utils.Parser(call)
    parser.register_action(InstallExe)
    parser.parse(action, service_name, *cmd_args)
    get_win_service().install(call.constructor, call.name, call.args, **call.kwargs)


if __name__ == '__main__':
    main(*sys.argv[1:])

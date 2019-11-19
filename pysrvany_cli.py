import sys

from pysrvany import services, utils


def get_win_service():
    from pysrvany import win_service
    return win_service.WinService


def main(action, service_name, *cmd_args):
    if action == 'install_exe':
        service_class_path = utils.Shell.serialize_class(services.Executable)
        cmd_args = list(cmd_args)
        kwargs = {}
        try:
            idx = cmd_args.index("--pysrvany-cwd")
            kwargs["cwd"] = cmd_args[idx + 1]
            cmd_args.pop(idx)
            cmd_args.pop(idx)
        except ValueError:
            pass
        args = [cmd_args]
    elif action == 'install_class':
        service_class_path, args, kwargs = cmd_args[0], cmd_args[1:], {}
    else:
        assert False
    get_win_service().install(service_class_path, service_name, *args, **kwargs)


if __name__ == '__main__':
    main(*sys.argv[1:])

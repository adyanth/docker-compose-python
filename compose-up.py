import compose.cli.main as compose
from compose.parallel import ParallelStreamWriter
from functools import partial
from io import StringIO
import logging

def monkey_patch_compose(compose, logObject):
    compose.console_handler = logging.StreamHandler(logObject)

    ParallelStreamWriter(logObject).set_noansi()

    def log_printer_from_project(
        project,
        containers,
        monochrome,
        log_args,
        cascade_stop=False,
        event_stream=None,
    ):
        return compose.LogPrinter(
            containers,
            compose.build_log_presenters(project.service_names, monochrome),
            event_stream or project.events(),
            output=logObject,
            cascade_stop=cascade_stop,
            log_args=log_args
        )

    compose.log_printer_from_project = log_printer_from_project


def dispatch(args):
    dispatcher = compose.DocoptDispatcher(
        compose.TopLevelCommand, {'options_first': True, 'version': compose.get_version_info('compose')}
    )
    options, handler, command_options = dispatcher.parse(args)
    compose.setup_console_handler(compose.console_handler, options.get('--verbose'), compose.set_no_color_if_clicolor(options.get('--no-ansi')), options.get("--log-level"))
    return partial(compose.perform_command, options, handler, command_options)

def run(file):
    try:
        command = dispatch([
            '--no-ansi',
            '-f', file,
            "up", "-d"      # Can use any docker-compose command, as shown below
            # 'logs', 'mongo'
            # 'down'
        ])
        return command()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    output = StringIO()
    monkey_patch_compose(compose, output)
    run('docker-compose-test.yml')
    print("Output:")
    print(output.getvalue())

from DATA.commands import search, get_search_output, get_list_output, list_installed, show, get_show_output, install
import argparse
import subprocess
import sys
sys.path.insert(1, '../')
parser = argparse.ArgumentParser(
    prog="CLI",
    description="Use this cli to manage application instalations",
    epilog="epilog"
)


subparsers = parser.add_subparsers(help='sub-command help')


# searching for packages on winget
parser_search = subparsers.add_parser("search", help="search help")
parser_search.add_argument("search_query", type=str,
                           help="The query used to search for the specific application")
parser_search.add_argument(
    "--id", type=str, help="Filter the search to include only apps with the specified id on winget")
parser_search.add_argument(
    "--name", type=str, help="Filter the search to include only apps with the specified name on winget")
parser_search.add_argument(
    "--tag", type=str, help="Filter the search to include only apps with the specified tag on winget")
parser_search.add_argument("-e", "--exact", action='store_true',
                           help="Uses the exact string in the query, case-sensitivity included")
parser_search.set_defaults(func=lambda args: get_search_output(search(args)))

# listing existing applications on winget
parser_list = subparsers.add_parser("list", help="list help")
parser_list.add_argument("list_query", type=str, nargs='?', default=None,
                         help="The query used to list the applications installed on your system")
parser_list.add_argument(
    "--id", type=str, help="Filter include only apps with the specified id on winget")
parser_list.add_argument(
    "--name", type=str, help="Filter include only apps with the specified name on winget")
parser_list.add_argument(
    "--tag", type=str, help="Filter include only apps with the specified tag on winget")
parser_list.add_argument(
    "--scope", type=str, help="Filter by the user/machine scope")
parser_list.add_argument("-e", "--exact", action='store_true',
                         help="Uses the exact string in the query, case-sensitivity included")
parser_list.add_argument("--versions", action='store_true',
                         help="Shows the versions for the application")
parser_list.set_defaults(func=lambda args: get_list_output(list_installed(args)))

# showing package info on winget
parser_show = subparsers.add_parser("show", help="show help")
parser_show.add_argument("show_query", type=str, nargs='?', default=None,
                         help="The query used to search for the specific application")
parser_show.add_argument(
    "--id", type=str, help="Filter include only apps with the specified id on winget")
parser_show.add_argument(
    "--name", type=str, help="Filter include only apps with the specified name on winget")
parser_show.add_argument(
    "--tag", type=str, help="Filter include only apps with the specified tag on winget")
parser_show.add_argument("-e", "--exact", action='store_true',
                         help="Uses the exact string in the query, case-sensitivity included")
parser_show.add_argument("--versions", action='store_true',
                         help="Shows the versions for the application")
parser_show.set_defaults(func=lambda args: get_show_output(show(args)))



# installing a package with winget
parser_show = subparsers.add_parser("install", help="install help")
parser_show.add_argument("install_query", type=str,
                         help="The query used to search for the specific application")
parser_show.add_argument(
    "--id", type=str, help="Filter include only apps with the specified id on winget")
parser_show.add_argument(
    "--name", type=str, help="Filter include only apps with the specified name on winget")
parser_show.add_argument(
    "--tag", type=str, help="Filter include only apps with the specified tag on winget")
parser_show.add_argument("-e", "--exact", action='store_true',
                         help="Uses the exact string in the query, case-sensitivity included")
parser_show.add_argument("-v", "--version",
                         help="Select the version for the installation. If unspecified the latest version will be selected")
parser_show.add_argument("--scope",
                         help="The user/machine scope for the installation")
parser_show.add_argument("--source",
                         help="Specify the sorce of the package")
parser_show.add_argument("-a", "--arhitecture",
                         help="The arhitecture to install")
parser_show.add_argument("-i", "--interactive", action='store_true',
                         help="Run the installer in interactive mode")
parser_show.add_argument("-s", "--silent", action='store_true',
                         help="Run the installer in silent mode, suppressing all UI, if possible.")
parser_show.add_argument("--override",
                         help="A string that will be passed directly to the installer")
parser_show.add_argument("--disable-interactivity", action='store_true',
                         help="Disable interactive prompts")
parser_show.add_argument("-l", "--location",
                         help="The path for the instalation if supported. (If the package doesn't install on the specified location when using the -l tag, then it doesn't support it and it would be advised to run it in interactive mode for location features)")
parser_show.set_defaults(func=install)


# uninstalling a package with winget
def uninstall(args):
    options = "winget uninstall --accept-source-agreements " + \
        "\"" + args.uninstall_query + "\"" + " "
    if args.id:
        options += " --id " + args.id + " "
    if args.name:
        options += " --name " + args.name + " "
    if args.tag:
        options += " --tag " + args.tag + " "
    if args.exact:
        options += " --exact "
    if args.version:
        options += " --version " + args.version + " "
    if args.interactive:
        options += " --interactive "
    if args.silent and not args.interactive:
        options += " --silent "
    if args.preserve:
        options += " --preserve "
    if args.purge and not args.preserve:
        options += " --purge "
    print(options)
    subproc = subprocess.run(
        options.strip(), capture_output=True, shell=True)
    print("output: ", subproc.stdout.decode())


parser_show = subparsers.add_parser("uninstall", help="uninstall help")
parser_show.add_argument("uninstall_query", type=str,
                         help="The query used to search for the specific application")
parser_show.add_argument(
    "--id", type=str, help="Filter include only apps with the specified id on winget")
parser_show.add_argument(
    "--name", type=str, help="Filter include only apps with the specified name on winget")
parser_show.add_argument(
    "--tag", type=str, help="Filter include only apps with the specified tag on winget")
parser_show.add_argument("-e", "--exact", action='store_true',
                         help="Uses the exact string in the query, case-sensitivity included")
parser_show.add_argument("-v", "--version",
                         help="Select the version for the uninstall. If unspecified the latest version will be selected")
parser_show.add_argument("-i", "--interactive", action='store_true',
                         help="Run the uninstaller in interactive mode")
parser_show.add_argument("-s", "--silent", action='store_true',
                         help="Run the uninstaller in silent mode, suppressing all UI, if possible.")
parser_show.add_argument("--purge", action='store_true',
                         help="Deletes all files and directories in the application directory")
parser_show.add_argument("--preserve", action='store_true',
                         help="Retains all files and directories created by the application")
parser_show.set_defaults(func=uninstall)

args = parser.parse_args()
print(args.func(args))

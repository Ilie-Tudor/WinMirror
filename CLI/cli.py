from DATA.commands import *
import argparse
import sys
import json
sys.path.insert(1, '../')
parser = argparse.ArgumentParser(
    prog="WinMirrorCLI",
    description="Use this cli to manage application instalations and bundles",
    epilog="For a more interactive experience, try out the WinMirror GUI application"
)

subparsers = parser.add_subparsers(help='sub-command help')

# searching for packages on winget
parser_search = subparsers.add_parser("search", help="Search for applications using winget utility")
parser_search.add_argument("search_query", type=str, nargs='?', default=None,
                           help="The query used to search for the specific application")
parser_search.add_argument(
    "--id", type=str, help="Filter the search to include only apps with the specified id on winget")
parser_search.add_argument(
    "--name", type=str, help="Filter the search to include only apps with the specified name on winget")
parser_search.add_argument(
    "--tag", type=str, help="Filter the search to include only apps with the specified tag on winget")
parser_search.add_argument("-e", "--exact", action='store_true',
                           help="Uses the exact string in the query, case-sensitivity included")
parser_search.set_defaults(func=lambda args: json.dumps(get_search_output(search(args)), indent=4))


# listing existing applications on winget
parser_list = subparsers.add_parser("list", help="List the application that are installed on your system")
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
parser_list.set_defaults(func=lambda args: json.dumps(get_list_output(list_installed(args)), indent=4))


# showing package info on winget
parser_show = subparsers.add_parser("show", help="Show detailed information about a specific application. If the query isn't narrow enough to resolve to one app, then further filtering is necessary")
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
parser_install = subparsers.add_parser("install", help="Install a specific application found on winget")
parser_install.add_argument("install_query", type=str, nargs='?', default=None,
                         help="The query used to search for the specific application")
parser_install.add_argument(
    "--id", type=str, help="Filter include only apps with the specified id on winget")
parser_install.add_argument(
    "--name", type=str, help="Filter include only apps with the specified name on winget")
parser_install.add_argument(
    "--tag", type=str, help="Filter include only apps with the specified tag on winget")
parser_install.add_argument("-e", "--exact", action='store_true',
                         help="Uses the exact string in the query, case-sensitivity included")
parser_install.add_argument("-v", "--version",
                         help="Select the version for the installation. If unspecified the latest version will be selected")
parser_install.add_argument("--scope",
                         help="The user/machine scope for the installation")
parser_install.add_argument("--source",
                         help="Specify the sorce of the package")
parser_install.add_argument("-a", "--arhitecture",
                         help="The arhitecture to install")
parser_install.add_argument("-i", "--interactive", action='store_true',
                         help="Run the installer in interactive mode")
parser_install.add_argument("-s", "--silent", action='store_true',
                         help="Run the installer in silent mode, suppressing all UI, if possible.")
parser_install.add_argument("--override",
                         help="A string that will be passed directly to the installer")
parser_install.add_argument("--disable-interactivity", action='store_true',
                         help="Disable interactive prompts")
parser_install.add_argument("-l", "--location",
                         help="The path for the instalation if supported. (If the package doesn't install on the specified location when using the -l tag, then it doesn't support it and it would be advised to run it in interactive mode for location features)")
parser_install.set_defaults(func=install)


# uninstalling a package with winget
parser_uninstall = subparsers.add_parser("uninstall", help="Uninstall an existing application from your sistem")
parser_uninstall.add_argument("uninstall_query", type=str, nargs='?', default=None,
                         help="The query used to search for the specific application")
parser_uninstall.add_argument(
    "--id", type=str, help="Filter include only apps with the specified id on winget")
parser_uninstall.add_argument(
    "--name", type=str, help="Filter include only apps with the specified name on winget")
parser_uninstall.add_argument(
    "--tag", type=str, help="Filter include only apps with the specified tag on winget")
parser_uninstall.add_argument("-e", "--exact", action='store_true',
                         help="Uses the exact string in the query, case-sensitivity included")
parser_uninstall.add_argument("-v", "--version",
                         help="Select the version for the uninstall. If unspecified the latest version will be selected")
parser_uninstall.add_argument("-i", "--interactive", action='store_true',
                         help="Run the uninstaller in interactive mode")
parser_uninstall.add_argument("-s", "--silent", action='store_true',
                         help="Run the uninstaller in silent mode, suppressing all UI, if possible.")
parser_uninstall.add_argument("--purge", action='store_true',
                         help="Deletes all files and directories in the application directory")
parser_uninstall.add_argument("--preserve", action='store_true',
                         help="Retains all files and directories created by the application")
parser_uninstall.set_defaults(func=uninstall)


# getting information about winget
parser_uninstall = subparsers.add_parser("info", help="Uninstall an existing application from your sistem")
parser_uninstall.set_defaults(func=info)


# bundle management
parser_bundle = subparsers.add_parser("bundle", help="Bundle management commands group. A bundle is a colection of application that cand be bulk installed and exported")
bundle_subparsers = parser_bundle.add_subparsers(help="Manage bundles of application to bulk install, export, add, etc. winget applications")


# get bundle
parser_get_bundles = bundle_subparsers.add_parser("get", help="Get bundles information")
parser_get_bundles.add_argument("-t", "--title", 
                         help="Get the bundle with the specified title")
parser_get_bundles.add_argument("-i", "--id", type=int,
                         help="Get the bundle with the specified id")
parser_get_bundles.add_argument("-a", "--all", action="store_true",
                         help="Get all the bundles available")
parser_get_bundles.set_defaults(func=lambda args: json.dumps(get_bundle(args), indent=4))


# create bundle
parser_create_bundles = bundle_subparsers.add_parser("create", help="Create a new bundle")
parser_create_bundles.add_argument("-t", "--title", required=True,
                         help="The title of the new bundle")
parser_create_bundles.add_argument("-d", "--description", required=True,
                         help="The description of the new bundle")
parser_create_bundles.add_argument("-a", "--apps", type=json.loads,
                         help="Get all the bundles available")
parser_create_bundles.set_defaults(func=lambda args: json.dumps(create_bundle(args),indent=4))


# delete bundle
parser_delete_bundles = bundle_subparsers.add_parser("delete", help="Delete a bundle")
parser_delete_bundles.add_argument("-i", "--id", type=int, required=True,
                         help="The id of the bundle")
parser_delete_bundles.set_defaults(func=delete_bundle)


# update bundle title
parser_update_bundle_title = bundle_subparsers.add_parser("title", help="Update the title of a bundle")
parser_update_bundle_title.add_argument("-i", "--id", type=int, required=True,
                         help="The id of the bundle")
parser_update_bundle_title.add_argument("-t", "--title", required=True,
                         help="The new title for the specified bundle")
parser_update_bundle_title.set_defaults(func=update_bundle_title)


# add application in bundle
parser_add_to_bundle = bundle_subparsers.add_parser("add", 
                                                    help="""Add applications to bundle. The application should adhere to the following schema:
                                                    winget_app: {
                                                        name: string,
                                                        id: string,
                                                        source: string
                                                    }
                                                    or
                                                    readonly_app:{
                                                        name: string,
                                                        url: string,
                                                        id: string
                                                    }
                                                    
                                                    """)
parser_add_to_bundle.add_argument("-b", "--bundle-id", type=int, required=True,
                         help="The id of the bundle")
parser_add_to_bundle.add_argument("-t", "--type", required=True,
                         help="The type of the application (winget/readonly)")
parser_add_to_bundle.add_argument("-a", "--app", type=json.loads, required=True,
                         help="The content of the application to add")
parser_add_to_bundle.set_defaults(func=lambda args: json.dumps(add_application_to_bundle(args),indent=4))


# remove application from bundle
parser_remove_from_bundle = bundle_subparsers.add_parser("remove", help="Remove application from bundle")
parser_remove_from_bundle.add_argument("-b", "--bundle-id", type=int, required=True,
                         help="The id of the bundle")
parser_remove_from_bundle.add_argument("-t", "--type", required=True,
                         help="The type of the application (winget/readonly)")
parser_remove_from_bundle.add_argument("-i", "--id", required=True,
                         help="The id of the application to remove")
parser_remove_from_bundle.set_defaults(func=lambda args: json.dumps(remove_application_from_bundle(args), indent=4))


# export bundle
parser_export_bundle = bundle_subparsers.add_parser("export", help="Export a bundle")
parser_export_bundle.add_argument("-i", "--id", type=int, required=True,
                         help="The id of the bundle")
parser_export_bundle.add_argument("-o", "--output", required=True,
                         help="The path to the file in which to export")
parser_export_bundle.set_defaults(func=export_bundle)


# import bundle
parser_import_bundle = bundle_subparsers.add_parser("import", help="Import a bundle")
parser_import_bundle.add_argument("-f", "--file", required=True,
                         help="The file containing the bundle")
parser_import_bundle.set_defaults(func=import_bundle)


# bundle install
parser_install_bundle = bundle_subparsers.add_parser("install", help="Bulk install all the applications from a bundle")
parser_install_bundle.add_argument("-b", "--bundle-id", required=True,
                         help="The id of the bundle to bulk install")
parser_install_bundle.set_defaults(func=bundle_install)



args = parser.parse_args()
args.func(args)
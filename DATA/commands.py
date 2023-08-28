import subprocess
import re
import os
import json
import DATA.db_controller as db

# listing/searching for packages on winget
def get_search_output(output_string: str):
    lines = output_string.split("\n")

    # this line here is needed for the case in which winget cannot search in a certain source
    lines = list(
        filter(lambda e: 'Failed when searching source' not in e, lines))
    # ---------------------------------------------------------------------------------------

    table_head = re.sub('[^[^a-zA-Z0-9.:\s]+', '', lines[0]).strip()

    name_column_search = re.search('Name\s+', table_head)
    name_column_bounds = None
    if name_column_search:
        name_column_bounds = (name_column_search.start(),
                              name_column_search.end()-1)

    id_column_search = re.search('Id\s+', table_head)
    id_column_bounds = None
    if id_column_search:
        id_column_bounds = (id_column_search.start(), id_column_search.end()-1)

    version_column_search = re.search('Version\s+', table_head)
    version_column_bounds = None
    if version_column_search:
        version_column_bounds = (
            version_column_search.start(), version_column_search.end()-1)

    match_column_search = re.search('Match\s+', table_head)
    match_column_bounds = None
    if match_column_search:
        match_column_bounds = (match_column_search.start(),
                               match_column_search.end()-1)

    source_column_search = re.search('Source\s*', table_head)
    source_column_bounds = None
    if source_column_search:
        source_column_bounds = (source_column_search.start(),
                                source_column_search.end()-1)

    packages_list = []
    for line in lines[2:len(lines)-1]:
       
        package = {}
        line = re.sub(r'[^\x00-\x7F]', '**', line)
        line = re.sub('[^a-zA-Z0-9()}{&+-_*.:\s]+', '?', line).strip()

        package["name"] = line[name_column_bounds[0]
            :name_column_bounds[1]].strip()
        package["id"] = line[id_column_bounds[0]:id_column_bounds[1]].strip()
        package["version"] = line[version_column_bounds[0]
            :version_column_bounds[1]].strip()
        if match_column_bounds:
            package["match"] = line[match_column_bounds[0]:match_column_bounds[1]].strip()
        if source_column_bounds:
            package["source"] = line[source_column_bounds[0]:].strip()
        packages_list.append(package)
    
    return packages_list

def get_list_output(output_string: str):
    lines = output_string.split("\n")

    # this line here is needed for the case in which winget cannot search in a certain source
    lines = list(
        filter(lambda e: 'Failed when searching source' not in e, lines))
    # ---------------------------------------------------------------------------------------

    table_head = re.sub('[^[^a-zA-Z0-9.:\s]+', '', lines[0]).strip()

    name_column_search = re.search('Name\s*', table_head)
    name_column_bounds = None
    if name_column_search:
        name_column_bounds = (name_column_search.start(),
                              name_column_search.end())

    id_column_search = re.search('Id\s*', table_head)
    id_column_bounds = None
    if id_column_search:
        id_column_bounds = (id_column_search.start(), id_column_search.end())

    version_column_search = re.search('Version\s*', table_head)
    version_column_bounds = None
    if version_column_search:
        version_column_bounds = (
            version_column_search.start(), version_column_search.end())

    available_version_column_search = re.search('Available\s*', table_head)
    available_version_column_bounds = None
    if available_version_column_search:
        available_version_column_bounds = (available_version_column_search.start(),
                               available_version_column_search.end())

    source_column_search = re.search('Source\s*', table_head)
    source_column_bounds = None
    if source_column_search:
        source_column_bounds = (source_column_search.start(),
                                source_column_search.end())

    packages_list = []
    for line in lines[2:len(lines)-1]:
        # the regex here may need modifications after more testing. Version or id may contain other characters too.
        package = {}
        line = re.sub(r'[^\x00-\x7F]', '**', line)
        line = re.sub('[^a-zA-Z0-9()}{&+-_*.:\s]+', '?', line).strip()
        package["name"] = line[name_column_bounds[0]
            :name_column_bounds[1]].strip()
        package["id"] = line[id_column_bounds[0]:id_column_bounds[1]].strip()
        if version_column_bounds:
            package["version"] = line[version_column_bounds[0]
                :version_column_bounds[1]].strip()
        if available_version_column_bounds:
            package["available"] = line[available_version_column_bounds[0]:available_version_column_bounds[1]].strip()
        if source_column_bounds:
            package["source"] = line[source_column_bounds[0]:source_column_bounds[1]].strip()
        packages_list.append(package)
    # print(json.dumps(packages_list, indent=4))
    return packages_list


class Search_Args:
    def __init__(self, search_query, id, name, tag, exact) -> None:
        self.search_query = search_query
        self.id = id
        self.name = name
        self.tag = tag
        self.exact = exact

class List_Args:
    def __init__(self, list_query, id, name, tag, exact, scope) -> None:
        self.list_query = list_query
        self.id = id
        self.name = name
        self.tag = tag
        self.exact = exact
        self.scope = scope


def search(args):
    options = "winget search " + "\"" + args.search_query + "\"" + " "
    if args.id:
        options += " --id " + args.id + " "
    if args.name:
        options += " --name " + args.name + " "
    if args.tag:
        options += " --tag " + args.tag + " "
    if args.exact:
        options += " --exact "
    subproc = subprocess.run(
        options.strip(), capture_output=True, shell=True)

    return subproc.stdout.decode()


def list_installed(args):
    options = "winget list "
    if args.list_query:
        options += "\"" + args.list_query + "\"" + " "
    if args.id:
        options += " --id " + args.id + " "
    if args.name:
        options += " --name " + args.name + " "
    if args.tag:
        options += " --tag " + args.tag + " "
    if args.exact:
        options += " --exact "
    if args.scope:
        options += " --scope " + args.scope
    subproc = subprocess.run(
        options.strip(), capture_output=True, shell=True)
    # print("output: ", subproc.stdout.decode())
    return subproc.stdout.decode()

# showing package information on winget
def get_show_output(output_string: str):
    lines = output_string.split("\n")

    # this line here is needed for the case in which winget cannot search in a certain source
    lines = list(
        filter(lambda e: 'Failed when searching source' not in e, lines))
    # ---------------------------------------------------------------------------------------

    return lines


def show(args):
    options = "winget show " 
    if args.show_query:
        options += "\"" + args.show_query + "\"" + " "
    if args.id:
        options += " --id " + args.id + " "
    if args.name:
        options += " --name " + args.name + " "
    if args.tag:
        options += " --tag " + args.tag + " "
    if args.exact:
        options += " --exact "
    subproc = subprocess.run(
        options.strip(), capture_output=True, shell=True)
    # print(subproc.stdout.decode())
    return subproc.stdout.decode()

class Show_Args:
    def __init__(self, show_query, id, name, tag, exact) -> None:
        self.show_query = show_query
        self.id = id
        self.name = name
        self.tag = tag
        self.exact = exact


# installing a package with winget
def get_install_output(output_string: str):
    lines = output_string.split("\n")

    # this line here is needed for the case in which winget cannot search in a certain source
    lines = list(
        filter(lambda e: 'Failed when searching source' not in e, lines))
    # ---------------------------------------------------------------------------------------

    return lines

def install(args):
    options = "winget install --accept-source-agreements --accept-package-agreements " + \
        "\"" + args.install_query + "\"" + " "
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
    if args.scope:
        options += " --scope " + args.scope + " "
    if args.source:
        options += " --source " + args.source + " "
    if args.arhitecture:
        options += " --arhitecture " + args.arhitecture + " "
    if args.interactive:
        options += " --interactive "
    if args.silent and not args.interactive:
        options += " --silent "
    if args.override:
        options += " --override " + args.override + " "
    if args.disable_interactivity:
        options += " --disable-interactivity " 
    if args.location:
        options += " --location " + args.location + " "
    subproc = subprocess.run(
        options.strip(), capture_output=True, shell=True)
    # print("output: ", subproc.stdout.decode())
    return subproc.stdout.decode()

class Install_Args:
    def __init__(self, install_query, id=None, name=None, tag=None, exact=False, version=None,
                 scope=None, source=None, arhitecture=None, interactive=False, silent=False,
                 override=None, disable_interactivity=False, location=None):
        self.install_query = install_query
        self.id = id
        self.name = name
        self.tag = tag
        self.exact = exact
        self.version = version
        self.scope = scope
        self.source = source
        self.arhitecture = arhitecture
        self.interactive = interactive
        self.silent = silent
        self.override = override
        self.disable_interactivity = disable_interactivity
        self.location = location


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
    # print(options)
    subproc = subprocess.run(
        options.strip(), capture_output=True, shell=True)
    print("output: ", subproc.stdout.decode())

class Uninstaller_Args:
    def __init__(self, uninstall_query, id=None, name=None, tag=None,
                 exact=False, version=None, interactive=False,
                 silent=False, preserve=False, purge=False):
        self.uninstall_query = uninstall_query
        self.id = id
        self.name = name
        self.tag = tag
        self.exact = exact
        self.version = version
        self.interactive = interactive
        self.silent = silent
        self.preserve = preserve
        self.purge = purge

# getting bundles info
def get_bundle(args):
    if args.id:
        return db.get_bundle_by_id(args.id)
    if args.title:
        return db.get_bundle_by_title(args.title)
    if args.all:
        return db.get_all_bundles()

class Get_Bundle_Args:
    def __init__(self, all: bool, id=None, title=None, ) -> None:
        self.id = id
        self.title = title
        self.all = all
    
# creating bundle
def create_bundle(args):
    if args.title and args.description:
        if args.apps:
            return db.create_bundle(title=args.title, description=args.description, apps = args.apps)
        return db.create_bundle(title=args.title, description=args.description)
    
class Create_Bundle_Args:
    def __init__(self, title, description="", apps = None) -> None:
        self.title = title
        self.description = description
        self.apps = apps
    
# deleting bundle
def delete_bundle(args):
    if args.id:
        return db.delete_bundle(args.id)

class Delete_Args:
    def __init__(self, id=None):
        self.id = id

# updating bundle title
def update_bundle_title(args):
    if args.id and args.title:
        return db.update_bundle_title(args.id, args.title)
    
# adding applications to bundle
def add_application_to_bundle(args):
    if args.bundle_id and args.type and args.app:
        return db.add_app_to_bundle(args.bundle_id,args.type,args.app)

class Add_Application_To_Bundle_Args:
    def __init__(self, bundle_id=None, type=None, app=None) -> None:
        self.bundle_id = bundle_id
        self.type = type
        self.app = app

# removing applications from bundle
def remove_application_from_bundle(args):
    if args.bundle_id and args.type and args.id:
        return db.remove_app_from_bundle(args.bundle_id, args.type, args.id)
    
# exporting a bundle 
def export_bundle(args):
    if args.output and args.id:
        directory = os.path.realpath(os.path.dirname(__file__))
        content = json.dumps(db.get_bundle_by_id(args.id), indent=2)

        os.chdir(directory)
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        output_file = open(args.output, "w")
        output_file.write(content)
        output_file.close
        return {"status": "success", "message": "Operation completed successfully", "result": json.loads(content)}

class Export_Bundle_Args:
    def __init__(self, output: str, id) -> None:
        self.output = output
        self.id = id

# importing a bundle
def import_bundle(args):
    if args.file:
        directory = os.path.realpath(os.path.dirname(__file__))
        os.chdir(directory)
        with open(args.file, "r") as file:
            bundle = json.loads(file.read())
            file.close()
            return create_bundle(Create_Bundle_Args(bundle["title"], bundle["description"], bundle["apps"]))

class Import_Bundle_Args:
    def __init__(self, file) -> None:
        self.file = file


# bulk install 
def bundle_install(args):
    if not args.bundle_id:
        return
    bundles = db.get_bundle_by_id(args.bundle_id)
    winget_apps = bundles["apps"]["winget"]
    for app in winget_apps:
        print(install(Install_Args(app["name"],app["id"],source=app["source"])))
        print(f'{app["name"]} ({app["id"]}) installed')

class Bundle_Install_Args:
    def __init__(self, bundle_id = None) -> None:
        self.bundle_id = bundle_id




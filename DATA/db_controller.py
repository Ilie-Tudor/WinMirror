from pysondb import db as pydb
import os
from functional import seq
directory = os.path.realpath(os.path.dirname(__file__))
db=pydb.getDb(directory+"/db.json")


# The schema for the DB:
# {
    # data: [bundles[]]
# }

# bundle:{
#     id: string,
#     title: string,
#     apps: {
#         winget: [winget_app[]],
#         readonly: [readonly_app[]],
#     }
# }

# winget_app: {
#     name: string,
#     id: string
# }

# readonly_app:{
#     name: string,
#     url: string,
#     id: string
# }

def notNone(value,backup):
    if value is None:
        return backup
    else:
        return value

def create_bundle(title, apps = None):

    if len(db.getByQuery({"title": title}))>0:
        return {"status": "error", "message": "A bundle with the specified name already exists", "result": None}

    if apps:
        id = db.add({"title": title, "apps": {"winget": apps["winget"], "readonly": apps["readonly"]}})
        return {"status": "success", "message": "Operation completed successfully", "result": id}
    else:
        id = db.add({"title": title, "apps": {"winget": [], "readonly": []}})
        return {"status": "success", "message": "Operation completed successfully", "result": id}

def delete_bundle(id):
    if len(db.getByQuery({"id": id}))==0:
        return {"status": "error", "message": "Bundle not found", "result": None}
    success = db.deleteById(id)
    if not success:
        return {"status": "error", "message": "Couldn't delete button, please try again", "result": None}
    return {"status": "success", "message": "Operation completed successfully", "result": True}


def add_app_to_bundle(bundle_id, app_type, app):
    bundle = db.getByQuery({"id": bundle_id})[0]
    apps_object = bundle["apps"]
    if len(bundle)==0:
        return {"status": "error", "message": "Bundle not found", "result": None}
    if seq(bundle["apps"][app_type]).find(lambda elem: elem["id"] == app["id"])!=None:
        return {"status": "error", "message": "Application allready exists in bundle", "result": None}

    apps_array = apps_object[app_type]
    apps_array.append(app)
    
    db.updateById(bundle_id, {"apps": {**apps_object, app_type: apps_array}})
    return {"status": "success", "message": "Operation completed successfully", "result": db.getByQuery({"id": bundle_id})[0]}

def remove_app_from_bundle(bundle_id, app_type, app_id):
    bundle = db.getByQuery({"id": bundle_id})[0]
    apps_object = bundle["apps"]
    if len(bundle)==0:
        return {"status": "error", "message": "Bundle not found", "result": None}
    app = seq(bundle["apps"][app_type]).find(lambda elem: elem["id"] == app_id)
    if app==None:
        return {"status": "error", "message": "Application doesn't exists in bundle", "result": None}

    apps_array = apps_object[app_type]
    apps_array.remove(app)

    db.updateById(bundle_id, {"apps": {**apps_object, app_type: apps_array}})
    return {"status": "success", "message": "Operation completed successfully", "result": db.getByQuery({"id": bundle_id})[0]}


# print(create_bundle("hello2"))
# print(add_app_to_bundle(216011805207191901, "readonly", {"name": "Aplicatia mea", "url": "https://", "id": "myappid"}))
# print(remove_app_from_bundle(216011805207191901, "readonly", "myappid"))
print(delete_bundle(216011805207191901))

    



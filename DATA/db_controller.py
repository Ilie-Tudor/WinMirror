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
#     description: string,
#     apps: {
#         winget: [winget_app[]],
#         readonly: [readonly_app[]],
#     }
# }

# winget_app: {
#     name: string,
#     id: string,
#     source: string
# }

# readonly_app:{
#     name: string,
#     id: string
# }

def notNone(value,backup):
    if value is None:
        return backup
    else:
        return value

def create_bundle(title, description,  apps = None):
    if len(db.getByQuery({"title": title}))>0:
        return {"status": "error", "message": "A bundle with the specified title already exists", "result": None}
    if apps:
        id = db.add({"title": title, "description": description, "apps": {"winget": apps["winget"], "readonly": apps["readonly"]}})
        return {"status": "success", "message": "Operation completed successfully", "result": id}
    else:
        id = db.add({"title": title, "description": description, "apps": {"winget": [], "readonly": []}})
        return {"status": "success", "message": "Operation completed successfully", "result": id}

def delete_bundle(id):
    if len(db.getByQuery({"id": id}))==0:
        return {"status": "error", "message": "Bundle not found", "result": None}
    success = db.deleteById(id)
    if not success:
        return {"status": "error", "message": "Couldn't delete button, please try again", "result": None}
    return {"status": "success", "message": "Operation completed successfully", "result": True}

def add_app_to_bundle(bundle_id, app_type, app):
    bundle = db.getById(bundle_id)
    apps_object = bundle["apps"]
    if bundle is None:
        return {"status": "error", "message": "Bundle not found", "result": None}
    if seq(bundle["apps"][app_type]).find(lambda elem: elem["id"] == app["id"])!=None:
        return {"status": "error", "message": "Application allready exists in bundle", "result": None}

    apps_array = apps_object[app_type]
    apps_array.append(app)
    
    db.updateById(bundle_id, {"apps": {**apps_object, app_type: apps_array}})
    return {"status": "success", "message": "Operation completed successfully", "result": db.getById(bundle_id)}

def remove_app_from_bundle(bundle_id, app_type, app_id):
    bundle = db.getById(bundle_id)
    apps_object = bundle["apps"]
    if bundle is None:
        return {"status": "error", "message": "Bundle not found", "result": None}
    app = seq(bundle["apps"][app_type]).find(lambda elem: elem["id"] == app_id)
    if app==None:
        return {"status": "error", "message": "Application doesn't exists in bundle", "result": None}

    apps_array = apps_object[app_type]
    apps_array.remove(app)

    db.updateById(bundle_id, {"apps": {**apps_object, app_type: apps_array}})
    return {"status": "success", "message": "Operation completed successfully", "result": db.getById(bundle_id)}

def get_all_bundles():
    return db.getAll()

def get_bundle_by_id(id):
    return db.getById(id)

def get_bundle_by_title(title):
    return db.getByQuery({"title": title})

def update_bundle_title(id, newTitle):
    if len(db.getById(id))==0:
        return {"status": "error", "message": "Bundle not found", "result": None}
    db.updateById(id,{"title": newTitle})
    return {"status": "success", "message": "Operation completed successfully", "result": db.getById(id)}



    



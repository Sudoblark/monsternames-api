from flask import make_response, jsonify
import database.models as models
from peewee import fn

def return_name():
    # Connect to db
    models.db.connect(reuse_if_open=True)
    # Get random record
    names = models.GoatmenFirstName.select().order_by(fn.Rand()).limit(1)
    result = (names[0].firstName)
    # Disconnect from DB
    models.db.close()
    # Return json data
    return make_response(jsonify({'firstName' : result}), 200)

def insert_first_name(firstName, user):
    # Connect to db
    models.db.connect(reuse_if_open=True)
    # First check if the record already exists
    if (models.GoatmenFirstName.select().where(models.GoatmenFirstName.firstName == firstName)).exists():
        return make_response(jsonify({'error' : 'Duplicate record', 'message' : 'Record already exists'}), 400)
    # Insert
    models.GoatmenFirstName.create(firstName=firstName)
    models.PostAudit.create(user=user, message='GoatmenFirstName record "{0}" created'.format(firstName))
    models.db.commit()
    models.db.close()
    # Return success
    return make_response(jsonify({'firstName' : firstName, 'message' : 'New record created'}), 200)
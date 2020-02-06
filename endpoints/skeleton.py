from flask import make_response, jsonify
import database.models as models
from peewee import fn

def return_name():
    # Connect to db
    models.db.connect(reuse_if_open=True)
    # Get random record
    firstName = models.SkeletonFirstName.select().order_by(fn.Rand()).limit(1)
    lastName = models.SkeletonLastName.select().order_by(fn.Rand()).limit(1)
    
    firstName = firstName[0].firstName
    lastName = lastName[0].lastName
    # Disconnect from DB
    models.db.close()
    # Return json data
    return make_response(jsonify({'firstName' : firstName,
                                   'lastName' : lastName,
                                   'fullName' : '{0} {1}'.format(firstName, lastName)}), 200)

def insert_first_name(firstName, user):
    # Connect to db
    models.db.connect(reuse_if_open=True)
    # First check if the record already exists
    if (models.SkeletonFirstName.select().where(models.SkeletonFirstName.firstName == firstName)).exists():
        return make_response(jsonify({'error' : 'Duplicate record', 'message' : 'Record already exists'}), 400)
    # Insert
    models.SkeletonFirstName.create(firstName=firstName)
    models.PostAudit.create(user=user, message='SkeletonFirstName record "{0}" created'.format(firstName))
    models.db.commit()
    models.db.close()
    # Return success
    return make_response(jsonify({'firstName' : firstName, 'message' : 'New record created'}), 200)

def insert_last_name(lastName, user):
    # Connect to db
    models.db.connect(reuse_if_open=True)
    # First check if the record already exists
    if (models.SkeletonLastName.select().where(models.SkeletonLastName.lastName == lastName)).exists():
        return make_response(jsonify({'error' : 'Duplicate record', 'message' : 'Record already exists'}), 400)
    # Insert
    models.SkeletonLastName.create(lastName=lastName)
    models.PostAudit.create(user=user, message='SkeletonLastName record "{0}" created'.format(lastName))
    models.db.commit()
    models.db.close()
    # Return success
    return make_response(jsonify({'lastName' : lastName, 'message' : 'New record created'}), 200)
import os
import datetime
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from ..methods.rate_table import process_rate_table
from ..models import Model_ConfigRateTable
from ..schemas import Schema_ConfigRateTable

file_uploads = Blueprint('file_uploads', __name__)

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
ALLOWED_EXTENSIONS = {'txt', 'csv'}

_schema_rate_table = Schema_ConfigRateTable(many=True)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@file_uploads.route('/upload/rate-table', methods=["POST"])
def upload_rate_table():
    # check if the post request has the file part
    if 'file' not in request.files:
        return "No file in payload", 400
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return "No selected file", 400

    if file and allowed_file(file.filename):
        now = datetime.datetime.now() 
        # append timestamp to filename and secure it
        filename = secure_filename(now.strftime("%Y%m%d-%H%M%S-") + file.filename)

        # run validations on rate table data
        rate_tables_dict = process_rate_table(file)
        # load rate table models
        rate_tables = _schema_rate_table.load(rate_tables_dict)
        # write rate table data to DB
        Model_ConfigRateTable.save_all_to_db(rate_tables)

        # save file to local storage
        # must come after reading file
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        # return data
        return jsonify(_schema_rate_table.dump(rate_tables)), 200
    return "Uh oh, something went wrong...", 400

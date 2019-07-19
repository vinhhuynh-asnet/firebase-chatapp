from io import BytesIO
from flask import Flask, request, send_file
from google.cloud import storage
storage_client = storage.Client()

# Demo function download file from GCS
def download_file(request):
    bucket = storage_client.get_bucket('demo-gcs-sample')
    blob = bucket.get_blob('photo.jpeg')
    file = BytesIO(blob.download_as_string())
    return send_file(file,
        attachment_filename = blob.name,
        as_attachment=True,
        mimetype='image/jpeg')
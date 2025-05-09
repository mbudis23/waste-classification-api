import shutil

def save_upload_file(file, destination):
    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

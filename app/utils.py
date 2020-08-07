import os
import uuid


class FileUtils:

    @staticmethod
    def save_file(field, folder=''):
        if field:
            filename_original = field.data.filename
            ext = filename_original.split('.')[-1]

            filename_new = str(uuid.uuid4()) + '.' + ext

            field.data.save(os.path.join(current_app.config['BASE_DIR'], 'app/static/img/upload/' + folder, filename_new))

            return filename_new

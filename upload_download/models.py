from django.db import models
from django.forms import ValidationError
from datetime import datetime
from django.utils.deconstruct import deconstructible
from fatturazione.models import Fattura
from os.path import basename

@deconstructible
class UploadToPathAndRename(object):

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1].lower()
        new_filename = datetime.now().strftime("%Y%m%d_%H%M%S")
        return '{0}{1}.{2}'.format(self.sub_path, new_filename, ext)

class UploadFile (models.Model):
    name = models.FileField("Nome file", upload_to=UploadToPathAndRename('uploads/'), blank=False)
    created_date_time = models.DateTimeField("Creato", auto_now_add=True)

    def clean(self): 
        
        import zipfile
        import io

        # Get file extension, and if not present set it as None
        try:
            file_ext = self.name.name.split('.')[-1].lower()
        except:
            file_ext = None
        
        # Check if file has zip extension. If it does, check that it is a valid
        # zip file. If it is, check that it contains the right dbf files 
        if file_ext == None or file_ext != 'zip':         
            raise ValidationError('Stai cercando di caricare un file non valido. Seleziona un archivio .zip valido')
        else:
            try:
                with zipfile.ZipFile(io.BytesIO(self.name.file.read()), "r") as zip_file:
                    zip_file_list = [fil.lower() for fil in zip_file.namelist()]
                    db_list = ["anag.dbf", "fatt.dbf", "lfat.dbf"]
                    if not all(fil in zip_file_list for fil in db_list):
                        raise ValidationError("L'archivio .zip che stai cercando di caricare non contiene database validi")
            except zipfile.BadZipfile:
                raise ValidationError('Formato file invalido. Seleziona un archivio .zip valido')
            except ValidationError as err:
                raise err

    class Meta:
        verbose_name = 'file da caricare'
        verbose_name_plural = "files da caricare"

    def __str__(self):
        return str(basename(self.name.name))
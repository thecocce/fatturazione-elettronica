from django.db import models
from django.forms import ValidationError

class Cliente (models.Model):
    codana = models.CharField("Codice cliente", max_length=6, blank=True, null=True, unique=True)
    intest = models.CharField("Intestazione", max_length=10, blank=True, null=True)
    rsoc = models.CharField("Cliente", max_length=100, blank=True, null=True)
    codfis = models.CharField("Codice fiscale", max_length=16, blank=True, null=True)
    piva = models.CharField("Partita IVA", max_length=20, blank=True, null=True)
    indir = models.CharField("Indirizzo", max_length=40, blank=True, null=True)
    cap = models.CharField("CAP", max_length=5, blank=True, null=True)
    local = models.CharField("Località", max_length=35, blank=True, null=True)
    prov = models.CharField("Provincia", max_length=2, blank=True, null=True)
    nazione = models.CharField("Nazione", max_length=3, blank=True, null=True)
    allegiva = models.SmallIntegerField("Allegati IVA", blank=True, null=True)
    riferiment = models.CharField("Riferimento", max_length=30, blank=True, null=True)
    telef = models.CharField("Telefono", max_length=40, blank=True, null=True)
    fax = models.CharField("Fax", max_length=15, blank=True, null=True)
    ressec = models.CharField("Residenza secondaria", max_length=60, blank=True, null=True)
    datanasc = models.DateField("Data nascita", blank=True, null=True)
    luona = models.CharField("Luogo nascita", max_length=35, blank=True, null=True)
    provna = models.CharField("Provincia nascita", max_length=2, blank=True, null=True)
    indircor = models.CharField("Indirizzo corrispondente", max_length=40, blank=True, null=True)
    capcor = models.CharField("CAP corrispondente", max_length=5, blank=True, null=True)
    localcor = models.CharField("Località corrispondente", max_length=35, blank=True, null=True)
    provcor = models.CharField("Provincia corrispondente", max_length=2, blank=True, null=True)
    nazionecor = models.CharField("Nazione corrispondente",max_length=3, blank=True, null=True)
    note = models.CharField("Note", max_length=200, blank=True, null=True)
    indirizzo_pec = models.EmailField("Indirizzo PEC", max_length=254, blank=True, null=True, default=None)
    codice_univoco = models.CharField("Codice univoco", max_length=10, blank=True, null=True, default=None)

    class Meta:
        verbose_name = 'cliente'
        verbose_name_plural = 'clienti'

    def clean(self):
        
        if self.codice_univoco:
            if len(self.codice_univoco) != 7:
                raise ValidationError('Il codice univoco deve avere 7 caratteri')

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        
        if self.codice_univoco:
            self.codice_univoco = self.codice_univoco.strip().upper()
        if self.indirizzo_pec:
            self.indirizzo_pec = self.indirizzo_pec.strip()
        super(Cliente, self).save(force_insert, force_update, *args, **kwargs)

    def __str__(self):
        return str(self.codana + " - " + self.rsoc)

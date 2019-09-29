from django.db import models

class Cedente (models.Model):

    denominazione = models.CharField("Denominazione", max_length=254, blank=False)
    indirizzo = models.CharField("Indirizzo", max_length=254, blank=False)
    cap = models.CharField("CAP", max_length=10, blank=False)
    comune = models.CharField("Comune", max_length=254, blank=False)
    provincia = models.CharField("Provincia", max_length=2, blank=False)
    nazione = models.CharField("Nazione", max_length=2, blank=False)
    regime_fiscale = models.CharField("Regime Fiscale", max_length=10, blank=False)
    partita_iva = models.CharField("Partita Iva", max_length=20, blank=False)
    indirizzo_pec = models.EmailField("Indirizzo PEC", max_length=254, blank=True)
    indirizzo_email_commerciale = models.EmailField("Indirizzo email commerciale", max_length=254, blank=True)
    codice_fiscale = models.CharField("Codice fiscale", max_length=20, blank=True)
    codice_univoco = models.CharField("Codice univoco", max_length=10, blank=True)
    numero_telefono = models.CharField("Telefono", max_length=20, blank=True)

    class Meta:
        verbose_name = 'informazione cedente'
        verbose_name_plural = 'informazione cedenti'

    def __str__(self):
        return str(self.id)
    
    def save(self, force_insert=False, force_update=False):
        
        self.denominazione = self.denominazione.strip().upper()
        self.indirizzo = self.indirizzo.strip().upper()
        self.cap = self.cap.strip().upper()
        self.comune = self.comune.strip().upper()
        self.provincia = self.provincia.strip().upper()
        self.nazione = self.nazione.strip().upper()
        self.regime_fiscale = self.regime_fiscale.strip().upper()
        self.partita_iva = self.partita_iva.strip().upper()
        self.codice_univoco = self.codice_univoco.strip().upper()
        self.codice_fiscale = self.codice_fiscale.strip().upper()
        self.indirizzo_email_commerciale = self.indirizzo_email_commerciale.strip()
        self.indirizzo_pec = self.indirizzo_pec.strip()
        self.numero_telefono = self.numero_telefono.strip()
        super(Cedente, self).save(force_insert, force_update)

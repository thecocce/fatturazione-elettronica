from django.db import models
from anagrafe.models import Cliente

class Fattura (models.Model):
    tdoc = models.CharField("Causale", max_length=20, blank=True, null=True)
    nrdoc = models.CharField("Numero documento", max_length=8, blank=True, null=True)
    ddoc = models.DateField("Data documento", blank=True, null=True)
    codana = models.ForeignKey(Cliente, verbose_name="Cliente", null=True)
    stato = models.CharField(max_length=1, blank=True, null=True)
    mopag = models.CharField("Modalità pagamento", max_length=5, blank=True, null=True)
    bappoggio = models.CharField("Banca d'appoggio", max_length=10, blank=True, null=True)
    speseboll = models.CharField("Spese bollo", max_length=1, blank=True, null=True)
    bolli = models.PositiveSmallIntegerField(blank=True, null=True)
    tpsconto = models.CharField("Tipo sconto", max_length=1, blank=True, null=True)
    percsconto = models.DecimalField("Percentual sconto", max_digits=4, decimal_places=2, blank=True, null=True)
    sconto = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    listino = models.CharField(max_length=5, blank=True, null=True)
    coddes = models.CharField("Codice listino", max_length=6, blank=True, null=True)
    rsoc = models.CharField("Ragione sociale", max_length=40, blank=True, null=True)
    indirizzo = models.CharField(max_length=40, blank=True, null=True)
    localita = models.CharField("Località", max_length=40, blank=True, null=True)
    provincia = models.CharField(max_length=2, blank=True, null=True)
    agente = models.CharField(max_length=6, blank=True, null=True)
    cprovv = models.CharField("Codice provvigione", max_length=5, blank=True, null=True)
    provv = models.DecimalField("Provvigione",max_digits=14, decimal_places=2, blank=True, null=True)
    tprovv = models.CharField("Tipo provvigione", max_length=1, blank=True, null=True)
    percprovv = models.DecimalField("Percentuale provvigione", max_digits=4, decimal_places=2, blank=True, null=True)
    pariva = models.CharField("IVA", max_length=3, blank=True, null=True)
    valuta = models.CharField(max_length=5, blank=True, null=True)
    cambio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    note = models.CharField(max_length=40, blank=True, null=True)
    aspetto = models.CharField(max_length=40, blank=True, null=True)
    colli = models.CharField(max_length=10, blank=True, null=True)
    tporto = models.CharField("Tipo trasporto", max_length=40, blank=True, null=True)
    amezzo = models.CharField("Vettore", max_length=1, blank=True, null=True)
    vcoddes = models.CharField("Codice vettore", max_length=6, blank=True, null=True)
    vrsoc = models.CharField("Ragione sociale vettore", max_length=40, blank=True, null=True)
    vindirizzo = models.CharField("Indirizzo vettore", max_length=40, blank=True, null=True)
    vlocalita = models.CharField("Località vettore", max_length=40, blank=True, null=True)
    vprovincia = models.CharField("Provincia vettore", max_length=2, blank=True, null=True)
    data = models.DateField(blank=True, null=True)
    ora = models.TimeField(blank=True, null=True)
    acconto = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    tcautr = models.CharField(max_length=5, blank=True, null=True)
    cautr = models.CharField(max_length=40, blank=True, null=True)
    gendoc = models.PositiveSmallIntegerField(blank=True, null=True)
    gencon = models.PositiveSmallIntegerField("Generazione documento", blank=True, null=True)
    genmag = models.PositiveSmallIntegerField(blank=True, null=True)
    comm = models.CharField(max_length=7, blank=True, null=True)
    pvaluta = models.DateField(blank=True, null=True)
    campo1 = models.CharField(max_length=20, blank=True, null=True)
    campo2 = models.CharField(max_length=20, blank=True, null=True)
    campo3 = models.CharField(max_length=20, blank=True, null=True)
    campo4 = models.CharField(max_length=20, blank=True, null=True)
    campo5 = models.CharField(max_length=20, blank=True, null=True)
    campo6 = models.CharField(max_length=20, blank=True, null=True)
    campo7 = models.CharField(max_length=20, blank=True, null=True)
    campo8 = models.CharField(max_length=20, blank=True, null=True)
    campo9 = models.CharField(max_length=20, blank=True, null=True)
    campo10 = models.CharField(max_length=20, blank=True, null=True)
    psconto1 = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    psconto2 = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    psconto3 = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = 'fattura'
        verbose_name_plural = 'fatture'

    def __str__(self):
        return str(self.id)

class ElementoFattura (models.Model):
    lnummov = models.ForeignKey(Fattura, verbose_name="Numero movimento", null=True)
    nrr = models.PositiveSmallIntegerField("Numero",blank=True, null=True)
    codart = models.CharField("Codice articolo", max_length=15, blank=True, null=True)
    codmag = models.CharField("Codice magazzino", max_length=8, blank=True, null=True)
    descri = models.CharField("Descrizione",max_length=40, blank=True, null=True)
    um = models.CharField("Unità di misura", max_length=2, blank=True, null=True)
    qto = models.FloatField("Quantità", blank=True, null=True)
    prezzo = models.FloatField("Prezzo", blank=True, null=True)
    tsconto = models.CharField("Tipo sconto", max_length=1, blank=True, null=True)
    sconto1 = models.DecimalField("Percentuale sconto 1", max_digits=14, decimal_places=2, blank=True, null=True)
    percsc2 = models.DecimalField("Percentuale sconto 2", max_digits=4, decimal_places=2, blank=True, null=True)
    percsc3 = models.DecimalField("Percentuale sconto 2", max_digits=4, decimal_places=2, blank=True, null=True)
    iva = models.CharField("IVA", max_length=3, blank=True, null=True)
    lagente = models.CharField("Agente", max_length=6, blank=True, null=True)
    ltprovv = models.CharField("Provvigione agente 1", max_length=1, blank=True, null=True)
    lcprovv = models.CharField("Provvigione agente 2", max_length=5, blank=True, null=True)
    lprovv = models.DecimalField("Provvigione agente 3", max_digits=11, decimal_places=2, blank=True, null=True)
    note = models.CharField("Note", max_length=20, blank=True, null=True)
    prezzoe = models.DecimalField(max_digits=15, decimal_places=6, blank=True, null=True)
    genmag = models.PositiveSmallIntegerField(blank=True, null=True)
    marca = models.CharField(max_length=15, blank=True, null=True)
    ndis = models.CharField(max_length=15, blank=True, null=True)
    collaudo = models.CharField(max_length=2, blank=True, null=True)
    nscostru = models.CharField(max_length=10, blank=True, null=True)
    posc = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'elemento fattura'
        verbose_name_plural = 'elementi fattura'

    def __str__(self):
        return str(self.id)
    
    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        
        if self.um:
            self.um = self.um.replace("ø", ".")
        super(ElementoFattura, self).save(force_insert, force_update, *args, **kwargs)
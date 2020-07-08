from fatturazione.models import ElementoFattura, AliquotaIva

for e in ElementoFattura.objects.filter(iva__isnull=False):
    try:
        ese = AliquotaIva.objects.get(codice_iva=e.iva.upper())
        e.esenzione_iva = ese
    except:
        e.esenzione_iva = None
    e.save()

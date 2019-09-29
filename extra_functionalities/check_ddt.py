from fatturazione.models import Fattura
from dateutil import parser 

for fattura in Fattura.objects.all():
    for elemento_fattura in fattura.elementofattura_set.filter(iva__isnull=True, codart__isnull=True, descri__icontains="Rif. DDT"):
        try:
            ddt_ref = " ".join(elemento_fattura.descri.split())
            ddt_ref_split = ddt_ref.split()
            ddt_ref_numero = ddt_ref_split[2].split(".")[1]
            ddt_ref_data = parser.parse(ddt_ref_split[4], dayfirst=True)
        except:
            print(fattura.id, elemento_fattura.descri)
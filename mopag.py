from fatturazione.models import ModalitaPagamento, Fattura

for f in Fattura.objects.all():
    try:
        mopag = ModalitaPagamento.objects.get(codice_pagamento=f.mopag)
        f.mopag_nuova = mopag
    except:
        f.mopag_nuova = None
        print(f.id, f.mopag)
    f.save()
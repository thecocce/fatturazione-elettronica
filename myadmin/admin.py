from django.contrib import admin
from django.utils.translation import ugettext as _, ugettext_lazy
from admin_view_permission.admin import AdminViewPermissionAdminSite
from django.utils.safestring import mark_safe
import string
import random

from djangoql.admin import DjangoQLSearchMixin
from djangoql.schema import DjangoQLSchema

def id_generator(size=5, chars=string.ascii_uppercase + string.digits):
    """Generates a random 5-character-long string"""

    return ''.join(random.choice(chars) for _ in range(size))

def isint(value):
    """Check if number is int"""
    try:
        int(value)
        return True
    except ValueError:
        return False

def change_cpu_governor(governor):
    """Changes the CPU governor of my odroid. Default is powersave!"""
    import subprocess

    try:
        result = subprocess.check_output('odroid-cpu-control -s -g "{}"'.format(governor), shell=True)
    except:
        pass

class MyAdminSite(AdminViewPermissionAdminSite):
    
    '''Create a custom admin site called MyAdminSite'''
    
    # Text to put at the end of each page's <title>.
    site_title = ugettext_lazy('Fatturazione elettronica')

    # Text to put in each page's <h1>.
    site_header = ugettext_lazy('Fatturazione elettronica')

    # Text to put at the top of the admin index page.
    index_title = ugettext_lazy('Home')

    # URL for the "View site" link at the top of each admin page.
    site_url = '/'
    
    def get_urls(self):
        from django.conf.urls import url
        urls = super(MyAdminSite, self).get_urls()
        # Note that custom urls get pushed to the list (not appended)
        # This doesn't work with urls += ...
        urls = [
            url(r'media/(?P<url_path>.*)$', self.admin_view(self.downloads)),
        ] + urls
        return urls

    def downloads(self, request, *args, **kwargs):
        """Protected view for uploads/media files"""

        from django.http import HttpResponse
        from django.http import Http404
        import mimetypes
        import os
        
        response = HttpResponse()
        url_path = str(kwargs["url_path"])
        mimetype, encoding = mimetypes.guess_type(url_path)
        mimetype = mimetype if mimetype else 'application/octet-stream'
        response["Content-Type"] = mimetype
        if encoding:
            response["Content-Encoding"] = encoding
        response['X-Accel-Redirect'] = "/protected_media/{url_path}".format(url_path=url_path)
        file_name = os.path.basename(url_path)
        response["Content-Disposition"] = "attachment; filename={download_file_name}".format(download_file_name=file_name)

        return response
        
# Instantiate custom admin site 
my_admin_site = MyAdminSite()

# Disable delete selected action
my_admin_site.disable_action('delete_selected')

# User/Group admin

from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import GroupAdmin, UserAdmin
my_admin_site.register(Group, GroupAdmin)
my_admin_site.register(User, UserAdmin)

# Anagrafe admin

from anagrafe.models import Cliente

class ClienteQLSchema(DjangoQLSchema):
    '''Customize search functionality'''
    
    def get_fields(self, model):
        ''' Define fields that can be searched'''
        
        if model == Cliente:
            return ['codana', 'rsoc', 'piva', 'indir', 'cap','local', 
            'prov', 'nazione', 'note', 'codice_univoco', 'indirizzo_pec']
        return super(ClienteQLSchema, self).get_fields(model)

class ClientAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = ('codana', 'rsoc', 'indirizzo_completo',)
    list_display_links = ('codana', )
    ordering = ['codana']
    djangoql_schema = ClienteQLSchema
    list_per_page = 25

    def get_readonly_fields(self, request, obj=None):
        
        return ['codana', 'rsoc', 'piva', 'indir', 'cap','local', 
            'prov', 'nazione', 'allegiva', 'telef', 'fax', 'note',]

    def change_view(self,request,object_id,extra_content=None):
        
        self.fields = ('codana', 'rsoc', 'piva', 'indir', 'cap','local', 
        'prov', 'nazione', 'allegiva', 'telef', 'fax', 'note', 'indirizzo_pec', 'codice_univoco')
        return super(ClientAdmin,self).change_view(request,object_id)

    def indirizzo_completo(self, instance):
        """Custom list_view field to show the full address of a client"""

        strings = [instance.indir, instance.cap, instance.local, instance.prov, instance.nazione]
        return ", ".join(filter(None, strings))
    indirizzo_completo.short_description = 'indirizzo'

my_admin_site.register(Cliente, ClientAdmin)

# Esenzione IVA admin

from fatturazione.models import AliquotaIva

class AliquotaIVAAdmin(admin.ModelAdmin):
    list_display = ('codice_iva', 'perc_iva', 'natura_esenzione', 'riferimento_normativo', 'riferimento_normativo_cliente')
    list_display_links = ('codice_iva', )
    list_per_page = 25
    ordering = ('codice_iva',)

    def add_view(self, request, form_url='', extra_context=None):

        self.fields = ('codice_iva', 'perc_iva', 'natura_esenzione', 'riferimento_normativo', 'riferimento_normativo_cliente')
        return super(AliquotaIVAAdmin, self).add_view(request, form_url, extra_context=extra_context)

    def change_view(self,request,object_id,extra_content=None):
        
        self.fields = ('codice_iva', 'perc_iva', 'natura_esenzione', 'riferimento_normativo', 'riferimento_normativo_cliente')
        return super(AliquotaIVAAdmin,self).change_view(request,object_id)

    def get_queryset(self, request):

        return super(AliquotaIVAAdmin, self).get_queryset(request).exclude(perc_iva__isnull=True)

my_admin_site.register(AliquotaIva, AliquotaIVAAdmin)


# Modalita' pagamento

from fatturazione.models import ModalitaPagamento

class ModalitaPagamentoAdmin(admin.ModelAdmin):
    list_display = ('codice_pagamento', 'n_giorni_scadenza', 'codice_pagamento_fattura_elettronica')
    list_display_links = ('codice_pagamento', )
    list_per_page = 25
    ordering = ('codice_pagamento',)

    def add_view(self, request, form_url='', extra_context=None):

        self.fields = ('codice_pagamento', 'n_giorni_scadenza', 'codice_pagamento_fattura_elettronica')
        return super(ModalitaPagamentoAdmin, self).add_view(request, form_url, extra_context=extra_context)

    def change_view(self,request,object_id,extra_content=None):
        
        self.fields = ('codice_pagamento', 'n_giorni_scadenza', 'codice_pagamento_fattura_elettronica')
        return super(ModalitaPagamentoAdmin,self).change_view(request,object_id)

    def get_queryset(self, request):

        return super(ModalitaPagamentoAdmin, self).get_queryset(request).exclude(attivo=False)

my_admin_site.register(ModalitaPagamento, ModalitaPagamentoAdmin)

# Fatturazione admin

from fatturazione.models import Fattura
from fatturazione.models import ElementoFattura

class FatturaQLSchema(DjangoQLSchema):
    '''Customize search functionality'''
    
    def get_fields(self, model):
        ''' Define fields that can be searched'''
        
        if model == Fattura:
            return ['id', 'ddoc', 'codana']
        elif model == Cliente:
            return ['codana']
        return super(FatturaQLSchema, self).get_fields(model)

class ElementoFatturaInline(admin.TabularInline):
    model = ElementoFattura
    verbose_name_plural = "Elementi Fattura"
    extra = 0
    fields = ['codart',	'descri', 'um', 'qto', 'prezzo', 'iva']

class FatturaAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = ('id', 'nrdoc', 'ddoc', 'codana',)
    list_display_links = ('id', )
    list_per_page = 25
    djangoql_schema = FatturaQLSchema
    inlines = [ElementoFatturaInline]
    actions = ['esporto_fattura_elettronica']

    def get_readonly_fields(self, request, obj=None):
        
        if obj:
            return ['codana',]
    
    def change_view(self,request,object_id,extra_content=None):
        
        self.fields = ('tdoc', 'nrdoc', 'ddoc', 'codana', 'stato', 'mopag', 'bappoggio','speseboll',)
        return super(FatturaAdmin,self).change_view(request,object_id)

    def importo_totale(self, instance):

        """Custom list-view field to show the total value of an invoice"""

        elementi_fattura = ElementoFattura.objects.filter(lnummov=instance.id, iva__perc_iva__isnull=False)
        sum = 0.0
        for elemento_fattura in elementi_fattura:
            if elemento_fattura.iva.upper() not in ['8C', '8A','41','36','74', "15", '10']:
                sum = sum + elemento_fattura.qto * elemento_fattura.prezzo * (float(elemento_fattura.iva)/100+1)
            else:
                sum = sum + elemento_fattura.qto * elemento_fattura.prezzo
        return "{0:.2f}".format(sum)
    importo_totale.short_description = 'Totale (€)'

    def esporto_fattura_elettronica(self, request, queryset):
        
        """Action to generate an xml version of an invoice according to
        FatturaPA ver 1.2.1  """

        import time
        import datetime
        from dateutil import parser
        from lxml import etree as ET
        from spine.settings import STATIC_ROOT, BASE_DIR
        from info_cedente.models import Cedente
        import os
        import zipfile
        from django.http import HttpResponse
        from django.http import HttpResponseServerError

        def isfloat(value):
            """Check if number is float"""
            try:
                float(value)
                return True
            except ValueError:
                return False

        def create_SubElement(parent, tag, attrib={}, txt=None, nsmap=None,**_extra):
            """Creates subelement from parent element"""

            from lxml import etree as ET
            result = ET.SubElement(parent, tag, attrib, None,**_extra)
            result.text = txt
            return result
        
        def last_day_of_month(any_day):
            """Given x days after invoice date period, get the last day of the month"""

            next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
            return next_month - datetime.timedelta(days=next_month.day)

        # Crank up the CPU governor for faster performance
        change_cpu_governor("performance")

        # Get cedente, only one is available and allowed so id is 1
        cedente = Cedente.objects.get(id=1)
        download_file_prefix = '{}{}'.format(cedente.nazione, cedente.partita_iva)

        # Create HTTP response
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="{}_{}.zip'.format(download_file_prefix, id_generator())
        
        # Generate zip file
        with zipfile.ZipFile(response, "w", zipfile.ZIP_DEFLATED) as zip_file:

            for fattura in queryset:
                
                # Root of the XML file
                string_root = '<p:FatturaElettronica \
                xmlns:ds="http://www.w3.org/2000/09/xmldsig#" \
                xmlns:p="http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2" \
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" versione="FPR12" \
                xsi:schemaLocation="http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2 http://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.2/Schema_del_file_xml_FatturaPA_versione_1.2.xsd"> \
                </p:FatturaElettronica>'
                root = ET.fromstring(string_root)

                # Header
                header = ET.SubElement(root, "FatturaElettronicaHeader")

                dati_trasmissione = ET.SubElement(header, "DatiTrasmissione")
                cedente_prestatore = ET.SubElement(header, "CedentePrestatore")
                cessionario_committente = ET.SubElement(header, "CessionarioCommittente")

                ## Dati trasmissione
                id_trasmittente = ET.SubElement(dati_trasmissione, "IdTrasmittente")
                id_paese = create_SubElement(id_trasmittente, "IdPaese", txt = cedente.nazione)
                id_codice = create_SubElement(id_trasmittente, "IdCodice", txt = cedente.partita_iva)

                progressivo_invio = create_SubElement(dati_trasmissione, "ProgressivoInvio", txt = str(fattura.id))
                formato_trasmissione = create_SubElement(dati_trasmissione, "FormatoTrasmissione", txt = "FPR12")
                
                if fattura.codana.codice_univoco:
                    codice_destinatario = create_SubElement(dati_trasmissione, "CodiceDestinatario", txt = fattura.codana.codice_univoco)
                else:
                    codice_destinatario = create_SubElement(dati_trasmissione, "CodiceDestinatario", txt = "0000000")

                contatti_trasmittente = create_SubElement(dati_trasmissione, "ContattiTrasmittente")
                trasmittente_telefono = create_SubElement(contatti_trasmittente, "Telefono", txt = cedente.numero_telefono)
                trasmittente_email = create_SubElement(contatti_trasmittente, "Email", txt = cedente.indirizzo_email_commerciale)
                
                if fattura.codana.indirizzo_pec:
                    pec_destinatario = create_SubElement(dati_trasmissione, "PECDestinatario", txt = fattura.codana.indirizzo_pec) 

                ## Cedente Prestatore
                prestatore_dati_anagrafici = ET.SubElement(cedente_prestatore, "DatiAnagrafici")
                prestatore_id_iva = ET.SubElement(prestatore_dati_anagrafici, "IdFiscaleIVA")
                prestatore_id_paese = create_SubElement(prestatore_id_iva, "IdPaese", txt = cedente.nazione)
                prestatore_id_codice = create_SubElement(prestatore_id_iva, "IdCodice", txt = cedente.partita_iva)
                prestatore_anagrafica = ET.SubElement(prestatore_dati_anagrafici, "Anagrafica")
                prestatore_denominazione = create_SubElement(prestatore_anagrafica, "Denominazione", txt = cedente.denominazione)
                prestatore_regime_fiscale = create_SubElement(prestatore_dati_anagrafici, "RegimeFiscale", txt = cedente.regime_fiscale)
                prestatore_sede = ET.SubElement(cedente_prestatore, "Sede")
                prestatore_indirizzo = create_SubElement(prestatore_sede, "Indirizzo", txt= cedente.indirizzo)
                prestatore_cap = create_SubElement(prestatore_sede, "CAP", txt = cedente.cap)
                prestatore_comune = create_SubElement(prestatore_sede, "Comune", txt = cedente.comune)
                prestatore_provincia = create_SubElement(prestatore_sede, "Provincia", txt = cedente.provincia)
                prestatore_nazione = create_SubElement(prestatore_sede, "Nazione", txt = cedente.nazione)

                ## Cessionario commitente
                commitente_dati_anagrafici = ET.SubElement(cessionario_committente, "DatiAnagrafici")
                if fattura.codana.piva:
                    commitente_id_iva = ET.SubElement(commitente_dati_anagrafici, "IdFiscaleIVA")
                    commitente_id_paese = create_SubElement(commitente_id_iva, "IdPaese", txt = fattura.codana.nazione.upper() if fattura.codana.nazione else "IT")
                    commitente_id_codice = create_SubElement(commitente_id_iva, "IdCodice", txt = fattura.codana.piva.upper())
                else:
                    if fattura.codana.codfis:
                        commitente_codice_fiscale = create_SubElement(commitente_dati_anagrafici, "CodiceFiscale", txt = fattura.codana.codfis.upper())
                commitente_anagrafica = ET.SubElement(commitente_dati_anagrafici, "Anagrafica")
                commitente_denominazione = create_SubElement(commitente_anagrafica, "Denominazione", txt = fattura.codana.rsoc.upper())
                commitente_sede = ET.SubElement(cessionario_committente, "Sede")
                commitente_indirizzo = create_SubElement(commitente_sede, "Indirizzo", txt = fattura.codana.indir.upper())
                commitente_cap = create_SubElement(commitente_sede, "CAP", txt = fattura.codana.cap.upper() if fattura.codana.cap else "ND")
                commitente_comune = create_SubElement(commitente_sede, "Comune", txt = fattura.codana.local.upper())
                commitente_provincia = create_SubElement(commitente_sede, "Provincia", txt = fattura.codana.prov.upper() if fattura.codana.prov else "ND")
                commitente_nazione = create_SubElement(commitente_sede, "Nazione", txt = fattura.codana.nazione.upper() if fattura.codana.nazione else "IT")

                #Body
                body = ET.SubElement(root, "FatturaElettronicaBody")

                ## Dati generali
                dati_generali = ET.SubElement(body, "DatiGenerali")
                dati_beni_servizi = ET.SubElement(body, "DatiBeniServizi")
                dati_pagamento = ET.SubElement(body, "DatiPagamento")

                ### Dati generali documento
                documento_dati_generali = ET.SubElement(dati_generali, "DatiGeneraliDocumento")
                if fattura.tdoc == 'NC':
                    documento_tipo = create_SubElement(documento_dati_generali, "TipoDocumento", txt = "TD04")
                else:
                    documento_tipo = create_SubElement(documento_dati_generali, "TipoDocumento", txt = "TD01")
                documento_divisa = create_SubElement(documento_dati_generali, "Divisa", txt = "EUR")
                documento_data = create_SubElement(documento_dati_generali, "Data", txt = fattura.ddoc.strftime('%Y-%m-%d'))
                documento_numero = create_SubElement(documento_dati_generali, "Numero", txt = fattura.nrdoc.upper())

                ### Dati DDT
                for elemento_fattura in fattura.elementofattura_set.filter(iva__perc_iva__isnull=True, codart__isnull=True, descri__icontains="Rif. DDT"):
                    try:
                        ddt_ref = " ".join(elemento_fattura.descri.split())
                        ddt_ref_split = ddt_ref.split()
                        ddt_ref_numero = ddt_ref_split[2].split(".")[1]
                        ddt_ref_data = parser.parse(ddt_ref_split[4], dayfirst=True)
                    except:
                        continue
                    else:
                        ddt_dati = ET.SubElement(dati_generali, "DatiDDT")
                        ddt_numero = create_SubElement(ddt_dati, "NumeroDDT", txt = ddt_ref_numero)
                        ddt_data = create_SubElement(ddt_dati, "DataDDT", txt = ddt_ref_data.strftime('%Y-%m-%d'))

                ## Dati beni servizi
                i = 1
                riepilogo_somme = {}
                for elemento_fattura in fattura.elementofattura_set.filter(iva__perc_iva__isnull=False):
                    linea_dettaglio = ET.SubElement(dati_beni_servizi, "DettaglioLinee")
                    linea_numero = create_SubElement(linea_dettaglio, "NumeroLinea", txt = str(i))
                    linea_descrizione = create_SubElement(linea_dettaglio, "Descrizione", txt = "Art. {} - {}".format(elemento_fattura.codart, elemento_fattura.descri).upper()[:1000] if elemento_fattura.codart else elemento_fattura.descri.upper()[:1000])
                    if elemento_fattura.descri:
                        if elemento_fattura.descri.lower() != "spese bancarie":
                            linea_quantita = create_SubElement(linea_dettaglio, "Quantita", txt = "{0:.2f}".format(elemento_fattura.qto))
                            linea_unita_misura = create_SubElement(linea_dettaglio, "UnitaMisura", txt = elemento_fattura.um.upper() if elemento_fattura.um else "ND")
                    
                    if len(str(elemento_fattura.prezzo).split(".")[-1]) >= 3:
                        linea_prezzo_unitario = create_SubElement(linea_dettaglio, "PrezzoUnitario", txt = str(elemento_fattura.prezzo))
                    else:
                        linea_prezzo_unitario = create_SubElement(linea_dettaglio, "PrezzoUnitario", txt = "{0:.2f}".format(elemento_fattura.prezzo))
                    
                    prezzo_totale = elemento_fattura.qto * elemento_fattura.prezzo
                    linea_prezzo_totale = create_SubElement(linea_dettaglio, "PrezzoTotale", txt = "{0:.2f}".format(prezzo_totale))
                    iva = elemento_fattura.iva
                    riepilogo_somme[iva.codice_iva] = riepilogo_somme.get(iva.codice_iva, 0) + prezzo_totale
                    
                    linea_aliquota_iva = create_SubElement(linea_dettaglio, "AliquotaIVA", txt = "{0:.2f}".format(float(iva.perc_iva)))
                    if iva.natura_esenzione:
                        linea_natura = create_SubElement(linea_dettaglio, "Natura", txt = iva.natura_esenzione)
                    
                    i = i + 1 

                ### Riepilogo
                importo_totale = 0.0
                for codice_iva, importo in riepilogo_somme.items():
                    iva = AliquotaIva.objects.get(codice_iva=codice_iva)
                    
                    riepilogo_dati = ET.SubElement(dati_beni_servizi, "DatiRiepilogo")

                    riepilogo_aliquota_iva = create_SubElement(riepilogo_dati, "AliquotaIVA", txt = "{0:.2f}".format(iva.perc_iva))
                    if iva.natura_esenzione:
                        linea_natura = create_SubElement(riepilogo_dati, "Natura", txt = iva.natura_esenzione)

                    riepilogo_imponibile_importo = create_SubElement(riepilogo_dati, "ImponibileImporto", txt = "{0:.2f}".format(importo))
                    imposta = float(iva.perc_iva)/100*importo
                    importo_totale = importo_totale + importo + imposta
                    riepilogo_imposta = create_SubElement(riepilogo_dati, "Imposta", txt = "{0:.2f}".format(imposta))
                    if iva.riferimento_normativo:
                        if iva.riferimento_normativo_cliente and fattura.codana.riferiment:
                            riferimento_normativo = iva.riferimento_normativo + ', ' + fattura.codana.riferiment
                        else:
                            riferimento_normativo = iva.riferimento_normativo
                        
                        riferimento_normativo = create_SubElement(riepilogo_dati, "RiferimentoNormativo", txt = riferimento_normativo)

                ## Dati pagamento

                pagamento_condizioni = create_SubElement(dati_pagamento, "CondizioniPagamento", txt = "TP02")
                pagamento_dettaglio = ET.SubElement(dati_pagamento, "DettaglioPagamento")

                pagamento_madalita = create_SubElement(pagamento_dettaglio, "ModalitaPagamento", txt = fattura.mopag.codice_pagamento_fattura_elettronica)
                scadenza = fattura.ddoc + datetime.timedelta(days=fattura.mopag.n_giorni_scadenza)

                scadenza = last_day_of_month(scadenza)
                pagamento_scadenza = create_SubElement(pagamento_dettaglio, "DataScadenzaPagamento", txt = scadenza.strftime('%Y-%m-%d'))

                pagamento_importo = create_SubElement(pagamento_dettaglio, "ImportoPagamento", txt = "{0:.2f}".format(importo_totale))

                documento_import_totale = create_SubElement(documento_dati_generali, "ImportoTotaleDocumento", txt = "{0:.2f}".format(importo_totale))

                if fattura.tdoc == 'NC':
                    documento_causale = create_SubElement(documento_dati_generali, "Causale", txt = "Nota accredito")
                elif fattura.tdoc == 'FV':
                    documento_causale = create_SubElement(documento_dati_generali, "Causale", txt = "Fattura vendita")

                xslt = ET.parse(STATIC_ROOT + 'xml/fatturaordinaria_v1.2.1.xsl')
                transform = ET.XSLT(xslt)
            
                zip_file.writestr('{}_{}.xml'.format(download_file_prefix, fattura.id), '<?xml version="1.0" encoding="UTF-8" ?>' + ET.tostring(root, encoding = "unicode"))
                zip_file.writestr('{}_{}.html'.format(download_file_prefix, fattura.id), ET.tostring(transform(root), encoding = "unicode"))
        
        change_cpu_governor("powersave")

        return response
    esporto_fattura_elettronica.short_description = "Esporta selezionati come fatture elettroniche"

class ElementoFatturaAdmin(admin.ModelAdmin):
    list_display = ('id','lnummov', 'codart', 'descri',	'um', 'qto', 'prezzo')
    list_display_links = ('id', )
    list_per_page = 25

    def get_model_perms(self, request):
        if not request.user.is_superuser:
            return {}
        return super(ElementoFatturaAdmin, self).get_model_perms(request)

my_admin_site.register(Fattura, FatturaAdmin)
# my_admin_site.register(ElementoFattura, ElementoFatturaAdmin)

# Uploads and downloads admin

from upload_download.models import UploadFile
# from upload_download.models import DownloadFile

class UploadAdmin(admin.ModelAdmin):
    list_display = ('created_date_time', 'name')
    list_display_links = ('name', )
    list_per_page = 25

    def save_model(self, request, obj, form, change):
        
        obj.save()

        change_cpu_governor("performance")

        import zipfile
        import os
        import subprocess

        import geopandas
        import pandas as pd
        from spine.settings import MEDIA_ROOT, BASE_DIR

        # Load DataFrames
        with zipfile.ZipFile(obj.name.path, "r") as zip_file:
            
            extract_folder = os.path.join(BASE_DIR, "temp/")
            zip_file.extractall(extract_folder)
            
            anag = geopandas.read_file(os.path.join(extract_folder, "ANAG.DBF"))
            os.unlink(os.path.join(extract_folder, "ANAG.DBF"))
            
            fatture = geopandas.read_file(os.path.join(extract_folder, "FATT.DBF"))
            os.unlink(os.path.join(extract_folder, "FATT.DBF"))
            
            elementi_fattura = geopandas.read_file(os.path.join(extract_folder, "LFAT.DBF"))
            os.unlink(os.path.join(extract_folder, "LFAT.DBF"))

        # Anagrafe

        anag.fillna(value=pd.np.nan, inplace=True)

        for index, row in anag.iterrows():
            
            try:
                cliente = Cliente.objects.get(codana=row[0].strip().upper())
            except:
                cliente = Cliente(
                    codana = row[0].strip().upper() if row[0] == row[0] else None,
                )
            
            cliente.intest = row[1] if row[1] == row[1] else None
            cliente.rsoc = ' '.join([str(x) for x in [row[2], row[3]] if isinstance(x, str) ]) if row[2] == row[2] else None
            cliente.codfis = row[4] if row[4] == row[4] else None
            cliente.piva = row[5] if row[5] == row[5] else None
            cliente.indir = row[6] if row[6] == row[6] else None
            cliente.cap = row[7] if row[7] == row[7] else None
            cliente.local = row[8] if row[8] == row[8] else None
            cliente.prov = row[9] if row[9] == row[9] else None
            cliente.nazione = row[10] if row[10] == row[10] else None
            cliente.allegiva = row[11] if row[11] == row[11] else None
            cliente.riferiment = row[12] if row[12] == row[12] else None
            cliente.telef = row[13] if row[13] == row[13] else None
            cliente.fax = row[14] if row[14] == row[14] else None
            cliente.ressec = row[15] if row[15] == row[15] else None
            cliente.datanasc = row[16] if row[16] == row[16] else None
            cliente.luona = row[17] if row[17] == row[17] else None
            cliente.provna = row[18] if row[18] == row[18] else None
            cliente.indircor = row[19] if row[19] == row[19] else None
            cliente.capcor = row[20] if row[20] == row[20] else None
            cliente.localcor = row[21] if row[21] == row[21] else None
            cliente.provcor = row[22] if row[22] == row[22] else None
            cliente.nazionecor = row[23] if row[23] == row[23] else None
            cliente.note = row[24] if row[24] == row[24] else None
            cliente.save()

        try:
            latest_fattura_id = Fattura.objects.latest('id').id
        except:
            latest_fattura_id = 0

        # Fatture 
        fatture.fillna(value=pd.np.nan, inplace=True)

        latest_fatture = fatture[fatture["NUMMOV"] > latest_fattura_id]

        for index, row in latest_fatture.iterrows():
            
            try:
                cliente = Cliente.objects.get(codana=row[4].strip().upper())
            except:
                cliente = None

            row[6] if row[6] == row[6] else None

            if row[6] == row[6]:
                try:
                    mopag = ModalitaPagamento.objects.get(codice_pagamento=row[6].strip().upper())
                except:
                    mopag = None
            else:
                mopag = None

            fattura = Fattura.objects.create(
                id = row[0],
                tdoc = row[1] if row[1] == row[1] else None,
                nrdoc = row[2] if row[2] == row[2] else None,
                ddoc = row[3] if row[3] == row[3] else None,
                codana = cliente,
                stato = row[5] if row[5] == row[5] else None,
                old_mopag = row[6] if row[6] == row[6] else None,
                mopag = mopag,
                bappoggio = row[7] if row[7] == row[7] else None,
                speseboll = row[8] if row[8] == row[8] else None,
                bolli = row[9] if row[9] == row[9] else None,
                tpsconto = row[10] if row[10] == row[10] else None,
                percsconto = row[11] if row[11] == row[11] else None,
                sconto = row[12] if row[12] == row[12] else None,
                listino = row[13] if row[13] == row[13] else None,
                coddes = row[14] if row[14] == row[14] else None,
                rsoc = row[15] if row[15] == row[15] else None,
                indirizzo = row[16] if row[16] == row[16] else None,
                localita = row[17] if row[17] == row[17] else None,
                provincia = row[18] if row[18] == row[18] else None,
                agente = row[19] if row[19] == row[19] else None,
                cprovv = row[20] if row[20] == row[20] else None,
                provv = row[21] if row[21] == row[21] else None,
                tprovv = row[22] if row[22] == row[22] else None,
                percprovv = row[23] if row[23] == row[23] else None,
                pariva = row[24] if row[24] == row[24] else None,
                valuta = row[25] if row[25] == row[25] else None,
                cambio = row[26] if row[26] == row[26] else None,
                note = row[27] if row[27] == row[27] else None,
                aspetto = row[28] if row[28]== row[28] else None,
                colli = row[29] if row[29] == row[29] else None,
                tporto = row[30] if row[30] == row[30] else None,
                amezzo = row[31] if row[31] == row[31] else None,
                vcoddes = row[32] if row[32] == row[32] else None,
                vrsoc = row[33] if row[33] == row[33] else None,
                vindirizzo = row[34] if row[34] == row[34] else None,
                vlocalita = row[35] if row[35] == row[35] else None,
                vprovincia = row[36] if row[36] == row[36] else None,
                data = row[37] if row[37] == row[37] else None,
                ora = row[38] if row[38] == row[38] else None,
                acconto = row[39] if row[39] == row[39] else None,
                tcautr = row[40] if row[40] == row[40] else None,
                cautr = row[41] if row[41] == row[41] else None,
                gendoc = row[42] if row[42] == row[42] else None,
                gencon = row[43] if row[43] == row[43] else None,
                genmag = row[44] if row[44] == row[44] else None,
                comm = row[45] if row[45] == row[45] else None,
                pvaluta = row[46] if row[46] == row[46] else None,
                campo1 = row[47] if row[47] == row[47] else None,
                campo2 = row[48] if row[48] == row[48] else None,
                campo3 = row[49] if row[49] == row[49]else None,
                campo4 = row[50] if row[50] == row[50] else None,
                campo5 = row[51] if row[51] == row[51] else None,
                campo6 = row[52] if row[52] == row[52] else None,
                campo7 = row[53] if row[53] == row[53] else None,
                campo8 = row[54] if row[54] == row[54] else None,
                campo9 = row[55] if row[55] == row[55] else None,
                campo10 = row[56] if row[56] == row[56] else None,
            )

        # Elementi fattura

        elementi_fattura.fillna(value=pd.np.nan, inplace=True)

        latest_elementi_fatture = elementi_fattura[elementi_fattura["LNUMMOV"] > latest_fattura_id]

        for index, row in latest_elementi_fatture.iterrows():
            
            try:
                fattura = Fattura.objects.get(id=int(row[0]))
            except:
                fattura = None
            
            if row[12] == row[12]:
                try:
                    aliquota_iva = AliquotaIva.objects.get(codice_iva=row[12].strip().upper())
                except:
                    aliquota_iva = None
            else:
                aliquota_iva = None
            
            elemento_fattura = ElementoFattura.objects.create(
                lnummov = fattura,
                nrr = row[1] if row[1] == row[1] else None,
                codart = row[2] if row[2] == row[2] else None,
                codmag = row[3] if row[3] == row[3] else None,
                descri = row[4] if row[4] == row[4] else None,
                um = row[5] if row[5] == row[5] else None,
                qto = row[6] if row[6] == row[6] else None,
                prezzo = row[7] if row[7] == row[7] else None,
                tsconto = row[8] if row[8] == row[8] else None,
                sconto1 = row[9] if row[9] == row[9] else None,
                percsc2 = row[10] if row[10] == row[10] else None,
                percsc3 = row[11] if row[11] == row[11] else None,
                old_iva = row[12] if row[12] == row[12] else None,
                iva = aliquota_iva,
                lagente = row[13] if row[13] == row[13] else None,
                ltprovv = row[14] if row[14] == row[14] else None,
                lcprovv = row[15] if row[15] == row[15] else None,
                lprovv = row[16] if row[16] == row[16] else None,
                note = row[17] if row[17] == row[17] else None,
                prezzoe = row[18] if row[18] == row[18] else None,
                genmag = row[19] if row[19] == row[19] else None,
                marca = row[20] if row[20] == row[20] else None,
                ndis = row[21] if row[21] == row[21] else None,
                collaudo = row[22] if row[22] == row[22] else None,
                nscostru = row[23] if row[23] == row[23] else None,
                posc = row[24] if row[24] == row[24] else None,
                )
        
        try:
            result = subprocess.check_output(os.path.join(BASE_DIR, 'extra_functionalities/BackupSpineDB'), shell=True)
        except:
            pass
        
        change_cpu_governor("powersave")

my_admin_site.register(UploadFile, UploadAdmin)

# Cedente admin

from info_cedente.models import Cedente

class CedenteAdmin(admin.ModelAdmin):
    list_display = ('denominazione',)
    list_display_links = ('denominazione', )
    list_per_page = 25

my_admin_site.register(Cedente, CedenteAdmin)

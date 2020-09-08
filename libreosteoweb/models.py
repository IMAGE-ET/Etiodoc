
# This file is part of Libreosteo.
#
# Libreosteo is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Libreosteo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Libreosteo.  If not, see <http://www.gnu.org/licenses/>.
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.exceptions import NON_FIELD_ERRORS
from datetime import date, datetime
from libreosteoweb.api.utils import enum
import mimetypes

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class RegularDoctor(models.Model):
    """
        This class implements bean object to represent
        regular doctor for a patient

        It describes fields into this object which are mapped into DB
        """
    family_name = models.CharField(_('Family name'), max_length=200)
    first_name = models.CharField(_('Firstname'), max_length=200)
    phone = models.CharField(_('Phone'), max_length=100, blank=True, null=True)
    city = models.CharField(_('City'), max_length=200, blank=True)

    def __unicode__(self):
        return "%s %s" % (self.family_name, self.first_name)


class Patient(models.Model):
    """
        This class implements bean object to represent
        patient.
        """
    numSS = models.TextField(_('NumSS'), blank=True)
    numMut = models.TextField(_('NumMut'), blank=True)

    family_name = models.CharField(_('Family name'), max_length=200)
    original_name = models.CharField(_('Original name'),
                                     max_length=200,
                                     blank=True)
    first_name = models.CharField(_('Firstname'), max_length=200, blank=True)
    birth_date = models.DateField(_('Birth date'))
    address_street = models.CharField(_('Street'), max_length=500, blank=True)
    address_complement = models.CharField(_('Address complement'),
                                          max_length=500,
                                          blank=True)
    address_zipcode = models.CharField(_('Zipcode'),
                                       max_length=200,
                                       blank=True)
    address_city = models.CharField(_('City'), max_length=200, blank=True)
    email = models.EmailField(_('Email'), max_length=200, blank=True)
    phone = models.CharField(_('Phone'), max_length=200, blank=True)
    mobile_phone = models.CharField(_('Mobile phone'),
                                    max_length=200,
                                    blank=True)
    job = models.CharField(_('Job'), max_length=200, blank=True, default="")
    hobbies = models.TextField(_('Hobbies'), blank=True, default="")
    doctor = models.ForeignKey(RegularDoctor,
                               verbose_name=_('Regular doctor'),
                               blank=True,
                               null=True)
    smoker = models.BooleanField(_('Smoker'), default=False)
    laterality = models.CharField(_('Laterality'),
                                  max_length=1,
                                  choices=(('L', _('Left-handed')),
                                           ('A', _('Ambidextre')),
                                           ('R', _('Right-handed'))),
                                  blank=True,
                                  null=True)
    important_info = models.TextField(_('Important note'), blank=True)
    current_treatment = models.TextField(_('Current treatment'),
                                         blank=True,
                                         default="")
    surgical_history = models.TextField(_('Surgical history'), blank=True)
    medical_history = models.TextField(_('Medical history'), blank=True)
    family_history = models.TextField(_('Family history'), blank=True)
    trauma_history = models.TextField(_('Trauma history'), blank=True)
    medical_reports = models.TextField(_('Medical reports'), blank=True)
    creation_date = models.DateField(_('Creation date'),
                                     blank=True,
                                     null=True,
                                     editable=False)
    sex = models.CharField(_('Sex'),
                           max_length=1,
                           choices=(('M', _('Male')), ('F', _('Female'))),
                           blank=True,
                           null=True)

    # Not mapped field, only for traceability purpose
    current_user_operation = None

    def __unicode__(self):
        return "%s %s by %s" % (self.family_name, self.first_name,
                                self.current_user_operation)

    def clean(self):
        if self.creation_date is None:
            self.creation_date = date.today()

    def set_user_operation(self, user):
        """ Use this setting method to define the user
            which performs the operation (create, update).
            Not mapped in DB only for the runtime"""
        self.current_user_operation = user

    TYPE_NEW_PATIENT = 1
    TYPE_UPDATE_PATIENT = 2


class Children(models.Model):
    """
        This class implements bean object to represent
        children of a patient.
        """
    family_name = models.CharField(_('Family name'),
                                   max_length=200,
                                   blank=True)
    first_name = models.CharField(_('Firstname'), max_length=200)
    birthday_date = models.DateField(_('Birth date'))
    parent = models.ForeignKey(Patient, verbose_name=_('Parent'))

    def __unicode__(self):
        return "%s %s" % (self.family_name, self.first_name)


class Examination(models.Model):
    """
    This class implements bean object to represent
    examination on a patient
    """
    #Start of skeleton
    #Tête
    OsTempD = models.TextField(_('Os temporal droit'), blank=True)
    SphenoideD = models.TextField(_('Sphénoïde, grande aile droite'), blank=True)
    OsParietalD = models.TextField(_('Os pariétal droit'), blank=True)
    OsFrontal = models.TextField(_('Os Frontal'), blank=True)
    OsZygomatiqueD = models.TextField(_('Os zygomatique droit'), blank=True)
    MaxilaireSup = models.TextField(_('Maxillaire supérieur'), blank=True)
    OsNez = models.TextField(_('Os propre du nez'), blank=True)
    Mandible = models.TextField(_('Mandibule'), blank=True)
    OsZygomatiqueG = models.TextField(_('Os zygomatique gauche'), blank=True)
    OsTempG = models.TextField(_('Os temporal gauche'), blank=True)
    SphenoideG = models.TextField(_('Sphénoïde, grande aile Gauche'), blank=True)
    OsParietalG = models.TextField(_('Os pariétal gauche'), blank=True)
    Crane = models.TextField(_('Crane'), blank=True)
    AtmD = models.TextField(_('ATM Droite'), blank=True)
    AtmG = models.TextField(_('ATM Gauche'), blank=True)


    #Bras Droit
    EpauleD = models.TextField(_('Épaule Droite'), blank=True)
    ClaviculeD = models.TextField(_('Clavicule Droite'), blank=True)
    OmoplateD = models.TextField(_('Omoplate Droit'), blank=True)
    HumerusD = models.TextField(_('Humérus Droit'), blank=True)
    BrasD = models.TextField(_('Bras Droit'), blank=True)
    CoudeD = models.TextField(_('Coude Droit'), blank=True)
    CubitusD = models.TextField(_('Ulna Droit'), blank=True)
    RadiusD = models.TextField(_('Radius Droit'), blank=True)
    PoignetD = models.TextField(_('Poignet Droit'), blank=True)
    PisiformeD = models.TextField(_('Pisiforme Droit'), blank=True)
    PyramidalD = models.TextField(_('Pyramidal Droit'), blank=True)
    OsCrochuD = models.TextField(_('Os Crochu Droit'), blank=True)
    SemiLunaireD = models.TextField(_('Semi Lunaire Droit'), blank=True)
    GrandOsD = models.TextField(_('Grand os Droit'), blank=True)
    ScaphoideD = models.TextField(_('Scaphoïde Droit'), blank=True)
    TrapezoideD = models.TextField(_('Trapézoïde Droit'), blank=True)
    TrapezeD = models.TextField(_('Trapèze Droit'), blank=True)
    Metacarpe5D = models.TextField(_('5ème métacarpe droit'), blank=True)
    P1Seg5D = models.TextField(_('Phalange de l’auriculaire droit'), blank=True)
    P2Seg5D = models.TextField(_('Phalangine de l’auriculaire droit'), blank=True)
    P3Seg5D = models.TextField(_('Phalangette de l’auriculaire droit'), blank=True)
    Metacarpe4D = models.TextField(_('4ème métacarpe droit'), blank=True)
    P1Seg4D = models.TextField(_('Phalange de l’annulaire droit'), blank=True)
    P2Seg4D = models.TextField(_('Phalangine de l’annulaire droit'), blank=True)
    P3Seg4D = models.TextField(_('Phalangette de l’annulaire droit'), blank=True)
    Metacarpe3D = models.TextField(_('3ème métacarpe droit'), blank=True)
    P1Seg3D = models.TextField(_('Phalange du majeur droit'), blank=True)
    P2Seg3D = models.TextField(_('Phalangine du majeur droit'), blank=True)
    P3Seg3D = models.TextField(_('Phalangette du majeur droit'), blank=True)
    Metacarpe2D = models.TextField(_('2ème métacarpe droit'), blank=True)
    P1Seg2D = models.TextField(_('Phalange de l’index droit'), blank=True)
    P2Seg2D = models.TextField(_('Phalangine de l’index droit'), blank=True)
    P3Seg2D = models.TextField(_('Phalangette de l’index droit'), blank=True)
    Metacarpe1D = models.TextField(_('1er métatarse droit'), blank=True)
    P1PouceD = models.TextField(_('Phalange du pouce droit'), blank=True)
    P3PouceD = models.TextField(_('Phalangette du pouce droit'), blank=True)
    MainD = models.TextField(_('Main Droite'), blank=True)

    #Cage thoracique
    Cote1D = models.TextField(_('1ère côte droite '), blank=True)
    Cote2D = models.TextField(_('2ème côte droite'), blank=True)
    Cote3D = models.TextField(_('3ème côte droite'), blank=True)
    Cote4D = models.TextField(_('4ème côte droite'), blank=True)
    Cote5D = models.TextField(_('5ème côte droite'), blank=True)
    Cote6D = models.TextField(_('6ème côte droite'), blank=True)
    Cote7D = models.TextField(_('7ème côte droite'), blank=True)
    Cote8D = models.TextField(_('8ème côte droite'), blank=True)
    Cote9D = models.TextField(_('9ème côte droite'), blank=True)
    Cote10D = models.TextField(_('10ème côte droite'), blank=True)
    Cote11D = models.TextField(_('11ème côte droite'), blank=True)
    Cote12D = models.TextField(_('12ème côte droite'), blank=True)
    Cote1G = models.TextField(_('1ère côte gauche'), blank=True)
    Cote2G = models.TextField(_('2ème côte gauche'), blank=True)
    Cote3G = models.TextField(_('3ème côte gauche'), blank=True)
    Cote4G = models.TextField(_('4ème côte gauche'), blank=True)
    Cote5G = models.TextField(_('5ème côte gauche'), blank=True)
    Cote6G = models.TextField(_('6ème côte gauche'), blank=True)
    Cote7G = models.TextField(_('7ème côte gauche'), blank=True)
    Cote8G = models.TextField(_('8ème côte gauche'), blank=True)
    Cote9G = models.TextField(_('9ème côte gauche'), blank=True)
    Cote10G = models.TextField(_('10ème côte gauche'), blank=True)
    Cote11G = models.TextField(_('11ème côte gauche'), blank=True)
    Cote12G = models.TextField(_('12ème côte gauche'), blank=True)
    Manubrium = models.TextField(_('Manubrium sternal'), blank=True)
    CorpsSternal = models.TextField(_('Corps Sternal'), blank=True)
    ProcessusXiphoide  = models.TextField(_('Processus  xiphoïde '), blank=True)
    GrilCostalD = models.TextField(_('Gril costal droit'), blank=True)
    GrilCostalG = models.TextField(_('Gril costal gauche'), blank=True)
    Sternum = models.TextField(_('Sternum'), blank=True)

    #Bras gauche
    ClaviculeG = models.TextField(_('Clavicule Gauche'), blank=True)
    OmoplateG = models.TextField(_('Omoplate Gauche'), blank=True)
    HumerusG = models.TextField(_('Humérus Gauche'), blank=True)
    CubitusG = models.TextField(_('Ulna Gauche'), blank=True)
    RadiusG = models.TextField(_('Radius Gauche'), blank=True)
    BrasG = models.TextField(_('Bras Gauche'), blank=True)
    EpauleG = models.TextField(_('Épaule Gauche'), blank=True)
    CoudeG = models.TextField(_('Coude Gauche'), blank=True)
    PoignetG = models.TextField(_('Poignet Gauche'), blank=True)
    PisiformeG = models.TextField(_('Pisiforme Gauche'), blank=True)
    PyramidalG = models.TextField(_('Pyramidal Gauche'), blank=True)
    OsCrochuG = models.TextField(_('Os Crochu Gauche'), blank=True)
    SemiLunaireG = models.TextField(_('Semi Lunaire Gauche'), blank=True)
    GrandOsG = models.TextField(_('Grand os Gauche'), blank=True)
    ScaphoideG = models.TextField(_('Scaphoïde Gauche'), blank=True)
    TrapezoideG = models.TextField(_('Trapézoïde Gauche'), blank=True)
    TrapezeG = models.TextField(_('Trapèze Gauche'), blank=True)
    Metacarpe5G = models.TextField(_('5ème métacarpe gauche'), blank=True)
    P1Seg5G = models.TextField(_('Phalange de l’auriculaire gauche'), blank=True)
    P2Seg5G = models.TextField(_('Phalangine de l’auriculaire gauche'), blank=True)
    P3Seg5G = models.TextField(_('Phalangette de l’auriculaire gauche'), blank=True)
    Metacarpe4G = models.TextField(_('4ème métacarpe gauche'), blank=True)
    P1Seg4G = models.TextField(_('Phalange de l’annulaire gauche'), blank=True)
    P2Seg4G = models.TextField(_('Phalangine de l’annulaire gauche'), blank=True)
    P3Seg4G = models.TextField(_('Phalangette de l’annulaire gauche'), blank=True)
    Metacarpe3G = models.TextField(_('3ème métacarpe gauche'), blank=True)
    P1Seg3G = models.TextField(_('Phalange du majeur gauche'), blank=True)
    P2Seg3G = models.TextField(_('Phalangine du majeur gauche'), blank=True)
    P3Seg3G = models.TextField(_('Phalangette du majeur gauche'), blank=True)
    Metacarpe2G = models.TextField(_('2ème métacarpe gauche'), blank=True)
    P1Seg2G = models.TextField(_('Phalange de l’index gauche'), blank=True)
    P2Seg2G = models.TextField(_('Phalangine de l’index gauche'), blank=True)
    P3Seg2G = models.TextField(_('Phalangette de l’index gauche'), blank=True)
    Metacarpe1G = models.TextField(_('1er métatarse gauche'), blank=True)
    P1PouceG = models.TextField(_('Phalange du pouce gauche'), blank=True)
    P3PouceG = models.TextField(_('Phalangette du pouce gauche'), blank=True)
    MainG = models.TextField(_('Main Gauche'), blank=True)

    #Colonne & Hanche
    Cervicales = models.TextField(_('Cervicales'), blank=True)
    Thoraciques = models.TextField(_('Thoraciques'), blank=True)
    Lombaires = models.TextField(_('Lombaires'), blank=True)
    C1 = models.TextField(_('Altas'), blank=True)
    C2 = models.TextField(_('Axis'), blank=True)
    C3 = models.TextField(_('3ème cervicale'), blank=True)
    C4 = models.TextField(_('4ème cervicale'), blank=True)
    C5 = models.TextField(_('5ème cervicale'), blank=True)
    C6 = models.TextField(_('6ème cervicale'), blank=True)
    C7 = models.TextField(_('7ème cervicale'), blank=True)
    Th1 = models.TextField(_('1ère Thoracique'), blank=True)
    Th2 = models.TextField(_('2ème thoracique'), blank=True)
    Th3 = models.TextField(_('3ème thoracique'), blank=True)
    Th4 = models.TextField(_('4ème thoracique'), blank=True)
    Th5 = models.TextField(_('5ème thoracique'), blank=True)
    Th6 = models.TextField(_('6ème thoracique '), blank=True)
    Th7 = models.TextField(_('7ème thoracique'), blank=True)
    Th8 = models.TextField(_('8ème thoracique'), blank=True)
    Th9 = models.TextField(_('9ème thoracique'), blank=True)
    Th10 = models.TextField(_('10ème thoracique'), blank=True)
    Th11 = models.TextField(_('11ème thoracique'), blank=True)
    Th12 = models.TextField(_('12ème thoracique'), blank=True)
    L1 = models.TextField(_('1ère lombaire'), blank=True)
    L2 = models.TextField(_('2ème lombaire'), blank=True)
    L3 = models.TextField(_('3ème lombaire'), blank=True)
    L4 = models.TextField(_('4ème lombaire'), blank=True)
    L5 = models.TextField(_('5ème lombaire'), blank=True)
    Sacrum = models.TextField(_('Sacrum'), blank=True)
    IlionD = models.TextField(_('Aile iliaque droite (ilion)'), blank=True)
    IschionD = models.TextField(_('Ischion droit'), blank=True)
    OsPubienD = models.TextField(_('Os pubien droit'), blank=True)
    Coccyx = models.TextField(_('Vertèbres coccygiennes'), blank=True)
    IlioinG = models.TextField(_('Aile iliaque gauche (ilioin)'), blank=True)
    OsPubienG = models.TextField(_('Os pubien gauche'), blank=True)
    IschionG = models.TextField(_('Ischion gauche'), blank=True)
    Bassin = models.TextField(_('Bassin'), blank=True)
    HancheD = models.TextField(_('Hanche Droite'), blank=True)
    HancheG = models.TextField(_('Hanche Gauche'), blank=True)
    SacroIliaqueD = models.TextField(_('Sacro-iliaque Droit'), blank=True)
    SacroIliaqueG = models.TextField(_('Sacro-iliaque Gauche'), blank=True)

    #Jambe droite
    FemurD = models.TextField(_('Fémur Droit'), blank=True)
    PatellaD = models.TextField(_('Patella Droit'), blank=True)
    FibulaD = models.TextField(_('Fibula Droit'), blank=True)
    TibiaD = models.TextField(_('Tibia Droit'), blank=True)
    TalusD = models.TextField(_('Talus Droit'), blank=True)
    CalcuneusD = models.TextField(_('Calcuneus Droit'), blank=True)
    OsCuboideD = models.TextField(_('Os cuboïde Droit'), blank=True)
    OsNaviculaireD = models.TextField(_('Os naviculaire Droit'), blank=True)
    JambeD = models.TextField(_('Jambe Droite'), blank=True)
    GenouD = models.TextField(_('Genou Droit'), blank=True)
    ChevilleD = models.TextField(_('Cheville Droite'), blank=True)
    Cuneiforme1D = models.TextField(_('Cunéiforme médial Droit'), blank=True)
    Cuneiforme2D = models.TextField(_('Cunéiforme intermédiaire Droit'), blank=True)
    Cuneiforme3D = models.TextField(_('Cunéiforme latéral Droit'), blank=True)
    Metatarsien1D = models.TextField(_('1er Métatarsien Droit'), blank=True)
    Metatarsien2D = models.TextField(_('2ème Métatarsien Droit'), blank=True)
    Metatarsien3D = models.TextField(_('3ème Métatarsien Droit'), blank=True)
    Metatarsien4D = models.TextField(_('4ème Métatarsien Droit'), blank=True)
    Metatarsien5D = models.TextField(_('5ème Métatarsien Droit'), blank=True)
    Phalange1D = models.TextField(_('Phalange du 1er orteil Droit'), blank=True)
    Phalange2D = models.TextField(_('Phalange du 2ème orteil Droit'), blank=True)
    Phalange3D = models.TextField(_('Phalange du 3ème orteil Droit'), blank=True)
    Phalange4D = models.TextField(_('Phalange du 4ème orteil Droit'), blank=True)
    Phalange5D = models.TextField(_('Phalange du 5ème orteil Droit'), blank=True)
    Phalangine2D = models.TextField(_('Phalangine du 2ème orteil Droit'), blank=True)
    Phalangine3D = models.TextField(_('Phalangine du 3ème orteil Droit'), blank=True)
    Phalangine4D = models.TextField(_('Phalangine du 4ème orteil Droit'), blank=True)
    Phalangine5D = models.TextField(_('Phalangine du 5ème orteil Droit'), blank=True)
    Phalangette1D = models.TextField(_('Phalangette du 1er orteil Droit'), blank=True)
    Phalangette2D = models.TextField(_('Phalangette du 2ème orteil Droit'), blank=True)
    Phalangette3D = models.TextField(_('Phalangette du 3ème orteil Droit'), blank=True)
    Phalangette4D = models.TextField(_('Phalangette du 4ème orteil Droit'), blank=True)
    Phalangette5D = models.TextField(_('Phalangette du 5ème orteil Droit'), blank=True)
    PiedD = models.TextField(_('Pied Droit'), blank=True)

    #Jambe gauche
    FemurG = models.TextField(_('Fémur gauche'), blank=True)
    PatellaG = models.TextField(_('Patella gauche'), blank=True)
    FibulaG = models.TextField(_('Fibula gauche'), blank=True)
    TibiaG = models.TextField(_('Tibia gauche'), blank=True)
    TalusG = models.TextField(_('Talus gauche'), blank=True)
    CalcuneusG = models.TextField(_('Calcuneus gauche'), blank=True)
    OsCuboideG = models.TextField(_('Os cuboïde gauche'), blank=True)
    OsNaviculaireG = models.TextField(_('Os naviculaire gauche'), blank=True)
    JambeG = models.TextField(_('Jambe Gauche'), blank=True)
    GenouG = models.TextField(_('Genou Gauche'), blank=True)
    ChevilleG = models.TextField(_('Cheville Gauche'), blank=True)
    Cuneiforme1G = models.TextField(_('Cunéiforme médial gauche'), blank=True)
    Cuneiforme2G = models.TextField(_('Cunéiforme intermédiaire gauche'), blank=True)
    Cuneiforme3G = models.TextField(_('Cunéiforme latéral gauche'), blank=True)
    Metatarsien1G = models.TextField(_('1er Métatarsien gauche'), blank=True)
    Metatarsien2G = models.TextField(_('2ème Métatarsien gauche'), blank=True)
    Metatarsien3G = models.TextField(_('3ème Métatarsien gauche'), blank=True)
    Metatarsien4G = models.TextField(_('4ème Métatarsien gauche'), blank=True)
    Metatarsien5G = models.TextField(_('5ème Métatarsien gauche'), blank=True)
    Phalange1G = models.TextField(_('Phalange du 1er orteil gauche'), blank=True)
    Phalange2G = models.TextField(_('Phalange du 2ème orteil gauche'), blank=True)
    Phalange3G = models.TextField(_('Phalange du 3ème orteil gauche'), blank=True)
    Phalange4G = models.TextField(_('Phalange du 4ème orteil gauche'), blank=True)
    Phalange5G = models.TextField(_('Phalange du 5ème orteil gauche'), blank=True)
    Phalangine2G = models.TextField(_('Phalangine du 2ème orteil gauche'), blank=True)
    Phalangine3G = models.TextField(_('Phalangine du 3ème orteil gauche'), blank=True)
    Phalangine4G = models.TextField(_('Phalangine du 4ème orteil gauche'), blank=True)
    Phalangine5G = models.TextField(_('Phalangine du 5ème orteil gauche'), blank=True)
    Phalangette1G = models.TextField(_('Phalangette du 1er orteil gauche'), blank=True)
    Phalangette2G = models.TextField(_('Phalangette du 2ème orteil gauche'), blank=True)
    Phalangette3G = models.TextField(_('Phalangette du 3ème orteil gauche'), blank=True)
    Phalangette4G = models.TextField(_('Phalangette du 4ème orteil gauche'), blank=True)
    Phalangette5G = models.TextField(_('Phalangette du 5ème orteil gauche'), blank=True)
    PiedG = models.TextField(_('Pied Gauche'), blank=True)
    #End of skeleton




    reason = models.TextField(_('Reason'), blank=True)
    reason_description = models.TextField(_('Reason description/Context'),
                                          blank=True)
    orl = models.TextField(_('ORL Sphere'), blank=True)
    visceral = models.TextField(_('Sphère digestive'), blank=True)
    pulmo = models.TextField(_('Cardio-Pulmo Sphere'), blank=True)
    uro_gyneco = models.TextField(_('Uro-gyneco Sphere'), blank=True)
    periphery = models.TextField(_('Periphery Sphere'), blank=True)
    general_state = models.TextField(_('General state'), blank=True)
    medical_examination = models.TextField(_('Medical examination'),
                                           blank=True)
    diagnosis = models.TextField(_('Diagnostic Etiopathique'), blank=True)
    treatments = models.TextField(_('Treatments'), blank=True)
    conclusion = models.TextField(_('Conclusion'), blank=True)
    date = models.DateTimeField(_('Date'))
    # Status : 0 -> in progress
    # Status : 1 -> invoiced not paid
    # Status : 2 -> invoiced and paid
    # Status : 3 -> not invoiced
    status = models.SmallIntegerField(_('Status'))
    status_reason = models.TextField(_('Status reason'), blank=True, null=True)
    # Type : 1 -> normal examination
    # Type : 2 -> continuation of the examination
    # Type : 3 -> return of a previous examination
    # Type : 4 -> emergency examination
    type = models.SmallIntegerField(_('Type'))
    invoices = models.ManyToManyField('Invoice',
                                      verbose_name=_('Invoice'),
                                      blank=True)
    patient = models.ForeignKey(Patient, verbose_name=_('Patient'))
    therapeut = models.ForeignKey(User,
                                  verbose_name=_('Therapeut'),
                                  blank=True,
                                  null=True)

    EXAMINATION_IN_PROGRESS = 0
    EXAMINATION_WAITING_FOR_PAIEMENT = 1
    EXAMINATION_INVOICED_PAID = 2
    EXAMINATION_NOT_INVOICED = 3

    # i18n
    TYPE_NORMAL_EXAMINATION_I18N = _('Normal examination')
    TYPE_CONTINUING_EXAMINATION_I18N = _('Continuing examination')
    TYPE_RETURN_I18N = _('Return')
    TYPE_EMERGENCY_I18N = _('Emergency')

    def __unicode__(self):
        return "%s %s" % (self.patient, self.date)

    def get_invoice_number(self):
        invoice = self._get_last_invoice()
        return invoice.number if invoice is not None else None

    def _resolve_invoice(self, invoice):
        if invoice.canceled_by is not None:
            return self._resolve_invoice(invoice.canceled_by)
        return invoice if invoice.type == 'invoice' else None

    def _get_invoices_list(self):
        invoices_list = []
        if self.invoices is not None and self.invoices.all().count() > 0:
            invoices = self.invoices.all().order_by('date')
            for invoice in invoices:
                current_invoice = invoice
                invoices_list.append(current_invoice)
                while current_invoice.canceled_by is not None:
                    current_invoice = current_invoice.canceled_by
                    invoices_list.append(current_invoice)
        last_invoice = self._get_last_invoice()
        invoices_list.reverse()
        if last_invoice is not None:
            invoices_list.remove(self._get_last_invoice())
        return invoices_list

    invoices_list = property(_get_invoices_list)

    def _get_last_invoice(self):
        if self.invoices.all().count() == 0:
            return None
        invoices = self.invoices.all().order_by('-date')
        if invoices.first().canceled_by is not None:
            return self._resolve_invoice(invoices.first())
        return self.invoices.latest('date')

    last_invoice = property(_get_last_invoice)


ExaminationType = enum(
    'ExaminationType',
    'EMPTY',
    'NORMAL',
    'CONTINUING',
    'RETURN',
    'EMERGENCY',
)

ExaminationStatus = enum(
    'ExaminationStatus',
    'IN_PROGRESS',
    'WAITING_FOR_PAIEMENT',
    'INVOICED_PAID',
    'NOT_INVOICED',
)

InvoiceStatus = enum('InvoiceStatus', 'DRAFT', 'WAITING_FOR_PAIEMENT',
                     'INVOICED_PAID', 'CANCELED')


class ExaminationComment(models.Model):
    """This class represents a comment on examination
    """
    user = models.ForeignKey(User,
                             verbose_name=_('User'),
                             blank=True,
                             null=True)
    comment = models.TextField(_('Comment'))
    date = models.DateTimeField(_('Date'), null=True, blank=True)
    examination = models.ForeignKey(Examination, verbose_name=_('Examination'))



class Invoice(models.Model):
    """
    This class implements bean object to represent
    invoice on an examination
    """

    icon = models.TextField(_('Icon'), blank=True)
    dateExamination = models.DateTimeField(_('dateExamination'), blank=True)
    numDiplome = models.TextField(_('NumDiplome'), blank=True)
    codeAPE = models.TextField(_('CodeAPE'), blank=True)
    numSS = models.TextField(_('NumSS'), blank=True)
    numMut = models.TextField(_('NumMut'), blank=True)


    date = models.DateTimeField(_('Date'))
    amount = models.FloatField(_('Amount'))
    currency = models.CharField(_('Currency'), max_length=10)
    paiment_mode = models.CharField(_('Paiment mode'), max_length=10)
    header = models.TextField(_('Header'), blank=True)
    therapeut_name = models.TextField(_('Therapeut name'))
    therapeut_first_name = models.TextField(_('Therapeut firstname'))
    quality = models.TextField(_('Quality'), blank=True)
    adeli = models.TextField(_('Adeli'))
    location = models.TextField(_('Location'))
    number = models.TextField(_('Number'))
    patient_family_name = models.CharField(_('Family name'), max_length=200)
    patient_original_name = models.CharField(_('Original name'),
                                             max_length=200,
                                             blank=True)
    patient_first_name = models.CharField(_('Firstname'),
                                          max_length=200,
                                          blank=True)
    patient_address_street = models.CharField(_('Street'),
                                              max_length=500,
                                              blank=True)
    patient_address_complement = models.CharField(_('Address complement'),
                                                  max_length=500,
                                                  blank=True)
    patient_address_zipcode = models.CharField(_('Zipcode'),
                                               max_length=200,
                                               blank=True)
    patient_address_city = models.CharField(_('City'),
                                            max_length=200,
                                            blank=True)
    content_invoice = models.TextField(_('Content'), blank=True)
    footer = models.TextField(_('Footer'), blank=True)
    office_siret = models.TextField(_('Siret'), blank=True)
    office_address_street = models.CharField(_('Street'),
                                             max_length=500,
                                             blank=True,
                                             default='')
    office_address_complement = models.CharField(_('Address complement'),
                                                 max_length=500,
                                                 blank=True,
                                                 default='')
    office_address_zipcode = models.CharField(_('Zipcode'),
                                              max_length=200,
                                              blank=True,
                                              default='')
    office_address_city = models.CharField(_('City'),
                                           max_length=200,
                                           blank=True,
                                           default='')
    office_phone = models.CharField(_('Phone'),
                                    max_length=200,
                                    blank=True,
                                    default='')
    status = models.IntegerField(_('status'), default=0)
    therapeut_id = models.IntegerField(_('therapeut_id'), default=0)
    canceled_by = models.ForeignKey('self',
                                    verbose_name=_("Canceled by"),
                                    blank=True,
                                    null=True)
    type = models.CharField(_('Invoice type'),
                            max_length=10,
                            blank=True,
                            default='invoice')

    def _get_paiments_list(self):
        return self.paiment_set.all().order_by('-date')

    paiments_list = property(_get_paiments_list)

    def clean(self):
        if self.date is None:
            self.date = datetime.today()

    class Meta:
        ordering = ['-date']


class PaimentMean(models.Model):
    """
    This class implements object to represent
    the mean of paiement of an examination
    """
    code = models.CharField(_('Code'), max_length=10)
    text = models.CharField(_('Text'), max_length=50)
    enable = models.BooleanField(_('Enabled'), default=True)


class Paiment(models.Model):
    """
    This class implements object to represent
    paiments (it is possible to have many paiments) of an invoice
    """
    invoice = models.ManyToManyField('Invoice',
                                     verbose_name=_("Invoices"),
                                     blank=True)
    amount = models.FloatField(_('Amount'))
    currency = models.CharField(_('Currency'), max_length=10)
    paiment_mode = models.CharField(_('Paiment mode'), max_length=10)
    date = models.DateField(_('Date'))


class OfficeEvent(models.Model):
    """
    This class implements bean object to represent
    event on the office
    """
    date = models.DateTimeField(_('Date'), blank=True)
    clazz = models.TextField(_('Class'), blank=True)
    type = models.SmallIntegerField(_('Type'))
    comment = models.TextField(_('Comment'), blank=True)
    reference = models.IntegerField(_('Reference'), blank=True, null=False)
    user = models.ForeignKey(User,
                             verbose_name=_('user'),
                             blank=True,
                             null=False)

    def clean(self):
        if self.date is None:
            self.date = datetime.today()


class OfficeSettings(models.Model):
    """
    This class implements model for the settings into the application
    """

    icon = models.TextField(_('Icon'), blank=True)

    invoice_office_header = models.CharField(_('Invoice office header'),
                                             max_length=500,
                                             blank=True)
    office_address_street = models.CharField(_('Street'),
                                             max_length=500,
                                             blank=True)
    office_address_complement = models.CharField(_('Address complement'),
                                                 max_length=500,
                                                 blank=True)
    office_address_zipcode = models.CharField(_('Zipcode'),
                                              max_length=200,
                                              blank=True)
    office_address_city = models.CharField(_('City'),
                                           max_length=200,
                                           blank=True)
    office_phone = models.CharField(_('Phone'), max_length=200, blank=True)
    office_siret = models.CharField(_('Siret'), max_length=20)
    amount = models.FloatField(_('Amount'),
                               blank=True,
                               null=True,
                               default=None)
    currency = models.CharField(_('Currency'), max_length=10)
    invoice_content = models.TextField(_('Invoice content'), blank=True)
    invoice_footer = models.TextField(_('Invoice footer'), blank=True)
    invoice_start_sequence = models.TextField(_('Invoice start sequence'),
                                              blank=True)

    def save(self, *args, **kwargs):
        """
        Ensure that only one instance exists in the db
        """
        self.id = 1
        super(OfficeSettings, self).save()

    UPDATE_INVOICE_SEQUENCE = 1


class TherapeutSettings(models.Model):
    """
    This class implements model for extending the User model
    """

    numDiplome = models.TextField(_('NumDiplome'), blank=True)
    codeAPE = models.TextField(_('CodeAPE'), blank=True)

    adeli = models.TextField(_('Adeli'), blank=True)
    quality = models.TextField(_('Quality'), blank=True)
    user = models.OneToOneField(User,
                                verbose_name=_('User'),
                                blank=True,
                                null=True)
    siret = models.CharField(_('Siret'), max_length=20, blank=True, null=True)
    invoice_footer = models.TextField(_('Invoice footer'),
                                      blank=True,
                                      null=True)

    # dashboard modules
    stats_enabled = models.BooleanField(_('Statistics'), default=True)
    last_events_enabled = models.BooleanField(_('Events history'),
                                              default=True)

    DASHBOARD_MODULES_FIELDS = [
        {
            'field': stats_enabled,
            'image': 'images/dashboard-stats.png'
        },
        {
            'field': last_events_enabled,
            'image': 'images/dashboard-events.png'
        },
    ]

    def save(self, *args, **kwargs):
        """
        Ensure that empty string are none in DB
        """
        if self.siret == '':
            self.siret = None
        if self.invoice_footer == '':
            self.invoice_footer = None
        super(TherapeutSettings, self).save(*args, **kwargs)


class FileImport(models.Model):
    """
    implements a couple of file for importing data.
    It concerns only Patient and examination
    """
    file_patient = models.FileField(_('Patient file'))
    file_examination = models.FileField(_('Examination file'), blank=True)
    status = models.IntegerField(_('validity status'),
                                 blank=True,
                                 default=None,
                                 null=True)
    analyze = None

    def delete(self, *args, **kwargs):
        """
        Delete media file too.
        """
        if bool(self.file_patient):
            storage_patient, path_patient = self.file_patient.storage, self.file_patient.path
        if bool(self.file_examination):
            storage_examination, path_examination = self.file_examination.storage, self.file_examination.path
        super(FileImport, self).delete(*args, **kwargs)
        if bool(self.file_patient):
            storage_patient.delete(path_patient)
        if bool(self.file_examination):
            storage_examination.delete(path_examination)

import mimetypes

class Document(models.Model):
    """
    Implements a document to be attached to
    an examination or patient file
    """
    document_file = models.FileField(_('Document file'), upload_to="documents")
    title = models.TextField(_('Title'))
    notes = models.TextField(_('Notes'), blank=True, null=True, default=None)
    internal_date = models.DateTimeField(_('Adding date'),
                                         blank=True,
                                         null=False)
    document_date = models.DateField(_('Document date'),
                                     blank=True,
                                     null=True,
                                     default=None)
    user = models.ForeignKey(User,
                             verbose_name=_('User'),
                             blank=True,
                             null=True)
    mime_type = models.TextField(_('Mime-Type'),
                                 blank=False,
                                 null=True,
                                 default=None)

    def delete(self, *args, **kwargs):
        """
        Delete the file
        """
        super(Document, self).delete(*args, **kwargs)
        storage_document, path_document = self.document_file.storage, self.document_file.path
        storage_document.delete(path_document)

    def clean(self):
        if self.internal_date is None:
            self.internal_date = datetime.today()
        self.mime_type = mimetypes.guess_type(self.document_file.path)[0]
        logger.info("mime_type = %s " % self.mime_type)


class PatientDocument(models.Model):
    """
    Implements a document to be attached to a patient file
    """
    patient = models.ForeignKey(Patient,
                                verbose_name=_('patient'),
                                on_delete=models.CASCADE)
    document = models.OneToOneField(Document,
                                    verbose_name=_('document'),
                                    on_delete=models.CASCADE,
                                    primary_key=True)
    attachment_type = models.SmallIntegerField(_('attachmentType'))

    AttachmentType = enum('AttachmentType', 'SURGICAL', 'MEDICAL', 'FAMILIAL',
                          'TRAUMA', 'MEDICAL_REPORTS')

    def delete(self, *args, **kwargs):
        super(PatientDocument, self).delete(*args, **kwargs)
        self.document.delete()

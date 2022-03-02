from flask_wtf import FlaskForm
# from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, BooleanField, StringField, PasswordField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from autoservisas import models


MESSAGE_BAD_EMAIL = 'Neteisingas el.pašto adresas.'


class RegistracijosForma(FlaskForm):
    vardas = StringField('Vardas', [DataRequired()])
    el_pastas = StringField('El.paštas', [DataRequired(), Email(MESSAGE_BAD_EMAIL)])
    slaptazodis1 = PasswordField('Slaptažodis', [DataRequired()])
    slaptazodis2 = PasswordField('Pakartokite slaptažodį', [EqualTo('slaptazodis1', "Slaptažodis turi sutapti.")])
    submit = SubmitField('Prisiregistruoti')

    def tikrinti_varda(form, vardas):
        vartotojas = models.Vartotojas.query.filter_by(vardas=vardas.data).first()
        if vartotojas:
            raise ValidationError('Toks vartotojas jau egzistuoja. Pasirinkite kitą vardą.')

    def tikrinti_pasta(form, el_pastas):
        vartotojas = models.Vartotojas.query.filter_by(el_pastas=el_pastas.data).first()
        if vartotojas:
            raise ValidationError('Vartotojas su jūsų nurodytu el.pašto adresu jau egzistuoja.')


class ProfilioForma(FlaskForm):
    vardas = StringField('Vardas', [DataRequired()])
    el_pastas = StringField('El.paštas', [DataRequired(), Email(MESSAGE_BAD_EMAIL)])
    submit = SubmitField('Atnaujinti')

    def tikrinti_varda(form, vardas):
        vartotojas = models.Vartotojas.query.filter_by(vardas=vardas.data).first()
        if vartotojas:
            raise ValidationError('Vartotojas su jūsų nurodytu vardu jau egzistuoja. Pasirinkite kitą vardą.')

    def tikrinti_pasta(form, el_pastas):
        vartotojas = models.Vartotojas.query.filter_by(el_pastas=el_pastas.data).first()
        if vartotojas:
            raise ValidationError('Vartotojas su jūsų nurodytu el.pašto adresu jau egzistuoja.')


class PrisijungimoForma(FlaskForm):
    el_pastas = StringField('El. paštas', [DataRequired(), Email(MESSAGE_BAD_EMAIL)])
    slaptazodis1 = PasswordField('Slaptažodis', [DataRequired()])
    prisiminti = BooleanField('Prisiminti mane')
    submit = SubmitField('Prisijungti')


class AutomobilioRegistracija(FlaskForm):
    marke = StringField('Markė', [DataRequired()])
    modelis = StringField('Modelis', [DataRequired()])
    pagaminimo_metai = IntegerField('Pagaminimo metai', [DataRequired()])
    variklis = StringField('Variklis', [DataRequired()])
    valstybinis_nr = StringField('Valstyvinis NR', [DataRequired()])
    vin_kodas = StringField('VIN kodas', [DataRequired()])
    submit = SubmitField('Užregistruoti automobilį')

    def tikrinti_vin(form, vin_kodas):
        automobilis = models.Automobiliai.query.filter_by(vin_kodas=vin_kodas.data).first()
        print("XXXXXXXXXXXX", automobilis)
        if automobilis:
            raise ValidationError('Su tokiu VIN kodu jau egzistuoja autromobilis')


class RemontoDarbaiForma(FlaskForm):
    gedimo_aprasymas = TextAreaField('Gedimo aprašymas', [DataRequired()])
    submit = SubmitField('Užregistruoti remontui')


class RemontoDarbuStatusas(FlaskForm):
    statusas = SelectField('Statusas', choices=["NAUJAS", "PRIIMTAS", "REMONTUOJAMAS", "LAUKIAMA DETALIŲ", "ĮVYKDYTAS", "ATIDUOTAS"])
    remonto_kaina = IntegerField('Remonto kaina', [DataRequired()])
    gedimo_aprasymas = TextAreaField('Gedimo aprašymas', [DataRequired()])
    submit = SubmitField('Patvirtinti')


class AtsarginesDetalesForma(FlaskForm):
    tiekejas = SelectField('Tiekėjas', choices=["AD Baltic", "InterCars", "AutoAibė", "Tekstara", "Kita..."])
    detale = StringField('Detalė', [DataRequired()])
    detales_kaina = IntegerField('Detalės kaina', [DataRequired()])
    kiekis = IntegerField('Kiekis', [DataRequired()])
    submit = SubmitField('Patvirtinti')

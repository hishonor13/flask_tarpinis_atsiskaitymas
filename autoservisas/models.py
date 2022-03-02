from datetime import datetime
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, current_user
# from sqlalchemy import DateTime
from autoservisas import db


class Vartotojas(db.Model, UserMixin):
    __tablename__ = 'vartotojai'
    id = db.Column(db.Integer, primary_key=True)
    vardas = db.Column('Vartotojo vardas', db.String(200), nullable=False)
    el_pastas = db.Column('El.paštas', db.String(200), unique=True, nullable=False)
    slaptazodis1 = db.Column('Slaptažodis', db.String(200), nullable=False)
    registracijos_data = db.Column(db.DateTime(), default = datetime.utcnow)
    is_admin = db.Column('Administratorius', db.Boolean(), default=False)
    is_staf = db.Column('Darbuotojas', db.Boolean(), default=False)

    def __repr__(self) -> str:
        return self.vardas


class Automobiliai(db.Model):
    __tablename__ = 'automobiliai'
    id = db.Column(db.Integer, primary_key=True)
    marke = db.Column('Automobilio marke', db.String(30), nullable=False)
    modelis = db.Column('Automobilio modelis', db.String(30), nullable=False)
    pagaminimo_metai = db.Column('Pagaminimo metai', db.Integer, nullable=False)
    variklis = db.Column('Automobilio variklis', db.String(30), nullable=False)
    valstybinis_nr = db.Column('Valstybinis numeris', db.String(15), nullable=False)
    vin_kodas = db.Column('VIN kodas', db.String(17), unique=True, nullable=False)

    vartotojo_id = db.Column(db.Integer, db.ForeignKey('vartotojai.id'))
    vartotojas = db.relationship("Vartotojas", lazy=True)

    def __repr__(self) -> str:
        return f'{self.valstybinis_nr} - {self.marke} {self.modelis}'


class RemontoDarbai(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    remonto_registracijos_data = db.Column('Remonto registracijos data', db.DateTime(), default = datetime.utcnow)
    statusas = db.Column('Remonto statusas', db.String(30), nullable=False)
    remonto_kaina = db.Column('Remonto kaina', db.Integer, nullable=False)
    gedimo_aprasymas = db.Column('Gedimo aprašymas', db.String(300), nullable=False)

    automobilio_id = db.Column(db.Integer, db.ForeignKey('automobiliai.id'))
    automobilis = db.relationship("Automobiliai", lazy=True)
    vartotojo_id = db.Column(db.Integer, db.ForeignKey('vartotojai.id'))
    vartotojas = db.relationship("Vartotojas", lazy=True)

    def __repr__(self) -> str:
        return f'{self.automobilis} -- {self.statusas}'


class AtsarginesDetales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tiekejas = db.Column('Tiekėjas', db.String(50), nullable=False)
    detale = db.Column('Detalė', db.String(100), nullable=False)
    detales_kaina = db.Column('Detalės kaina', db.Integer, nullable=False)
    kiekis = db.Column('Kiekis', db.Integer, nullable=False)

    automobilio_id = db.Column(db.Integer, db.ForeignKey('automobiliai.id'))
    automobilis = db.relationship("Automobiliai", lazy=True)

        
class Adminitratorius(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin



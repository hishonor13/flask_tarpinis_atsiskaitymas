from flask import redirect, request, render_template, flash, url_for
from flask_bcrypt import Bcrypt
from flask_login import logout_user, login_user, login_required, current_user

from autoservisas.models import Vartotojas, Adminitratorius, Automobiliai, RemontoDarbai
from autoservisas import forms
from autoservisas import app, db, admin


admin.add_view(Adminitratorius(Vartotojas, db.session))
admin.add_view(Adminitratorius(Automobiliai, db.session))
admin.add_view(Adminitratorius(RemontoDarbai, db.session))
bcrypt = Bcrypt(app)


@app.route("/admin")
@login_required
def admin():
    return redirect(url_for(admin))


@app.route('/')
def home():
    db.session.rollback()
    return render_template('base.html', current_user=current_user)


@app.route('/registracija', methods=['GET', 'POST'])
def registracija():
    if current_user.is_authenticated:
        flash('Atsijunkite, kad priregistruoti naują vartotoją.')
        return redirect(url_for('home'))
    form = forms.RegistracijosForma()
    if form.validate_on_submit():
        naujas_vartotojas = Vartotojas.query.filter_by(el_pastas=form.el_pastas.data).first()
        if naujas_vartotojas is None:
            koduotas_slaptazodis = bcrypt.generate_password_hash(form.slaptazodis1.data).decode('utf-8')
            pirmo_vartotojo_tikrinimas = not Vartotojas.query.first()
            naujas_vartotojas = Vartotojas(
                vardas = form.vardas.data,
                el_pastas = form.el_pastas.data,
                slaptazodis1 = koduotas_slaptazodis,
                is_admin = pirmo_vartotojo_tikrinimas
            )
            db.session.add(naujas_vartotojas)
            db.session.commit()
            flash('Sėkmingai prisiregistravote! Galite prisijungti.', 'success')
        else:
            flash('Toks vartotojo vardas arba el. paštas jau egzistuoja', 'danger')
        return redirect(url_for('home'))
    return render_template('registracija.html', form=form, current_user=current_user)


@app.route('/prisijungimas', methods=['GET', 'POST'])
def prisijungimas():
    if current_user.is_authenticated:
        flash('Vartotojas jau prisijungęs. Atsijunkite ir bandykite iš naujo.')
        return redirect(url_for('home'))
    form = forms.PrisijungimoForma()
    if form.validate_on_submit():
        user = Vartotojas.query.filter_by(el_pastas=form.el_pastas.data).first()
        if user and bcrypt.check_password_hash(user.slaptazodis1, form.slaptazodis1.data):
            login_user(user, remember=form.prisiminti.data)
            return redirect(url_for('home'))
        else:
            flash('Prisijungti nepavyko, neteisingas el.paštas arba slaptažodis.', 'danger')
    return render_template('prisijungimas.html', form=form, current_user=current_user)


@app.route('/automobilio_registracija', methods=['GET', 'POST'])
@login_required
def automobilio_registracija():
    form = forms.AutomobilioRegistracija()
    if form.validate_on_submit():
        naujas_automobilis = Automobiliai(
            marke = form.marke.data,
            modelis = form.modelis.data,
            pagaminimo_metai = form.pagaminimo_metai.data,
            variklis = form.variklis.data,
            valstybinis_nr = form.valstybinis_nr.data,
            vin_kodas = form.vin_kodas.data,
            vartotojo_id = current_user.id
        )
        try:
            db.session.add(naujas_automobilis)
            db.session.commit()
        except:
            flash('Su tokiu VIN kodu jau egzistuoja atomobilis', 'danger')
        else:
            flash('Sėkmingai užregistravote automobilį', 'success')
        return redirect(url_for('automobilio_registracija'))
    return render_template('automobilio_registracija.html', form=form, current_user=current_user)


@app.route('/manoautomobiliai', methods=['GET', 'POST'])
@login_required
def manoautomobiliai():
    mano_automobiliai = Automobiliai.query.filter_by(vartotojas=current_user)
    return render_template('manoautomobiliai.html', mano_automobiliai=mano_automobiliai, current_user=current_user)


@app.route('/remonto_darbai', methods=['GET', 'POST'])
@login_required
def remonto_darbai():
    form = forms.RemontoDarbaiForma()
    mano_automobiliai = Automobiliai.query.filter_by(vartotojas=current_user)
    if form.validate_on_submit():
        nauja_registracija_remontui = RemontoDarbai(
            statusas = "NAUJAS",
            remonto_kaina = int(),
            gedimo_aprasymas = form.gedimo_aprasymas.data,
            automobilio_id = request.form.get('pasirinkimas'),
            vartotojo_id = current_user.id
        )
        db.session.add(nauja_registracija_remontui)
        db.session.commit()
        flash('Automobilus užregistruotas remontui', 'success')
        return redirect(url_for('home'))
    return render_template('remonto_darbai.html', form=form, mano_automobiliai=mano_automobiliai, current_user=current_user)


@app.route('/remontuojami_automobiliai', methods=['GET', 'POST'])
@login_required
def remontuojami_automobiliai():
    if current_user.is_staf:
        remontuojami_automobiliai = RemontoDarbai.query.filter(RemontoDarbai.statusas != 'ATIDUOTAS')
        return render_template('remontuojami_automobiliai_redagavimui.html', remontuojami_automobiliai=remontuojami_automobiliai, current_user=current_user)
    else:
        remontuojami_automobiliai = RemontoDarbai.query.filter_by(vartotojas=current_user)
        return render_template('remontuojami_automobiliai.html', remontuojami_automobiliai=remontuojami_automobiliai, current_user=current_user)


@app.route('/atsijungimas')
def atsijungimas():
    logout_user()
    return redirect(url_for('home'))


@app.route('/darbu_statusas', methods=['GET', 'POST'])
@login_required
def darbu_statusas(id):
    # automobilis = RemontoDarbai.query.get_or_404(id)
    return render_template('darbu_statusas.html')


@app.route('/atnaujinti_irasa/<int:id>', methods=['GET', 'POST'])
@login_required
def atnaujinti_irasa(id):
    form = forms.RemontoDarbuStatusas()
    duomenu_atnaujinimas = RemontoDarbai.query.get_or_404(id)
    if request.method == 'POST':
        try:
            duomenu_atnaujinimas.remonto_kaina = form.remonto_kaina.data
            duomenu_atnaujinimas.statusas = form.statusas.data
            duomenu_atnaujinimas.gedimo_aprasymas = form.gedimo_aprasymas.data
            db.session.commit()
            flash('Atnaujinti automobilio progreso duomenys')
            return redirect('/remontuojami_automobiliai')
        except:
            flash('Įvyko atnaujinimo klaida. Duomenys neatnaujinti!')
            return redirect('/remontuojami_automobiliai')
    else:
        form.remonto_kaina.data = duomenu_atnaujinimas.remonto_kaina
        form.statusas.data = duomenu_atnaujinimas.statusas
        form.gedimo_aprasymas.data = duomenu_atnaujinimas.gedimo_aprasymas
        return render_template('/darbu_statusas.html', form=form, id=id, duomenu_atnaujinimas=duomenu_atnaujinimas, current_user=current_user)


@app.route('/profilis', methods=['GET', 'POST'])
@login_required
def profilis():
    form = forms.ProfilioForma()
    if form.validate_on_submit():
        current_user.vardas = form.vardas.data
        current_user.el_pastas = form.el_pastas.data
        db.session.commit()
        flash('Profilis atnaujintas!', 'success')
        return redirect(url_for('profilis'))
    elif request.method == "GET":
        form.vardas.data = current_user.vardas
        form.el_pastas.data = current_user.el_pastas
    return render_template('profilis.html', current_user=current_user, form=form)

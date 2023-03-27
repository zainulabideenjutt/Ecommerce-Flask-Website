from market import app
from market import db
from flask import render_template, request, redirect, url_for, flash
from market.models import Item, User
from market.forms import PurchaseForm, RegisterForm, LoginForm, SellForm,ItemRegisterForm
from flask_login import login_user, logout_user, login_required, current_user


@app.route("/")
@app.route('/home')
def home_page():
    return render_template('Home.html')


@app.route('/item_register_page', methods=['GET', "POST"])
@login_required
def item_register_page():
    form = ItemRegisterForm()
    if form.validate_on_submit():
        Item_to_create = Item(
            name=form.name.data,
            price=form.price.data,
            barcode=form.barcode.data,
            description=form.description.data
        )
        db.session.add(Item_to_create)
        db.session.commit()
        flash(
            f'Item Successfully Added ! You are Now on market page : {Item_to_create.name.capitalize()}', category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error While Creating Item : {err_msg}', category='danger')
    return render_template('Item_register.html',form=form)


@app.route('/market', methods=['GET', "POST"])
@login_required
def market_page():
    purchase_form = PurchaseForm()
    sell_form = SellForm()
    if request.method == 'POST':
        # purchase item Logic
        purchase_item = request.form.get('purchased-item')
        p_item_object = Item.query.filter_by(name=purchase_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(
                    f'Congrates! You Purchased {p_item_object.name} for {p_item_object.price}$ ', category='success')
            else:
                flash(
                    f'Unfortunately! You do not have enough money to purchase{p_item_object.name}', category='danger')
        sold_item = request.form.get('sold-item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(
                    f'Congrates! You Sold {s_item_object.name} back to Market!', category='success')
            else:
                flash(
                    f'Something went wrong with selling {s_item_object.name}', category='danger')

        return redirect(url_for('market_page'))

    if request.method == 'GET':
        owned_items = Item.query.filter_by(owner=current_user.id)
        items = Item.query.filter_by(owner=None)
    return render_template('Market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, sell_form=sell_form)


@app.route('/register', methods=['GET', "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
            username=form.username.data,
            email_address=form.email_address.data,
            password=form.password1.data
        ) 
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(
            f'Account Successfully created ! Your are logged in as : {user_to_create.username.capitalize()}', category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error While Creating User : {err_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(
            username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(
                f'Success! You logged in Successfully.You logged in as: {attempted_user.username.capitalize()}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username or Password is Incorrect ! Please try Again.',
                  category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been Successfully Logged Out .', category='info')
    return redirect(url_for('home_page'))

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask.typing import ResponseReturnValue
from flask_login import current_user, login_required, logout_user

from application import login_manager
from application.modules.accounts import services
from application.modules.accounts.forms import CreateAccountForm, LoginForm
from application.modules.accounts.models import Account

accounts = Blueprint("accounts", __name__, url_prefix="/auth")


@login_manager.user_loader
def load_user(user_id: int) -> ResponseReturnValue:
    return Account.query.get(int(user_id))


@accounts.route("/register", methods=["GET", "POST"])
def register() -> ResponseReturnValue:
    form = CreateAccountForm()
    if form.validate_on_submit():
        created_account = services.register(form)
        flash(f'Account "{created_account.email}" registered successfully. Please log in.', "success")
        return redirect(url_for("accounts.login"))
    return render_template("accounts/register.html", form=form)


@accounts.route("/login", methods=["GET", "POST"])
def login() -> ResponseReturnValue:
    if current_user.is_authenticated:
        return redirect(url_for("accounts.me"))
    form = LoginForm()
    if form.validate_on_submit() and services.log_user_in(form):
        next_page = request.args.get("next")
        return redirect(next_page) if next_page else redirect(url_for("main.index"))

    return render_template("accounts/login.html", form=form)


@accounts.route("/me")
@login_required
def me() -> ResponseReturnValue:
    return render_template("accounts/me.html", title=f"{current_user.name}")


@accounts.route("/logout")
def logout() -> ResponseReturnValue:
    if not current_user.is_authenticated:
        flash("You are not logged in, so you cannot log out!", "danger")
        return redirect(url_for("accounts.login"))

    name = current_user.name
    logout_user()
    flash(f"Goodbye, {name}.", "info")
    return redirect(url_for("main.index"))

from flask import Blueprint, render_template, request, flash
from flask_login import current_user, login_required
from .models import Note
from . import db

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        note_content = request.form.get('note_content')  # Correct form field name

        if note_content:
            new_note = Note(content=note_content, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note saved', 'success')
        else:
            flash('Note content cannot be empty.', 'error')

    return render_template("index.html", user=current_user)
# from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///journals.db'
# db = SQLAlchemy(app)

# class JournalEntry(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100))
#     content = db.Column(db.Text)

# @app.route('/')
# def home():
#     entries = JournalEntry.query.all()
#     return render_template('index.html', entries=entries)

# @app.route('/add', methods=['GET', 'POST'])
# def add_entry():
#     if request.method == 'POST':
#         title = request.form['title']
#         content = request.form['content']
#         entry = JournalEntry(title=title, content=content)
#         db.session.add(entry)
#         db.session.commit()
#         return redirect(url_for('home'))
#     return render_template('add_entry.html')

# @app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
# def edit_entry(entry_id):
#     entry = JournalEntry.query.get_or_404(entry_id)
#     if request.method == 'POST':
#         entry.title = request.form['title']
#         entry.content = request.form['content']
#         db.session.commit()
#         return redirect(url_for('home'))
#     return render_template('edit_entry.html', entry=entry)

# @app.route('/delete/<int:entry_id>', methods=['GET', 'POST'])
# def delete_entry(entry_id):
#     entry = JournalEntry.query.get_or_404(entry_id)
#     if request.method == 'POST':
#         db.session.delete(entry)
#         db.session.commit()
#         return redirect(url_for('home'))
#     return render_template('delete_entry.html', entry=entry)

# if __name__ == '__main__':
#     db.create_all()
#     app.run(debug=True)

from flask import render_template
from backend.app import app  # ✅ correct


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/manage_news')
def manage_news():
    return render_template('manage_news.html')
@app.route('/add_category_uploader')
def add_category_uploader():
    return render_template('add_category_uploader.html')
@app.route('/add_news_handle')
def add_news_handle():
    return render_template('add_news_handle.html')
@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/manage_programs')
def manage_programs():
    return render_template('manage_programs.html')
@app.route('/add_programs')
def add_programs():
    return render_template('add_programs.html')

@app.route('/add_activity_uploader')
def add_activity_uploader():
    return render_template('add_activity_uploader.html')

@app.route('/program')
def program():
    return render_template('program.html')
@app.route('/church_articles')
def church_articles():
    return render_template('church_articles.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/view_message_handle')
def view_message_handle():
    return render_template('view_message_handle.html')
@app.route('/sermons')
def sermons():
    return render_template('sermons.html')
@app.route('/manage_sermons')
def manage_sermons():
    return render_template('manage_sermons.html')
@app.route('/manage_series_sermons_resource')
def manage_series_sermons_resource():
    return render_template('manage_series_sermons_resource.html')
@app.route('/manage_series_uploader')
def manage_series_uploader():
    return render_template('manage_series_uploader.html')
@app.route('/add_category_view')
def add_category_view():
    return render_template('add_category_view.html')
@app.route('/manage_resource')
def manage_resource():
    return render_template('manage_resource.html')
@app.route('/manage_resource_category')
def manage_resource_category():
    return render_template('manage_resource_category.html')
@app.route('/view_new_series_upload')
def view_new_series_upload():
    return render_template('view_new_series_upload.html')
@app.route('/view_resource')
def view_resource():
    return render_template('view_resource.html')
@app.route('/manage_minitries')
def manage_minitries():
    return render_template('manage_minitries.html')
@app.route('/add_ministries_handle')
def add_ministries_handle():
    return render_template('add_ministries_handle.html')
@app.route('/delete_edit_ministries_handle')
def delete_edit_ministries_handle():
    return render_template('delete_edit_ministries_handle.html')
@app.route('/manage_testmonies')
def manage_testmonies():
    return render_template('manage_testmonies.html')
@app.route('/submit_testmonies')
def submit_testmonies():
    return render_template('submit_testmonies.html')

@app.route('/approve_testmonies')
def approve_testmonies():
    return render_template('approve_testmonies.html')
@app.route('/testmonies')
def testmonies():
    return render_template('testmonies.html')
@app.route('/ministries')
def ministries():
    return render_template('ministries.html')
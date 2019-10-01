from flask import render_template, redirect, url_for, request, flash
from elastic_app_search import exceptions as ex_app_search
from requests import exceptions as ex_requests
from app import app, client_app_search, client_blog_search
from app.searchForm import SearchForm
from app.postForm import PostForm


@app.route('/')
@app.route('/index')
def index():
    # readme section instead of Index
    return render_template('index.html', title='Home')


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    engine_name = 'flask-app-search'
    if request.method == 'POST':
        if form.validate_on_submit():
            # Paging:
            # documents = client_app_search.search(engine_name, form.searchbox.data,
            # {"page": {"size": 25, "current": 3}})
            try:
                documents = client_app_search.search(engine_name, form.searchbox.data,
                                                     {"page": {"size": app.config['POSTS_PER_PAGE']}})
            except ex_requests.ConnectionError:
                # connection error
                flash('Connection Error!! Please check connection to App-search.')
                return redirect(url_for('search'))

            # print("Method: " + request.method)
            return render_template('search.html', title='Search', form=form, search_results=documents,
                                   query=form.searchbox.data)
        else:
            return redirect(url_for('search'))
    else:
        if request.args.get('page') and request.args.get('query'):
            # print("Other: " + str(form.validate_on_submit()))
            # print("Page: " + request.args.get('page'))
            # print("Query: " + request.args.get('query'))
            # print("Method: " + request.method)
            try:
                documents = client_app_search.search(engine_name, request.args.get('query'),
                                                     {"page": {"current": int(request.args.get('page')),
                                                               "size": app.config['POSTS_PER_PAGE']}})
            except ex_app_search.BadRequest:
                # 100 pages limit or other bad requests
                flash('Bad request or requested more than 100 pages.')
                return render_template('search.html', title='Search', form=form,
                                       query=request.args.get('query'))

            return render_template('search.html', title='Search', form=form, search_results=documents,
                                   query=request.args.get('query'))
        else:
            return render_template('search.html', title='Search', form=form)


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    form = SearchForm()
    engine_name = 'blog-posts'

    if form.validate_on_submit():
        try:
            documents = client_blog_search.search(engine_name, form.searchbox.data,
                                                  {"page": {"size": app.config['POSTS_PER_PAGE']}})
        except ex_requests.ConnectionError:
            # connection error
            flash('Connection Error!! Please check connection to App-search.')
            return redirect(url_for('posts'))

        return render_template('posts.html', title='Posts', form=form, search_results=documents,
                               query=form.searchbox.data)
    else:
        try:
            documents = client_blog_search.list_documents(engine_name, current=1, size=app.config['POSTS_PER_PAGE'])
        except ex_requests.ConnectionError:
            # connection error
            flash('Connection Error!! Please check connection to App-search.')
            return render_template('posts.html', title='Posts', form=form)
        return render_template('posts.html', title='Posts', form=form, search_results=documents)


@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    formPost = PostForm()
    engine_name = 'blog-posts'
    if formPost.validate_on_submit():
        # print("Clicked: " + str(formPost.validate_on_submit()))
        # Index document (https://github.com/elastic/app-search-python#indexing-creating-or-updating-a-single-document)
        document = {
            'title': formPost.title.data,
            'title_uri': formPost.titleUri.data,
            'date': str(formPost.date.data),
            'author': formPost.author.data,
            'content': formPost.content.data
        }
        ret_val = client_blog_search.index_document(engine_name, document)
        flash('Document added. ID: {}'.format(ret_val))
        return render_template('newpost.html', title='New post', form=formPost)
    else:
        return render_template('newpost.html', title='New post', form=formPost)

from bookshuffle import app, render_template, request
import random
import requests

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        genre = request.form.get("genreChooser")
        page = request.form.get("pageChooser")
        COVER_API_URL = 'http://covers.openlibrary.org/b/id/{cover_id}-L.jpg' 
        url = f'https://openlibrary.org/search.json?subject={genre}&limit=100'
        response = requests.get(url)
        data = response.json()
        books = []

        for doc in data['docs']:
            if 'number_of_pages_median' in doc:
                title = doc.get('title', '')
                cover_id = doc.get('cover_i')
                cover_url = COVER_API_URL.format(cover_id=cover_id) if cover_id else None
                books.append({'title': title, 'cover_url': cover_url})

        if page == "Any":
            page = "9999999"  # Assign a large value to page that won't match any valid page numbers
            if genre == "RandomGenre":
                listOfGenres = ['Fiction', 'Nonfiction', 'Historical Fiction', 'Mystery', 'Drama', 'Science Fiction']
                randomGenre = random.choice(listOfGenres)
                newUrl = f'https://openlibrary.org/search.json?subject={randomGenre}&limit=100'
                response1 = requests.get(newUrl)
                data1 = response1.json()
                for doc1 in data1['docs']:
                    title = doc1.get('title', '')
                    cover_id = doc1.get('cover_i')
                    cover_url = COVER_API_URL.format(cover_id=cover_id) if cover_id else None
                    books.append({'title': title, 'cover_url': cover_url})

        if int(page) == 400:
            books = [book for book in books if 'number_of_pages_median' in data['docs'] and data['docs']['number_of_pages_median'] >= 400]

        if int(page) < 100:
            books = [book for book in books if 'number_of_pages_median' in data['docs'] and data['docs']['number_of_pages_median'] < 100]

        if books:
            random_book = random.choice(books)
            return render_template("index.html", random_book=random_book, titles1=True)

    return render_template("index.html")

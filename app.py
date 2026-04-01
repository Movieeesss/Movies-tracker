@app.route('/run-movies')
def trigger_movies():
    if movies:
        threading.Thread(target=movies.run_all).start()
        return "OK", 200
    return "Error", 404

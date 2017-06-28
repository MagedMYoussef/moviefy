from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views import generic
from moviefy_lstm.lstm_model import runLSTM

def recommend(request):
    # Get the text the user typed to perform the algorithm on.
    # The template has a form that makes a POST request, we will go through this
    # request and get the value of the text entered
    if request.method == 'POST':
        post_request = request.POST
        '''
        Type of return from POST
        <QueryDict: {'csrfmiddlewaretoken': ['qeweqewr'], 'text-area1': ['I hate these new features On #ThisPhone after the update.']}>
        We well have key = 'text-area1', 'text-area2' or 'text-area3' based on where the user typed the text.
        '''
        text_area = dict(post_request.dict())
        '''
        Extracted text will be something like this
        ['I hate these new features On #ThisPhone after the update.']
        '''
        user_text = [value for key, value in text_area.items() if 'text-area' in key.lower()]

        '''
        List of 5 Feelings returned from the LSTM Model
            "anger": feelings[0],
            "disgust":feelings[1],
            "fear":feelings[2],
            "joy":feelings[3],
            "sadness":feelings[4],
        '''
        '''
        Shape of data: data = [feelings, movies_json]
        feelings = data[0]
        movies_json = data[1]
        '''
        data = runLSTM(str(user_text[0]))



    # If the user came to this page using other methods than POST like GET request
    # we will redirect them to the original tryitout page to enter a new submission.
    # this can happen when the user access the page "http://127.0.0.1:8000/recommend/" directly
    # not as the usual way after submission.
    else:
        return redirect("try:index")

    # Construct a context to send the data to the template in order to be displayed.
    context = {
        'recommend': True,
        'feelings': data[0],
        'movies_json': data[1],
        'user_text': user_text[0],
    }

    '''
    TODO:
    [OK] This function will have to take the text user typed in the textarea
    [What we did] Template Passes the input text through variable called 'user_text' and this text is extracted from
    the textarea in the FORM
    [OK] We need to know which textarea box we are in ! .. the default now is the first box only.

    [OK] ** We will need to create a new App for the machine learning model and create an API for it.
    Then process the algorithm on this text to determine:
    [OK] 1- Feelings map
    [OK] 2- Top 3 recommended movies
    [OK] Then it send back the feelings map data and recommended movies to render the page again
    '''

    return render(request, 'recommend.html', context)


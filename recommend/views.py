from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views import generic

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
        if request.POST.get('text-area', False):
            user_text = str(request.POST['text-area'])
            #print ("My input text is " + user_text)  # watch your command line
        '''
    else:
        return render(request, 'tryitout.html')

    context = {
        'recommend': True,
        'user_text': user_text[0],
    }

    '''
    TODO:
    [OK] This function will have to take the text user typed in the textarea
    [What we did] Template Passes the input text through variable called 'user_text' and this text is extracted from
    the textarea in the FORM
    [NEXT] We need to know which textarea box we are in ! .. the default now is the first box only.

    then process the algorithm on this text to determine:
    1- Feelings map
    2- Top 3 recommended movies
    Then it send back the feelings map data and recommended movies to render the page again

    '''


    return render(request, 'recommend.html' , context)


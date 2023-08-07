from django.shortcuts import render
from .models import Finch
# Create your views here.
# finches = [
#     {'name': 'Evening Grosbeak', 'threats': 'Deforestation, disease, loss of food sources due to pesticides', 'habitat': 'Northern and montane forests',
#         'notes': 'The Evening Grosbeak does not have a complex song, but rather draws from a collection of sweet, piercing notes and burry chirps.'},
#     {'name': 'Pine Grosbeak', 'threats': 'Possibly climate change', 'habitat': 'Open boreal forest',
#         'notes': 'Locals in Newfoundland affectionately call Pine Grosbeaks "mopes" because they can be so tame and slow moving. Pine Grosbeaks declined by 2.4 percent per year between 1966 and 2015, resulting in a cumulative decline of 70 percent.'},
#     {'name': 'Purple Finch', 'threats': 'Competition with the House Finch over food and breeding grounds, possibly climate change', 'habitat': 'Mixed northern, montane, and boreal forests',
#         'notes': 'Purple Finches sometimes imitate other birds in their songs, including Barn Swallows, American Goldfinches, Eastern Towhees, and Brown-headed Cowbirds. Purple Finch populations decreased by almost 1.5 percent per year between 1966 and 2014.'},
#     {'name': 'Hoary Redpoll', 'threats': 'Possibly climate change', 'habitat': 'Arctic tundra',
#         'notes': 'Some Hoary Redpolls winter in northern areas that are near their nesting grounds that remain dark, or nearly so, for months at a time.'},
# ]


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def finches_index(request):
    finches = Finch.objects.all()
    return render(request, 'finches/index.html', {'finches': finches})


def finches_detail(request, finch_id):
    finch = Finch.objects.get(id=finch_id)
    return render(request, 'finches/detail.html', {'finch': finch})

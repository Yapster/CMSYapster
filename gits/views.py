from django.shortcuts import render
#from github import Github
from django.conf import settings

def git_repos(request):
    g = Github(settings.USER_GITHUB, settings.PWD_GITHUB)
    repos = g.get_user().get_repos()

    return render(request,
                  "gits/home.html",
        {"repos": repos})
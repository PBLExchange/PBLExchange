from django.shortcuts import render, HttpResponseRedirect, Http404, HttpResponse, reverse, get_object_or_404


# Create your views here.
def users(base_template='pblexchange_base.html', **kwargs):
    return Http404

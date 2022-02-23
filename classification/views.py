from django.forms import formsets
from django.forms.forms import Form
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic
from django.forms.formsets import formset_factory
from django.forms import modelformset_factory
from django.db.models import Q, manager

import time

import json

from .forms import EditNomenclatureForm, NomenclatureForm, get_unique_values
from .models import Nomenclature

@login_required
def index(request):
    return render(
        request,
        'index.html',
        context={},
    )

def update(request, **args):
    data = request.POST

    try:
        for column_name in ['units', 'group', 'nomenclature_group', 'nomenclature_group_detail', 'brand']:
            if data[column_name] != '':
                Nomenclature.objects.filter(**{f'{column_name}': data[column_name]}).\
                    update(**{f'{column_name}': data[f'{column_name}-new']})
            elif data[f'{column_name}-new'] != '':
                Nomenclature.objects.create(code=round(time.time()), ntype='service',
                                            **{f'{column_name}': data[f'{column_name}-new']})

        return HttpResponse(json.dumps({'success': True}), content_type="application/json", status=200)
    except:
        return HttpResponse(json.dumps({'errors': 'error'}), content_type="application/json", status=400)

class NomenclatureListView(PermissionRequiredMixin, generic.ListView):
    model = Nomenclature
    permission_required = ('classification.view_nomenclature', 'classification.change_nomenclature')
    paginate_by = 15

    def get_queryset(self):
        return Nomenclature.objects.filter(
            (
                Q(units__isnull=True) | 
                Q(group__isnull=True) | 
                Q(nomenclature_group__isnull=True) | 
                Q(nomenclature_group_detail__isnull=True) | 
                Q(brand__isnull=True)
            ) & Q(ntype__exact='AS' if self.kwargs['type'] == 'as' else 'Техніка')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = formset_factory(NomenclatureForm, extra=0)(initial=context['object_list'].values())
        context['pages'] = list(
            range(
                1 + max(0, context['page_obj'].number - 5),
                min(
                    context['page_obj'].number  + 5,
                    context['page_obj'].paginator.num_pages
                ) + 1
            )
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        formset = modelformset_factory(model=Nomenclature, form=NomenclatureForm)(request.POST)
        errors = formset.errors

        if formset.is_valid():
            formset.save()
            return HttpResponse(json.dumps({'success': True}), content_type="application/json", status=200)
        else:
            print(errors)
            return HttpResponse(json.dumps({'errors': errors}), content_type="application/json", status=400)


class NomenclatureListView_edited(PermissionRequiredMixin, generic.ListView):
    model = Nomenclature
    permission_required = ('classification.view_nomenclature', 'classification.change_nomenclature')
    template_name = 'classification/nomenclature_list_edited.html'

    def get_queryset(self):
        manager_name = self.request.user.first_name + " " + self.request.user.last_name

        objects = Nomenclature.objects.filter(
            (
                Q(units__isnull=True) | 
                Q(group__isnull=True) | 
                Q(nomenclature_group__isnull=True) | 
                Q(nomenclature_group_detail__isnull=True) | 
                Q(brand__isnull=True)
            ) & Q(ntype__exact='AS' if self.kwargs['type'] == 'as' else 'Техніка') & Q(actual__exact=True) & (
                Q(manager__exact=manager_name) |
                Q(manager__isnull=True)
            )
        ).exclude(
            Q(nomenclature__exact='') |
            Q(nomenclature__isnull=True)
        ).order_by('nomenclature')[:15]

        for obj in objects:
            obj.manager = manager_name
            obj.save()

        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = formset_factory(NomenclatureForm, extra=0)(initial=context['object_list'].values())
        context['edit_form_labels'] = [
            'Одиниці виміру', 'Товарна група', 'Номенклатурна група', 'Номенклатурна група деталізація', 'Бренд'
        ]
        context['edit_form'] = EditNomenclatureForm()
        
        values_dict = {}

        for column_name in ['units', 'group', 'nomenclature_group', 'nomenclature_group_detail', 'brand']:
            values_dict[column_name] = get_unique_values(column_name)

        for obj in list(context['formset']) + [context['edit_form']]:
            for column_name in ['units', 'group', 'nomenclature_group', 'nomenclature_group_detail', 'brand']:
                obj.fields[column_name].widget.choices = values_dict[column_name]

        return context

    def post(self, request, *args, **kwargs):
        formset = modelformset_factory(model=Nomenclature, form=NomenclatureForm)(request.POST, queryset=self.get_queryset())
        errors = formset.errors

        if formset.is_valid():
            formset.save()
            return HttpResponse(json.dumps({'success': True}), content_type="application/json", status=200)
        else:
            print(errors)
            return HttpResponse(json.dumps({'errors': errors}), content_type="application/json", status=400)
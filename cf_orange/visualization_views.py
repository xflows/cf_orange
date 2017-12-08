import Orange
from django.shortcuts import render



def orng_table_to_dict(data):
    attrs, metas, data_new = [], [], []
    try:
        class_var = data.domain.class_var.name
    except:
        class_var = ''
    for m in data.domain.metas:
        metas.append(m[0]) #?? todo
    for a in data.domain.attributes:
        attrs.append(a.name)
    pretty_float = lambda x, a: '%.3f' % x if a is Orange.data.variable.ContinuousVariable and x!='?' else x
    for inst in range(len(data)):
        inst_new = []
        for a in data.domain.variables:
            value = data[inst][a.name].value
            inst_new.append((a.name, pretty_float(value, a)))
        for m in data.domain.metas:
            value = data[inst][m].value
            a = data.domain.get_meta(m)
            inst_new.append((a.name, pretty_float(value, a)))
        data_new.append(inst_new)
    return {'attrs':attrs, 'metas':metas, 'data':data_new, 'class_var':class_var}



def table_viewer(request, input_dict, output_dict, widget):
    data = input_dict['data']
    a=render(request, 'visualizations/table_viewer.html',
                  {'widget': widget, 'input_dict': input_dict, 'output_dict': orng_table_to_dict(data)})
    return render(request, 'visualizations/table_viewer.html',
                  {'widget': widget, 'input_dict': input_dict, 'output_dict': orng_table_to_dict(data)})

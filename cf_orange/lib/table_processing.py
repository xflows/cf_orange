
def orange_select_attrs(input_dict):
    return input_dict


def orange_select_attrs_post(postdata, input_dict, output_dict):
    data = Orange.data.Table(input_dict['data'])

    new_attrs = []
    for name in postdata['attrs']:
        new_attrs.append(str(name))

    try:
        new_attrs.append(str(postdata['ca'][0]))
        class_attr = True
    except:
        class_attr = False

    new_domain = Orange.data.Domain(new_attrs, class_attr, data.domain)

    try:
        for meta in postdata['ma']:
            if data.domain.has_meta(str(meta)):
                new_domain.addmeta(Orange.feature.Descriptor.new_meta_id(), data.domain.getmeta(str(meta)))
            else:
                new_domain.add_meta(Orange.feature.Descriptor.new_meta_id(), data.domain[str(meta)])
    except:
        pass

    new_data = Orange.data.Table(new_domain, data)

    output_dict = {'data': new_data}
    return output_dict


def orange_select_data(input_dict):
    return input_dict


def orange_build_filter(val, attr, data):
    import Orange

    pos = 0
    try:
        pos = data.domain.meta_id(attr)
    except Exception as e:
        pos = data.domain.variables.index(attr)

    if val['operator'] == ">":
        return (
            Orange.data.filter.ValueFilterContinuous(
                position=pos,
                ref=float(val['values'][0]),
                oper=Orange.data.filter.ValueFilter.Greater
            )
        )
    elif val['operator'] == "<":
        return (
            Orange.data.filter.ValueFilterContinuous(
                position=pos,
                ref=float(val['values'][0]),
                oper=Orange.data.filter.ValueFilter.Less
            )
        )
    elif val['operator'] == "=":
        return (
            Orange.data.filter.ValueFilterContinuous(
                position=pos,
                ref=float(val['values'][0]),
                oper=Orange.data.filter.ValueFilter.Equal
            )
        )
    elif val['operator'] == "<=":
        return (
            Orange.data.filter.ValueFilterContinuous(
                position=pos,
                ref=float(val['values'][0]),
                oper=Orange.data.filter.ValueFilter.LessEqual
            )
        )
    elif val['operator'] == ">=":
        return (
            Orange.data.filter.ValueFilterContinuous(
                position=pos,
                ref=float(val['values'][0]),
                oper=Orange.data.filter.ValueFilter.GreaterEqual
            )
        )
    elif val['operator'] == "between":
        return (
            Orange.data.filter.ValueFilterContinuous(
                position=pos,
                min=float(val['values'][0]),
                max=float(val['values'][1]),
                oper=Orange.data.filter.ValueFilter.Between
            )
        )
    elif val['operator'] == "outside":
        return (
            Orange.data.filter.ValueFilterContinuous(
                position=pos,
                min=float(val['values'][0]),
                max=float(val['values'][1]),
                oper=Orange.data.filter.ValueFilter.Outside
            )
        )
    elif val['operator'] in ["equals", "in"]:
        vals = []
        for v in val['values']:
            vals.append(Orange.data.Value(attr, str(v)))
        return (
            Orange.data.filter.ValueFilterDiscrete(
                position=pos,
                values=vals
            )
        )
    elif val['operator'] == "s<":
        return (
            Orange.data.filter.ValueFilterString(
                position=pos,
                ref=str(val['values'][0]),
                oper=Orange.data.filter.ValueFilter.Less,
                case_sensitive=bool(val['case'])
            )
        )
    elif val['operator'] == "s>":
        return (
            Orange.data.filter.ValueFilterString(
                position=pos,
                ref=str(val['values'][0]),
                oper=Orange.data.filter.ValueFilter.Greater,
                case_sensitive=bool(val['case'])
            )
        )
    elif val['operator'] == "s=":
        return (
            Orange.data.filter.ValueFilterString(
                position=pos,
                ref=str(val['values'][0]),
                oper=Orange.data.filter.ValueFilter.Equal,
                case_sensitive=bool(val['case'])
            )
        )
    elif val['operator'] == "s<=":
        return (
            Orange.data.filter.ValueFilterString(
                position=pos,
                ref=str(val['values'][0]),
                oper=Orange.data.filter.ValueFilter.LessEqual,
                case_sensitive=bool(val['case'])
            )
        )
    elif val['operator'] == "s>=":
        return (
            Orange.data.filter.ValueFilterString(
                position=pos,
                ref=str(val['values'][0]),
                oper=Orange.data.filter.ValueFilter.GreaterEqual,
                case_sensitive=bool(val['case'])
            )
        )
    elif val['operator'] == "sbetween":
        return (
            Orange.data.filter.ValueFilterString(
                position=pos,
                min=str(val['values'][0]),
                max=str(val['values'][1]),
                oper=Orange.data.filter.ValueFilter.Between,
                case_sensitive=bool(val['case'])
            )
        )
    elif val['operator'] == "soutside":
        return (
            Orange.data.filter.ValueFilterString(
                position=pos,
                min=str(val['values'][0]),
                max=str(val['values'][1]),
                oper=Orange.data.filter.ValueFilter.Outside,
                case_sensitive=bool(val['case'])
            )
        )
    elif val['operator'] == "scontains":
        return (
            Orange.data.filter.ValueFilterString(
                position=pos,
                ref=str(val['values'][0]),
                oper=Orange.data.filter.ValueFilter.Contains,
                case_sensitive=bool(val['case'])
            )
        )
    elif val['operator'] == "snot contains":
        return (
            Orange.data.filter.ValueFilterString(
                position=pos,
                ref=str(val['values'][0]),
                oper=Orange.data.filter.ValueFilter.NotContains,
                case_sensitive=bool(val['case'])
            )
        )
    elif val['operator'] == "sbegins with":
        return (
            Orange.data.filter.ValueFilterString(
                position=pos,
                ref=str(val['values'][0]),
                oper=Orange.data.filter.ValueFilter.BeginsWith,
                case_sensitive=bool(val['case'])
            )
        )
    elif val['operator'] == "sends with":
        return (
            Orange.data.filter.ValueFilterString(
                position=pos,
                ref=str(val['values'][0]),
                oper=Orange.data.filter.ValueFilter.EndsWith,
                case_sensitive=bool(val['case'])
            )
        )


def orange_select_data_post(postdata, input_dict, output_dict):
    import Orange, json

    data = input_dict['data']
    conditions = json.loads(str(postdata['conditions'][0]))

    for cond in conditions['conditions']:
        data_filter = None
        if cond['condition'][0]['operator'] in ["is defined", "sis defined"]:
            data_filter = Orange.data.filter.IsDefined(domain=data.domain)
            data_filter.negate = cond['negate']
            data_filter.check[str(cond['condition'][0]['attr'])] = 1
        else:
            data_filter = Orange.data.filter.Values()
            data_filter.domain = data.domain
            data_filter.negate = cond['negate']
            data_filter.conjunction = False
            for or_cond in cond['condition']:
                attr = data.domain[str(or_cond['attr'])]
                data_filter.conditions.append(build_filter(or_cond, attr, data))
        data = data_filter(data)

    return {'data': data}


def cforange_split_dataset(input_dict):
    import orange
    output_dict = {}
    data = input_dict['dataset']
    selection = orange.MakeRandomIndices2(data,float(input_dict['p']))
    train_data = data.select(selection,0)
    test_data = data.select(selection,1)
    output_dict['train_data']=train_data
    output_dict['test_data']=test_data
    return output_dict




def cforange_discretize(input_dict):
    import orange
    from collections import defaultdict

    input_obj = input_dict['dataset']
    intervals = input_dict['intervals']
    output_tables = []

    input_type = input_obj.__class__.__name__

    if input_type == 'DBContext':
        context = input_obj
        input_tables = [context.orng_tables[tname] for tname in context.tables]
    elif input_type != 'list':
        input_tables = [input_obj]
    else:
        input_tables = input_obj

    discretizerIndex = int(input_dict['discretizer_id'])
    discretizers = [
        ("Equi-distant discretization",orange.EquiDistDiscretization), #numberOfIntervals
        ("Quantile-based discretization", orange.EquiNDiscretization), #numberOfIntervals
        ("Entropy-based discretization", orange.EntropyDiscretization), #no arguments
        ("Bi-modal discretization", orange.BiModalDiscretization),#no arguments
        ("Fixed discretization", orange.EquiNDiscretization)#FixedDiscretization) #points
    ]

    options = {}
    points = defaultdict(dict)
    if not intervals:
        if discretizerIndex in [4]:
            #find all cut-off points
            user_points = [float(a) for a in input_dict['points'].replace(" ","").split(",")]
            options['points']=sorted(user_points)
        elif discretizerIndex in [0,1]:
            options['numberOfIntervals']=int(input_dict['numberOfIntervals'])

    d = discretizers[discretizerIndex][1](**options)

    for inputdata in input_tables:
        newattrs = []
        for attr in inputdata.domain.attributes:
            if attr.varType == orange.VarTypes.Continuous:

                if not intervals:
                    # No intervals provided, calculate them
                    newattr = d(attr,inputdata) if discretizerIndex in [0,2,3] else d.constructVariable(attr)
                else:
                    # Use the input interval dictionary
                    attr_points = intervals[inputdata.name][attr.name]
                    idisc = orange.IntervalDiscretizer(points = attr_points)
                    newattr = idisc.constructVariable(attr)

                newattr.name = attr.name
                newattrs.append(newattr)
                points[inputdata.name][attr.name] = newattr.get_value_from.transformer.points
            else:
                newattrs.append(attr)
        name = inputdata.name
        newdomain = orange.Domain(newattrs, inputdata.domain.classVar)
        newdomain.addmetas(inputdata.domain.getmetas())
        new_t = orange.ExampleTable(newdomain, inputdata)
        new_t.name = name
        output_tables.append(new_t)

    if input_type == 'DBContext':
        output = input_obj.copy()
        output.orng_tables = dict(list(zip(input_obj.tables, output_tables)))
    elif input_type != 'list':
        output = output_tables[0]
    else:
        output = output_tables

    output_dict = {'odt': output, 'discr_intervals': points}
    return output_dict

def cforange_best_natts(input_dict):
    import orange
    import orngFSS
    data = input_dict['dataset']
    scores = input_dict['scores']
    n = int(input_dict['n'])
    new_dataset = orngFSS.selectBestNAtts(data,scores,n)
    output_dict={}
    output_dict['new_dataset'] = new_dataset
    return output_dict

def cforange_atts_above_thresh(input_dict):
    import orange
    import orngFSS
    data = input_dict['dataset']
    scores = input_dict['scores']
    thresh = float(input_dict['thresh'])
    new_dataset = orngFSS.selectAttsAboveThresh(data,scores,thresh)
    output_dict={}
    output_dict['new_dataset'] = new_dataset
    return output_dict


def cforange_odt_to_kdic(input_dict):
    from .odt_converters import toKDICstring, toKDICheader
    output_dict = {}
    f = toKDICheader(input_dict['odt'])
    output_dict['kdic'] = f.getvalue()
    f2 = toKDICstring(input_dict['odt'])
    output_dict['txt'] = f2.getvalue()
    return output_dict

def cforange_odt_to_prd_fct(input_dict):
    from .odt_converters import toPRDstring, toFCTstring
    output_dict = {}
    f = toPRDstring(input_dict['odt'])
    output_dict['prd'] = f.getvalue()
    f2 = toFCTstring(input_dict['odt'])
    output_dict['fct'] = f2.getvalue()
    return output_dict

def filter_table(input_dict):
    return {'altered_data' : None}

def filter_table_finished(postdata, input_dict, output_dict):
    print(postdata)
    import Orange
    from Orange.feature import Type
    widget_id = postdata['widget_id'][0]
    # Parse the changes
    new_table = Orange.data.Table(input_dict['data']).getitems([int(x) for x in postdata.get('include',[])])
    return {'altered_data' : new_table}

def orange_table_viewer(input_dict):
    return {}

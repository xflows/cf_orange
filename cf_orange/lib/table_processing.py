
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


















# VISUALIZATIONS

def orange_pr_space(input_dict):
    return {}


def orange_eval_bar_chart(input_dict):
    return {}


def orange_eval_to_table(input_dict):
    return {}


def orange_data_table(input_dict):
    return {}


def orange_data_info(input_dict):
    return {}


def orange_definition_sentences(input_dict):
    return {}


def orange_term_candidates(input_dict):
    return {}
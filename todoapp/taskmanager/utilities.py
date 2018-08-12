"""Utilities for task manager app."""
from django.http import JsonResponse
from django.db.models.fields.files import FieldFile
from django.core.validators import validate_email
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

import json
import datetime

from .constants import DEFAULT_LIMIT, DEFAULT_OFFSET


def setup_default_meta_data(meta_dict):
    """For setting up default meta data."""
    if not('limit' in meta_dict.keys()):
        meta_dict['limit'] = DEFAULT_LIMIT
    if not('offset' in meta_dict.keys()):
        meta_dict['offset'] = DEFAULT_OFFSET

    return meta_dict


def setup_query_limit(meta_dict):
    """For setting up query with limit."""
    return meta_dict['objects'][
        meta_dict['offset']: meta_dict['offset'] + meta_dict['limit']]


class CustomJSONEncoder(json.JSONEncoder):
    """Class for serializing custom json."""

    def default(self, o):
        """Default func."""
        if isinstance(o, datetime.datetime):
            return o.strftime('%s')
        elif isinstance(o, FieldFile):
            try:
                return o.url
            except:
                return None
        return super(CustomJSONEncoder, self).default(o)


def success_response(response={}, status=200):
    """For sending success response."""
    return JsonResponse(response, encoder=CustomJSONEncoder, status=status)


def error_response(exception, request=None):
    """For sending error response."""
    response = {}
    if isinstance(exception, ValueError):
        status = 400
        error_message = exception.message
    elif isinstance(exception, KeyError):
        status = 400
        error_message = 'Parameter missing: %s' % exception.message
    else:
        status = exception.status_code
        error_message = exception.message
        response['error_code'] = exception.code
    response['error_message'] = error_message
    response['success'] = False

    return JsonResponse(response, status=status)


def fetch_request_params(request_dict):
    """
    Function to collect the parameters in request.

    Input params:
        request_dict (obj): object which contains,
            mandatory_params (list): parameter list, which should be
                in the request.
            optional_params (list): parameters, which is optional
            media_params(list): media data.
            received_data (dict): json dictionary which contains the parameters
                in the parameter list.
    Return:
        param_dict (obj): object which has the collected parameters.
    """
    param_dict = {}
    if 'mandatory_params' in request_dict.keys():
        fetch_mandatory_params(request_dict, param_dict)

    if 'optional_params' in request_dict.keys():
        fetch_optional_params(request_dict, param_dict)

    return param_dict


def fetch_mandatory_params(request_dict, param_dict):
    """Function to fetch the mandatory parameters in request."""
    for item in request_dict['mandatory_params']:
        parameter = item[0]
        value = request_dict['received_data'].get(parameter)
        if not value:
            raise KeyError('%s is missing in request params' % (parameter))
        else:
            value_dict = {}
            value_dict['value'] = value
            value_dict['parameter'] = parameter
            value_dict['type'] = item[1]
            value = check_parameter_value(value_dict)

        param_dict[parameter] = value
    return param_dict


def fetch_optional_params(request_dict, param_dict):
    """Function to fetch the optional parameters in request."""
    for item in request_dict['optional_params']:
        parameter = item[0]
        value = request_dict['received_data'].get(parameter)
        if value:
            value_dict = {}
            value_dict['value'] = value
            value_dict['parameter'] = parameter
            value_dict['type'] = item[1]
            value = check_parameter_value(value_dict)

            param_dict[parameter] = value
    return param_dict


def check_parameter_value(value_dict):
    """
    Function to check the parameter vales and type.

    Input Params:
        value_dict (obj): collection obj with following data,
            value: value collected
            parameter: parameter name.
            type: value type
    """
    if value_dict['type'] == 'str':
        return(check_str_value(value_dict))
    elif value_dict['type'] == 'int':
        return(check_int_value(value_dict))
    elif value_dict['type'] == 'email':
        return(check_email_value(value_dict))
    elif value_dict['type'] == 'date':
        return(check_date_value(value_dict))
    elif value_dict['type'] == 'password':
        return(check_password(value_dict))
    else:
        raise ValueError('Invalid parameter type')


def check_str_value(value_dict):
    """Function to check the str value, and return the value."""
    try:
        return str(value_dict['value'])
    except:
        try:
            return str(value_dict['value'].encode("utf8"))
        except:
            raise ValueError('%s must be str' % (value_dict['parameter']))


def check_int_value(value_dict):
    """Function to check the int value, and return the value."""
    try:
        return int(value_dict['value'])
    except:
        raise ValueError('%s must be int' % (value_dict['parameter']))


def check_email_value(value_dict):
    """Function to check the email value, and return the value."""
    try:
        validate_email(value_dict['value'])
    except:
        raise ValueError(
            '%s is not in valid format.' % (value_dict['parameter']))
    return value_dict['value']


def check_date_value(value_dict):
    """Function to check the date value, and return the value."""
    try:
        return datetime.datetime.fromtimestamp(
            float(value_dict['value'])).date()
    except:
        raise ValueError(
            '%s must be Unix time stamp value' % (value_dict['parameter']))


def check_password(value_dict):
    """Function to check the password validity."""
    password = value_dict['value']
    validity = check_password_validity(password)
    validity['valid']
    if not validity['valid']:
        raise ValueError(validity['message'])
    return password


def check_password_validity(password):
    """
    Function to check password validity.

    Input Params:
        password(str): password
    Returns:
        (dict): with
            valid(bool): true of false status of validity.
            message(str): message
    """
    data = {}
    try:
        password_validation.validate_password(password)
        data['valid'] = True
        data['message'] = 'Valid Password.'
    except ValidationError as e:
        data['valid'] = False
        data['message'] = '; '.join(e.messages)
    return data

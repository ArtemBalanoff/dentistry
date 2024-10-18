patient_schema = {
    'type': 'object',
    'properties': {
        'email': {'type': 'string', 'format': 'email'},
        'phone_number': {'type': 'string'},
        'id': {'type': 'integer'}, },
    'required': ['email', 'phone_number', 'id'],
    'additionalProperties': False}


doctor_schema = {
    'type': 'object',
    'properties': {
        'id': {'type': 'integer'},
        'first_name': {'type': 'string'},
        'last_name': {'type': 'string'},
        'surname': {'type': 'string'},
        'specialization': {'type': 'integer'},
        'stage': {'type': 'integer'},
    },
    'required': ['id', 'first_name', 'last_name',
                 'surname', 'specialization', 'stage'],
    'additionalProperties': False}


doctor_list_schema = {
    'type': 'array',
    'items': doctor_schema
}

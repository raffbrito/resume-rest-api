class Institution:
    def __init__(self, id, name, degree=None, field=None, start_date=None, end_date=None, description=None, institution_tags=None):
        self.id = id
        self.name = name
        self.degree = degree
        self.field = field
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.institution_tags = institution_tags or []

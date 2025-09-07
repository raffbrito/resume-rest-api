class Company:
    def __init__(self, id, name, position, start_date=None, end_date=None, description=None, company_tags=None):
        self.id = id
        self.name = name
        self.position = position
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.company_tags = company_tags or []

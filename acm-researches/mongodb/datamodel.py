class Author:
    schema = {
        "name": str,
        "dblp_profile": str
    }

    def __init__(self, name, dblp_profile):
        self.name = name
        self.dblp_profile = dblp_profile

    def to_dict(self):
        return {
            "name": self.name,
            "dblp_profile": self.dblp_profile,
        }

    @staticmethod
    def validate_data(data):
        for key, data_type in Author.schema.items():
            if key not in data or not isinstance(data[key], data_type):
                return False
        return True

class Publication:
    schema = {
        "title": str,
        "authors": list,
        "year": int,
        "abstract": str,
        "ss_id": str
    }

    def __init__(self, title, authors, year, abstract, ss_id):
        self.title = title 
        self.authors = authors 
        self.year = year 
        self.abstract = abstract
        self.ss_id = ss_id

    def to_dict(self):
        return {
            "title": self.title,
            "authors": [author.to_dict() for author in self.authors],
            "year": self.year,
            "abstract": self.abstract,
            "ss_id": self.ss_id
        }

    @staticmethod
    def validate_data(data):
        for key, data_type in Publication.schema.items():
            if key not in data or not isinstance(data[key], data_type):
                return False

        # Validate the nested address document
        for author in data["authors"]:
            if not Author.validate_data(author):
                return False

        return True

class AuthorPublications:
    schema = {
        "name": str,
        "publications": list
    }

    def __init__(self, name, publications):
        self.name = name
        self.publications = publications

    def to_dict(self):
        return {
            "name": self.name,
            "publications": [pub.to_dict() for pub in self.publications]
        }

    @staticmethod
    def validate_data(data):
        for key, data_type in AuthorPublications.schema.items():
            if key not in data or not isinstance(data[key], data_type):
                return False

        # Validate the nested address document
        for pub in data["publications"]:
            if not Publication.validate_data(pub):
                return False

        return True
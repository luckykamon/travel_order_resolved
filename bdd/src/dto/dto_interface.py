class DtoInterface:
    def __init__(self):
        """Constructor of the class DtoInterface

        Raises:
            NotImplementedError: not implemented
        """        
        raise NotImplementedError("Not implemented")
    
    def toJson(self):
        """Convert the dto to a json

        Raises:
            NotImplementedError: not implemented
        """        
        raise NotImplementedError("Not implemented")
        
    def __fromJson(self, json):
        """Convert a json to a dto

        Args:
            json (dict): json to convert

        Raises:
            NotImplementedError: not implemented
        """        
        raise NotImplementedError("Not implemented")
        
    def toDao(self):
        """Convert the dto to a dao

        Raises:
            NotImplementedError: not implemented
        """        
        raise NotImplementedError("Not implemented")
        
    def __fromDao(self, dao):  
        """Convert a dao to a dto

        Args:
            dao (dao): dao (database object) to convert

        Raises:
            NotImplementedError: not implemented
        """        
        raise NotImplementedError("Not implemented")
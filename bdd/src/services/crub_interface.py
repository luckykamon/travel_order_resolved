class CRUBInterface:    
    def getJsonMany():
        """get all json of database objetcs

        Raises:
            NotImplementedError: not implemented

        Returns:
            dict: json of all database objects
        """            
        raise NotImplementedError
    
    def getJsonOneById(id):
        """get one json of database object from id

        Args:
            id (str): id of the database object

        Raises:
            NotImplementedError: not implemented

        Returns:
            dict: json of one database object from id
        """               
    
    def __getJsonFromObject(object):
        """get json from object

        Args:
            object (object): database object
            
        Raises:
            NotImplementedError: not implemented

        Returns:
            dict: json of the database object
        """
        raise NotImplementedError
    
    def __getMany():
        """get all database objetcs
        
        Raises:
            NotImplementedError: not implemented

        Returns:
            object: all database objects
        """        
        raise NotImplementedError
    
    def __getOneById(id):
        """get one database object from id

        Args:
            id (str): id of the database object
            
        Raises:
            NotImplementedError: not implemented

        Returns:
            object: one database object from id
        """
        raise NotImplementedError
    
    def __ckeckFields(id=None):
        """check if all fields correspond to the database object

        Args:
            id (str): id of the database object

        Raises:
            NotImplementedError: not implemented
            TypeError: if a field is not correct
        """
        raise NotImplementedError
    
    def createOne():
        """create one database object
        
        Raises:
            NotImplementedError: not implemented

        Returns:
            dict: json of the created database object
        """
        pass
    
    def updateOne(id):
        """update one database object from id

        Args:
            id (str): id of the database object
            
        Raises:
            NotImplementedError: not implemented

        Returns:
            dict: json of the updated database object
        """
        raise NotImplementedError
    
    def deleteOne(id):
        """delete one database object from id

        Args:
            id (str): id of the database object
            
        Raises:
            NotImplementedError: not implemented

        Returns:
            str: message for validate the deletion
        """
        raise NotImplementedError
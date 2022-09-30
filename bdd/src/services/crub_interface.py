class CRUBInterface:   
    # GET
    def __getJsonFromDao(dao):
        """get json from dao

        Args:
            dao (dao): database object
            
        Raises:
            NotImplementedError: not implemented

        Returns:
            dict: json of the database object
        """
        raise NotImplementedError("Not implemented")
    
    def __getMany():
        """get all database objetcs
        
        Raises:
            NotImplementedError: not implemented

        Returns:
            object: all database objects
        """        
        raise NotImplementedError("Not implemented")
    
    def getJsonMany():
        """get all json of database objetcs

        Raises:
            NotImplementedError: not implemented

        Returns:
            dict: json of all database objects
        """            
        raise NotImplementedError("Not implemented")
    
    def __getOneById(id:str):
        """get one database object from id

        Args:
            id (str): id of the database object
            
        Raises:
            NotImplementedError: not implemented

        Returns:
            object: one database object from id
        """
        raise NotImplementedError("Not implemented")
    
    def getJsonOneById(id:str):
        """get one json of database object from id

        Args:
            id (str): id of the database object

        Raises:
            NotImplementedError: not implemented

        Returns:
            dict: json of one database object from id
        """  
        raise NotImplementedError("Not implemented") 
    
    # CHECK
    def __ckeckFields(dto):
        """check if all fields correspond to the database object

        Args:
            dto (dto): dto of the database object

        Raises:
            NotImplementedError: not implemented
            TypeError: if a field is not correct
        """
        raise NotImplementedError("Not implemented")

    # CREATE
    def createOne(json:dict):   
        """create one database object
        
        Args:
            json (dict): json of the database object
        
        Raises:
            NotImplementedError: not implemented

        Returns:
            dict: json of the created database object
        """
        raise
    
    # UPDATE
    def updateOne(id:str, json:dict):
        """update one database object from id

        Args:
            id (str): id of the database object
            json (dict): json of the database object
            
        Raises:
            NotImplementedError: not implemented

        Returns:
            dict: json of the updated database object
        """
        raise NotImplementedError("Not implemented")
    
    # DELETE
    def deleteOne(id:str):
        """delete one database object from id

        Args:
            id (str): id of the database object
            
        Raises:
            NotImplementedError: not implemented

        Returns:
            str: message for validate the deletion
        """
        raise NotImplementedError("Not implemented")
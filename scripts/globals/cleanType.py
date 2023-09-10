def cleanType(t:type):
    """
    This can be used in the Python CLI (or IDLE) to get the type of an object.
    
    Arguments:
    * type `t` - The object's type.
    
    Returns:
    
    A string representing the object's type.

    Example:

    ```py
    >>> v = "Did you know you have rights?"
    >>> print(cleantype(v))
    str
    >>> 
    ```
    """
    tString = str(t)
    return tString.removeprefix("<class '").removesuffix("'>")
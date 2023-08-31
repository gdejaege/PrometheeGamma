
class Lock:
    """
    A very simple lock to synchronize objects

    Attributes
    ----------
    locked : bool
        True if the lock is closed, False otherwise
    """

    def __init__(self) -> None:
        self.locked = False


    def lock(self,a=None,b=None,c=None):
        """Close the lock
        """
        self.locked = True

    
    def unlock(self):
        """Open the lock
        """
        self.locked = False


    def isLocked(self):
        """Test if lock is opened or closed

        Returns
        -------
        True if the lock is closed, False otherwise
        """
        return self.locked

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


    def lock(self,a=None,b=None,c=None) -> None:
        """Close the lock
        """
        self.locked = True

    
    def unlock(self) -> None:
        """Open the lock
        """
        self.locked = False


    def isLocked(self) -> bool:
        """Test if lock is opened or closed

        Returns
        -------
        bool
            True if the lock is closed, False otherwise
        """
        return self.locked
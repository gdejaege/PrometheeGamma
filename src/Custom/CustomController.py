from Custom.CustomView import CustomView
from Custom.CustomModel import CustomModel

class CustomController:

    class Listener:
        def apply(self, results):
            pass
        def reset(self):
            pass


    def __init__(self, master) -> None:
        self.master = master

        # Initialize all variable that you need
        self.customView = None
        self.customModel = None


    def setListener(self, l:Listener):
        """Set the listener

        Parameters
        ----------
        l : Listener
            the new listener
        """
        self.listener = l


    def run(self):
        # TODO You can write core here to start module

        ##### Example: launch a view
        self.customView = CustomView(self.master)
        self.customView.setListener(self)
        self.customView.show()
        #####

        ##### Example: launch a model
        self.customModel = CustomModel()
        self.customModel.run()
        #####


    def apply(self, results):
        """Apply results

        Parameters
        ----------
        results : you can choose the format
            this must give the values of parameters I, J and P of PROMETHEE Gamma method
        """

        # TODO You can write code here to format results correctly
        # results must be in the form : (I,J,P) where I, J and P are the values of the 3 parameters of PROMETHEE Gamma method, in float

        # Call the parent controller to apply the results
        self.listener.apply(results)


    def reset(self):
        """Reset the tab and quit Custom module
        """
        # Destroy all children of the master frame to clear the view
        for w in self.master.winfo_children():
            w.destroy()

        # Call the parent controller to restart the helpForParameters tab
        self.listener.reset()
from Views.AppView import AppView

class AppController:
    def __init__(self) -> None:
        self.appView = AppView()

    def run(self) -> None:
        """
        Launch the app
        """
        self.appView.show()
        self.appView.mainloop()

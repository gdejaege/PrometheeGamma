"""
Main script of PROMETHEE Gamma GUI app

This script launch the app
"""

from promethee_gamma_gui.Controllers.AppController import AppController

if __name__ == '__main__':
    app = AppController()
    app.run()
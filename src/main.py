"""
Main script of PROMETHEE Gamma GUI app

This script launch the app
"""

from Controllers.AppController import AppController

if __name__ == '__main__':
    app = AppController()
    app.run()
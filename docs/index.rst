.. src documentation master file, created by
   sphinx-quickstart on Sun Feb 14 11:35:05 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to bt_button's documentation!
=====================================

Installation
------------

.. code-block::

   $ wget https://github.com/akihiro-yoshii/bt_button/releases/download/v0.1.3/bt_button-0.1-py3-none-any.whl
   $ pip install bt_button-0.1-py3-none-any.whl

How to use
----------

You can get button instance and register callback function as below.

.. code-block:: python

   import bt_button

   button = bt_button.AbShutter()
   button.add_released_listener(released)
   button.start()

   def released(event):
       print(event)
       print("Released!")

And you can get below result.

.. code-block::

   event at 1613224432.342770, code 115, type 01, val 00
   Released!


Sample Implementation
---------------------

https://github.com/akihiro-yoshii/bt_button_app/blob/main/main.py

.. toctree::
   :maxdepth: 4
   :caption: API References:

   bt_button


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

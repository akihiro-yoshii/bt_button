.. src documentation master file, created by
   sphinx-quickstart on Sun Feb 14 11:35:05 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
   :hidden:

   self
   device_setup
   bt_button

Overview
========

This package supports to get event of bluetooth device for your application.


Installation
------------

.. code-block::

   $ wget https://github.com/akihiro-yoshii/bt_button/releases/download/v0.2.0/bt_button-0.2-py3-none-any.whl
   # apt install libglib2.0-dev
   $ pip install bt_button-0.2-py3-none-any.whl


How to use
----------

You can get button instance and register callback function as below.

.. code-block:: python

   import bt_button

   button = bt_button.AbShutter([MAC ADDRESS])
   button.add_released_listener(released)
   button.connect()

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

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

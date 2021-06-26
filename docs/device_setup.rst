Device Setup
============

AB Shutter
----------

Before change device permission, pair AB Shutter to computer.

.. code-block::

   $ cat /etc/udev/rules.d/80-btbutton.rules
   KERNEL=="event*", ATTRS{name}=="AB Shutter3", MODE="0666"
   $ sudo service udev restart


BT Selfie E
-----------

Before change device permission, pair BT Selfie to computer.

.. code-block::

   $ cat /etc/udev/rules.d/80-btbutton.rules
   KERNEL=="event*", ATTRS{name}=="BTselfie E Keyboard", MODE="0666"
   $ sudo service udev restart


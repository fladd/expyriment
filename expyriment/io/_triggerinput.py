"""
A Trigger input

This module contains a class implementing a trigger input.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import defaults
import expyriment
from expyriment.misc import Clock, compare_codes
from _keyboard import Keyboard
from  _input_output import Input


class TriggerInput(Input):
    """A class implementing a trigger input."""

    def __init__(self, interface, default_code=None):
        """Create a trigger input.

        Parameters
        interface    -- the interface to use (expyrment.io.SerialPort or
                        expyriment.io.ParallelPort object)
        default_code -- the default code of the trigger (int) (optional)

        """

        Input.__init__(self)
        self._interface = interface
        if default_code is not None:
            self._default_code = default_code
        else:
            self._default_code = defaults.triggerinput_default_code

    @property
    def interface(self):
        """Getter for interface"""
        return self._interface

    @property
    def default_code(self):
        """Getter for default_code"""
        return self._default_code

    @default_code.setter
    def default_code(self, value):
        """Getter for default_code"""
        self._default_code = value

    def wait(self, code=None, bitwise_comparison=False):
        """Wait for a trigger.

        Returns the code received and the reaction time [code, rt].

        If bitwise_comparison = True, the function performs a bitwise
        comparison (logical and) between code and received input and waits
        until a certain bit pattern is set.

        Parameters
        code -- a specific code to wait for (int) (optional)
        bitwise_comparison -- make a bitwise comparison (default=False)

        """

        start = Clock._cpu_time()
        found = None
        rt = None
        if code is None:
            code = self._default_code
        self.interface.clear()
        while True:
            expyriment._active_exp._execute_wait_callback()
            read = self.interface.poll()
            if read is not None:
                if code is None: #return for every event
                    rt = int((Clock._cpu_time() - start) * 1000)
                    found = read
                    break
                elif compare_codes(read, code, bitwise_comparison):
                    rt = int((Clock._cpu_time() - start) * 1000)
                    found = read
                    break
            if Keyboard.process_control_keys():
                    break
        if self._logging:
            expyriment._active_exp._event_file_log(
                            "TriggerInput,received,{0},wait".format(found))
        return found, rt

    def get_triggers(self, code=None, bitwise_comparison=False):
        """Get list of received triggers.

        For not missing any triggers the history has to be updated regularly
        (e.g. by calling this method)!
        Returns None if no history is used.

        If bitwise_comparision = True, the function performs a bitwise
        comparison (logical and) between code and received input and waits
        until a certain bit pattern is set.

        Parameters
        code -- a specific code to get (int) (optional)
        bitwise_comparison -- make a bitwise comparison (default=False)

        """

        if self.interface.has_input_history:
            self.interface.clear()
            counter_list = []
            if code is None:
                code = self._default_code
            for event in self.interface.input_history.get_whole_buffer():
                if code is None: #get them all
                    counter_list.append(event)
                elif compare_codes(event, code, bitwise_comparison):
                    counter_list.append(event)
            return counter_list
        else:
            return None

    @property
    def trigger_count(self, code=None, bitwise_comparison=False):
        """Get the number of received triggers.

        For not missing any triggers the history has to be updated regularly
        (e.g. by calling this method)!
        Returns None if no history is used.

        If bitwise_comparision = True, the function performs a bitwise
        comparison (logical and) between code and received input and waits
        until a certain bit pattern is set.

        Parameters
        code -- a specific code to count (int) (optional)
        bitwise_comparison -- make a bitwise comparison (default=False)

        """

        if self.interface.has_input_history:
            self.interface.clear()
            counter = 0
            if code is None:
                code = self._default_code
            for event in self.interface.input_history.get_whole_buffer():
                if code is None: #count all
                    counter += 1
                elif compare_codes(event, code, bitwise_comparison):
                    counter += 1
            return counter
        else:
            return None

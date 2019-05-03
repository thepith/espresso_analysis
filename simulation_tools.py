"""Tools to have an easier management of simulations"""
import datetime
import sys
from espressomd import version


class data_collector:
    """collect data

    initialize with
    ```
    data = data_collector(<function>, <input_parameter>)
    ```

    This will register the function and the input parameters. When you run
    ```
    data.collect()
    ```
    then for all input parameters function will be called, and the output will be stored
    """
    def __init__(self, function, input_parameters):
        self._function = function
        self._input = input_parameters
        self._data = {}
        for i in self._input:
            self._data[i] = []

    def collect(self):
        """collect data"""
        for i in self._input:
            self._data[i].append(self._function(i))

    def __getitem__(self, key):
        if key in self._data:
            return self._data[key]
        raise KeyError

    def data(self):
        """return data"""
        return self._data


class timing:
    """Time a process"""
    def __init__(self, number_of_steps, start=0):
        self._number_of_steps = number_of_steps
        self._starttime = datetime.datetime.now()
        print("Starting Step {:d}. Number of steps: {:d}".format(start, number_of_steps))
        print("Current Time: {}".format(str(self._starttime)))
        print("")
        sys.stdout.flush()

    def report(self, step):
        """return the current time estimate"""
        currenttime = datetime.datetime.now()
        print("Finished Step {:d}. Number of steps: {:d}".format(step, self._number_of_steps))
        print("Current Time: {}".format(str(currenttime)))
        deltatime = currenttime - self._starttime
        totaltime = (float(self._number_of_steps)/float(step + 1))*deltatime
        print("elapsed time             : {}".format(str(deltatime)))
        print("estimated remaining time : {}".format(str(totaltime - deltatime)))
        print("estimated end time       : {}".format(str(totaltime + self._starttime)))
        print("")
        sys.stdout.flush()


def espressomd_version():
    """ return a string containing the espresso version """
    return "espresso version {}; commit: {}; git state: {}".format(
        version.friendly(), version.git_commit().decode('UTF-8'), version.git_state().decode('UTF-8')
    )


class Transcript():
    """Transcript - direct print output to a file, in addition to terminal.

Usage:
    import Transcript
    Transcript.start('logfile.log')
    print("inside file")
    Transcript.stop()
    print("outside file")
"""

    def __init__(self, filename):
        self.terminal = sys.stdout
        self.logfile = open(filename, "a")

    def write(self, message):
        """write a message"""
        self.terminal.write(message)
        self.logfile.write(message)

    def flush(self):
        """flush the file"""
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.

    def start(self, filename):
        """Start transcript, appending print output to given filename"""
        sys.stdout = Transcript(filename)

    def stop(self):
        """Stop transcript and return print functionality to normal"""
        sys.stdout.logfile.close()
        sys.stdout = sys.stdout.terminal

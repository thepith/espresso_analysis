"""Tools to have an easier management of simulations"""


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
        for i in self._input:
            self._data[i].append(self._function(i))

    def __getitem__(self, key):
        if key in self._data:
            return self._data[key]
        raise KeyError

    def data(self):
        return self._data


class timing:
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
    def __init__(self, number_of_steps, start=0):
        import datetime
        import sys
        self._number_of_steps = number_of_steps
        self._starttime = datetime.datetime.now()
        print("Starting Step {:d}. Number of steps: {:d}".format(start, number_of_steps))
        print("Current Time: {}".format(str(self._starttime)))
        print("")
        sys.stdout.flush()

    def report(self, step):
        import datetime
        import sys
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
    from espressomd import version
    return "espresso version {}; commit: {}; git state: {}".format(
        version.friendly(), version.git_commit(), version.git_state()
    )

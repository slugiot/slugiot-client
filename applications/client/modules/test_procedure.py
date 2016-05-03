# This is a test procedure file. It interacts with slugIOT through procedureapi
import procedureapi
api = procedureapi.ProcedureApi("test_procedure")

def run():
    # Add schedules
    api.add_schedule("method1", repeats=1, period_between_runs=10, function_args=[23, 34, 'testarg'])
    api.add_schedule("method2", repeats=1, period_between_runs=10)

def method1(arg1, arg2, arg3):
    api.write_log("In method1!!", log_level=api.LogLevel.DEBUG)
    api.write_log(arg1, log_level=api.LogLevel.DEBUG)
    api.write_log(arg2, log_level=api.LogLevel.DEBUG)
    api.write_log(arg3, log_level=api.LogLevel.DEBUG)
    return "Just executed method1"

def method2():
    api.write_log("In method2", api.LogLevel.DEBUG)
    api.write_value({"test_val": 50})
    test_val = api.read_value("test_val")
    if (test_val > 0):
        api.write_output(name="test_val", data=test_val)
        api.write_outputs({"test_val":test_val, "test_val2" : 51})

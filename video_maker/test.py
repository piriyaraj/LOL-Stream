from usecases.get_run_command import get_commands

try:
    get_commands("wenbo")
except Exception as e:
    print("Error: %s" % e)
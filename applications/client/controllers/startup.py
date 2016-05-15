def start():
    """Here we are acting as though the synchronizations have never yet been run.  An
    improvement would be to first check if run previously and avoid the extra steps
    of removing and adding back schedules again.
    This function is called by the slugiot_startup.sh script which runs at device starup.
    """
    api = procedureapi.ProcedureApi("do_synchronization")
    api.remove_schedule()
    api.add_schedule()

    api = procedureapi.ProcedureApi("do_procedure_sync")
    api.remove_schedule()
    api.add_schedule()
from _util import get_cost_metrics, readF, writeF


if __name__ == "__main__":

    import sys, os
    _sv = sys.argv[1]
    _sv_info = _sv + "_info.txt"
    _sv_metrics = _sv + "_metrics.txt"
    _info = readF('tmp_cost', _sv_info)
    _metrics = readF('tmp_cost', _sv_metrics)
    _ans, _steps = get_cost_metrics(_info, _metrics)
    print(f"> steps: '{_steps}'")
    print(f"> ans: '{_ans}'")
    _out = _sv + "_ans.txt"
    _out_steps = _sv + "_steps.txt"
    writeF('tmp_cost', _out, "\n".join(_ans))
    writeF('tmp_cost', _out_steps, _steps)

# python get-cost_metrics.py "cassandraclusters0"
# python get-cost_metrics.py "cassandraclusters1"
# python get-cost_metrics.py "databaseaccounts0"
# python get-cost_metrics.py "databaseaccounts1"
# python get-cost_metrics.py "mongoclusters"

# python get-cost_metrics.py "apimanagement"
# python get-cost_metrics.py "eventhubclusters"
# python get-cost_metrics.py "eventhubnamespace"

# python get-cost_metrics.py "synapse bigdatapools"
# python get-cost_metrics.py "synapse kustopools"
# python get-cost_metrics.py "synapse scopepools"
# python get-cost_metrics.py "synapse sqlpools"
# python get-cost_metrics.py "synapse workspace"

# python get-cost_metrics.py "DBforMySQL-flexibleServers0"
# python get-cost_metrics.py "DBforMySQL-flexibleServers1"
# python get-cost_metrics.py "DBforMySQL-servers"
# python get-cost_metrics.py "app-containerapps"
# python get-cost_metrics.py "disks"
# python get-cost_metrics.py "sql-databases0"
# python get-cost_metrics.py "sql-databases1"
# python get-cost_metrics.py "sql-elasticpools"
# python get-cost_metrics.py "sql-managedInstances"
# python get-cost_metrics.py "storageAccounts"
# python get-cost_metrics.py "storageAccounts-blobServices"
# python get-cost_metrics.py "storageAccounts-fileServices"
# python get-cost_metrics.py "virtualMachineScaleSets-vm0"
# python get-cost_metrics.py "virtualMachineScaleSets-vm1"
# python get-cost_metrics.py "virtualMachines0"
# python get-cost_metrics.py "virtualMachines1"
# python get-cost_metrics.py "virtualmachineScaleSets0"
# python get-cost_metrics.py "virtualmachineScaleSets1"


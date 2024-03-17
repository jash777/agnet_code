import psutil as ps
import datetime 
import json

# def get_process_data():
#     process_table = []
#     p = ps.pids()
#     processes = {
#     'pids' : '',
#     'name' : '',
#     'started' : '',
#     'status' : '',
#     'username':'',
#     "ports": '',
#     'ip':''
#     }
#     for process in p:
#         connections = ps.Process(process).connections(kind='inet')
#         ip_addresses = [conn.laddr.ip for conn in connections]
#         processes = {
#         'pids' : process,
#         'name' : ps.Process(process).name(),
#         'started' : datetime.utcfromtimestamp(ps.Process(process).create_time()).strftime('%Y-%m-%dT%H:%M:%SZ'),
#         'status' : ps.Process(process).status(),
#         'username' : ps.Process(process).username(),
#         'ports': [conn.laddr.port for conn in ps.Process(process).connections(kind='inet')],
#         'ip_addresses': ip_addresses 


#         }
#         process_table.append(processes)
#     json_data = json.dumps(process_table)
#     return json_data


def get_process_data():
    process_table = []
    p = ps.pids()

    for process in p:
        connections = ps.Process(process).connections(kind='inet')
        ip_addresses = [conn.laddr.ip for conn in connections]

        process_info = {  # Create a new dictionary for each process
            'pid': process,  # Changed 'pids' to 'pid'
            'name': ps.Process(process).name(),
            'started': datetime.utcfromtimestamp(ps.Process(process).create_time()).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'status': ps.Process(process).status(),
            'username': ps.Process(process).username(),
            'ports': [conn.laddr.port for conn in ps.Process(process).connections(kind='inet')],
            'ip_addresses': ip_addresses
        }

        process_table.append(process_info)  # Append the process_info 

    json_data = json.dumps(process_table)
    return json_data

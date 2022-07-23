from subprocess import Popen, PIPE
from datetime import datetime


def getting_the_output_of_the_ps_command():
    main_process = Popen(["ps", "aux"], stdout=PIPE, stderr=PIPE)
    return main_process.communicate()[0]


def dump_output_to_file():
    output = getting_the_output_of_the_ps_command()
    with open("data.txt", "w") as f:
        f.write(output.decode())


def open_file():
    with open("data.txt") as f:
        data = f.readlines()[1:]
    return data


def system_users():
    data = open_file()
    temp_list_users = []
    users_list = []
    for line in data:
        if line.split()[:1] not in temp_list_users:
            temp_list_users.append(line.split()[:1])
    for user in temp_list_users:
        users_list.extend(user)
    return users_list


def processes_running():
    data = open_file()
    process_len = []
    for proc_l in data:
        process_len.append(proc_l)
    return process_len


def user_processes():
    data = open_file()
    temp_proc_user = []
    processes_users_list = []
    users_list = system_users()
    processes_users = []
    for proc_us in data:
        temp_proc_user.append(proc_us.split()[:1])
    for proc_us in temp_proc_user:
        processes_users_list.extend(proc_us)
    for user in users_list:
        processes_users.append(f"Пользователем '{user.title()}'"
                               f" запущенно процессов: {processes_users_list.count(user)}")
    return processes_users


def total_memory_used():
    data = open_file()
    temp_num = []
    num_list = []
    memory_total = 0
    for line in data:
        temp_num.append(line.split()[5:6])
    for num in temp_num:
        num_list.extend(num)
    int_nums = [int(x) for x in num_list]
    for int_num in int_nums:
        memory_total += int_num
    return memory_total


def total_cpu_used():
    data = open_file()
    temp_cpu = []
    cpu_list = []
    cpu_total = 0
    for line in data:
        temp_cpu.append(line.split()[2:3])
    for cpu in temp_cpu:
        cpu_list.extend(cpu)
    float_cpu = [float(x) for x in cpu_list]
    for cpu in float_cpu:
        cpu_total += cpu
    return cpu_total


def uses_the_most_memory():
    data = open_file()
    temp_dict_command_and_memory = []
    max_usage_value_memory = [0.0]
    uses_memory = []
    for line in data:
        temp_dict_command_and_memory.append({'Command': line.split()[10:11], 'Memory': line.split()[3:4]})
    for command_Memory in temp_dict_command_and_memory:
        memory_value = [float(x) for x in command_Memory["Memory"]]
        if memory_value >= max_usage_value_memory:
            max_usage_value_memory = memory_value
    for command_Memory in temp_dict_command_and_memory:
        memory_value = [float(x) for x in command_Memory["Memory"]]
        if memory_value >= max_usage_value_memory:
            uses_memory.append(command_Memory)
    return uses_memory


def most_cpu_used():
    data = open_file()
    temp_dict_command_and_cpu = []
    max_usage_value_cpu = [0.0]
    uses_the_most_cpu = []
    for line in data:
        temp_dict_command_and_cpu.append({'Command': line.split()[10:11], 'CPU': line.split()[2:3]})
    for command_cpu in temp_dict_command_and_cpu:
        cpu_value = [float(x) for x in command_cpu["CPU"]]
        if cpu_value >= max_usage_value_cpu:
            max_usage_value_cpu = cpu_value
    for command_cpu in temp_dict_command_and_cpu:
        cpu_value = [float(x) for x in command_cpu["CPU"]]
        if cpu_value >= max_usage_value_cpu:
            uses_the_most_cpu.append(command_cpu)
    return uses_the_most_cpu


def output_system_users():
    return f"Пользователи системы: {', '.join(system_users())}"


def output_processes_running():
    return f"Процессов запущено: {len(processes_running())}"


def output_total_memory_used():
    return f"Всего памяти используется: {round(total_memory_used() * 10 ** -6, 1)} Mb"


def output_total_cpu_used():
    return f"Всего CPU используется: {round(total_cpu_used(), 1)}%"


if __name__ == '__main__':
    dump_output_to_file()
    print(output_system_users())
    print(output_processes_running())
    print("Пользовательских процессов:")
    print('\n'.join(user_processes()))
    print(output_total_memory_used())
    print(output_total_cpu_used())
    for kv in uses_the_most_memory():
        command = kv['Command'][0]
        print(f"Больше всего памяти использует:\n\tПРОЦЕСС: {command[:20]}\n\t"
              f"% ИСПОЛЬЗУЕМОЙ ПАМЯТИ: {kv['Memory'][0]} %")
    for kv in most_cpu_used():
        command = kv['Command'][0]
        print(f"Больше всего CPU использует:\n\tПРОЦЕСС: {command[:20]}\n\t% ИСПОЛЬЗУЕМОГО CPU: {kv['CPU'][0]} %")
    filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    with open(f"{filename}", "w") as f:
        f.write(f'Отчёт о состоянии системы:\n\n')
        f.write(f'{output_system_users()}\n')
        f.write(f'{output_processes_running()}\n')
        f.write(f'Пользовательских процессов:\n')
        f.writelines('\n'.join(user_processes()))
        f.write(f'\n{output_total_memory_used()}\n')
        f.write(f'{output_total_cpu_used()}\n')
        f.writelines(f'Больше всего памяти использует:\n\tПРОЦЕСС: {kv["Command"][0][:20]}\n\t'
                     f'% ИСПОЛЬЗУЕМОЙ ПАМЯТИ: {kv["Memory"][0]} %\n' for kv in uses_the_most_memory())
        f.writelines(f'Больше всего CPU использует:\n\tПРОЦЕСС: {kv["Command"][0][:20]}\n\t'
                     f'% ИСПОЛЬЗУЕМОГО CPU: {kv["CPU"][0]} %\n' for kv in most_cpu_used())

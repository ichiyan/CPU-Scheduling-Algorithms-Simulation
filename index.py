class Color():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

# The variable ready_queue used throughout the program represents the structure
# wherein processes are put as they enter the system and as they are ready and
# and are waiting to execute. However, despite being named as a queue, it does 
# not necessarily follow the rules of a FIFO queue. 

def fcfs(processes, num_processes):
    processes.sort(key = lambda p: p['arrival_time'])
    processes[0]['waiting_time'] = 0
    time = processes[0]['start_time'] = processes[0]['arrival_time']
    sequence = [{ 'key': processes[0]['key'], 'start_time': time, 'burst_time': processes[0]['burst_time'] }]

    for i in range(1, num_processes):
        time += processes[i - 1]['burst_time']
        # if ready queue is empty ==> processor is idle
        if(processes[i]['arrival_time'] > time):
            idle_time = processes[i]['arrival_time'] - time
            sequence.append({ 'key': '-', 'start_time': time, 'burst_time': idle_time })
            time += idle_time

        processes[i]['waiting_time'] = time - processes[i]['arrival_time']
        sequence.append({ 'key': processes[i]['key'], 'start_time': time, 'burst_time': processes[i]['burst_time'] })

    return processes, sequence


def np_sjf(processes, num_processes):
    if num_processes == 1:
        time = processes[0]['arrival_time']
        sequence = [{ 'key': processes[0]['key'], 'start_time': time, 'burst_time': processes[0]['burst_time'] }]
        processes[0]['waiting_time'] = 0
    else:
        processes.sort(key = lambda p: p['arrival_time'])
        # second_arrival: the first occurence of a process (sorted by arrival time) 
        # in which the arrival time is not the same as the process that arrived first
        # used to determine the processes that arrived first
        second_arrival = next( (pr for pr in processes if pr['arrival_time'] != processes[0]['arrival_time']), -1)
        # sj: the process with the shortest burst time among the processes that arrived first
        sj = min( processes[: processes.index(second_arrival) if second_arrival != -1 else num_processes ], key = lambda pro: pro['burst_time'])
        time = sj['arrival_time']
        sj_ndx = processes.index(sj)
        processes[sj_ndx]['waiting_time'] = 0
        bt = processes[sj_ndx]['burst_time']
        ready_queue = []
        sequence = [{ 'key': sj['key'], 'start_time': time, 'burst_time': sj['burst_time'] }]
        not_arrived = processes.copy()
        not_arrived.pop(sj_ndx)
        completed = 1
    
        while completed < num_processes:
            end = time + bt
            arrived_ctr = 0
            for pna in not_arrived:
                if(pna['arrival_time'] in range(time, end + 1)):
                    ready_queue.append(pna)
                    arrived_ctr += 1
            del not_arrived[:arrived_ctr]
            time = end
            if ready_queue:
                curr_process = min(ready_queue, key = lambda p: p['burst_time'])
                curr_process['waiting_time'] = end - curr_process['arrival_time']
                completed += 1
                ready_queue.remove(curr_process)
                prev = processes.index(curr_process)
                bt = processes[prev]['burst_time']
                sequence.append({ 'key': processes[prev]['key'], 'start_time': time, 'burst_time': processes[prev]['burst_time'] })
            else:
                # processor is idle
                bt = not_arrived[0]['arrival_time'] - end
                sequence.append({ 'key': '-', 'start_time': end, 'burst_time': bt })

    return processes, sequence


def p_sjf(processes, num_processes):
    if num_processes == 1:
        time = processes[0]['arrival_time']
        sequence = [{ 'key': processes[0]['key'], 'start_time': time, 'burst_time': processes[0]['burst_time'] }]
        processes[0]['waiting_time'] = 0
    else:
        processes.sort(key = lambda p: p['arrival_time'])
        ready_queue = []
        not_arrived = []
        # first item used for comparison purposes only
        sequence = [{ 'key': -1 }]
        time = processes[0]['arrival_time']
        # time_executing: total time the process is executed minus its last burst
        # last_burst: duration of last burst
        for pr in processes:
            pr['remaining_time'] = pr['burst_time']
            pr['time_executing']  = 0
            pr['last_burst'] = 0
            if pr['arrival_time'] == time:
                ready_queue.append(pr)
            else:
                not_arrived.append(pr)
        has_not_arrived = True if not_arrived else False

        while not_arrived: 
            pcurr = min( ready_queue, key = lambda job: job['burst_time'] )
            end = time + pcurr['remaining_time']
            newly_arrived_ctr = 0
            for i, pna in enumerate(not_arrived):
                if pna['arrival_time'] in range(time, end + 1):
                    ready_queue.append(pna)
                    newly_arrived_ctr += 1
                    # only adjust time and add to sequence once if there are multiple PNAs with same arrival time
                    if i == 0 or pna['arrival_time'] != not_arrived[i-1]['arrival_time']:
                        elapsed = pna['arrival_time'] - time
                        pcurr['remaining_time'] -= elapsed
                        bt = pcurr['burst_time'] - pcurr['remaining_time']
                        pcurr['time_executing'] += bt
                        if sequence[-1]['key'] != pcurr['key']: 
                            pcurr['last_start_time'] = time
                            pcurr['last_burst'] = bt
                        else:
                            pcurr['last_burst'] += bt
                        sequence.append({ 'key': pcurr['key'], 'start_time': time, 'burst_time': bt, 'p_ndx': processes.index(pcurr) } )
                        time += elapsed
                    # if preempted
                    if( pna['remaining_time'] < pcurr['remaining_time'] ):
                        pcurr = pna
                        end = time + pcurr['remaining_time']
                        bt = pcurr['burst_time'] - pcurr['remaining_time']
                        pcurr['time_executing'] += bt
                        if sequence[-1]['key'] != pcurr['key']:
                            pcurr['last_start_time'] = time
                        sequence.append({ 'key': pcurr['key'], 'start_time': time, 'burst_time': bt, 'p_ndx': processes.index(pcurr) } )
                else:
                    break
            del not_arrived[:newly_arrived_ctr]

            if "last_start_time" in pcurr:
                pcurr['time_executing'] -= pcurr['last_burst']
            else:
                # last process that is executed before all processes have arrived
                pcurr['last_start_time'] = time
                sequence.append({ 'key': pcurr['key'], 'start_time': time, 'burst_time': pcurr['remaining_time'] - time } )

            ready_queue.remove(pcurr)
            time = end

            # processor is idle
            if not ready_queue:
                time = not_arrived[0]['arrival_time']
                next_arrivals = []
                for pna in not_arrived:
                    if pna['arrival_time'] == time:
                        next_arrivals.append(pna)
                    else:
                        break 
                ready_queue.append( min(next_arrivals, key = lambda job: job['burst_time']) )
                not_arrived.pop(0)
                sequence.append({ 'key': '-', 'start_time': end, 'burst_time': time - end } )

        # once all processes have arrived, perform np_sjf to the remaining processes  
        ready_queue.sort(key = lambda job: job['burst_time'])
        sequence.pop(0)
        if has_not_arrived:
            bt = sequence[-1]['burst_time'] =  time - sequence[-1]['start_time']
        for p in ready_queue:
            p['last_start_time'] = start_time = time
            time += p['remaining_time']
            bt = time - start_time
            sequence.append({ 'key': p['key'], 'start_time': start_time, 'burst_time': bt } )

        for p in processes:
            p['waiting_time'] = p['last_start_time'] - p['time_executing'] - p['arrival_time']

    return processes, sequence
   

def rr(processes, num_processes, time_slice):
    processes.sort(key = lambda p: p['arrival_time'])
    for p in processes:
        p['remaining_time'] = p['burst_time']
        p['time_executing'] = 0

    not_arrived = processes[1:].copy()
    ready_queue = [processes[0]]
    time = processes[0]['arrival_time']
    sequence = []
    completed =  0

    while(completed < num_processes):
        if not ready_queue:
            # processor is idle
            ready_queue.append(not_arrived[0])
            not_arrived.pop(0)
            idle_time = ready_queue[0]['arrival_time'] - time
            sequence.append({'key': '-', 'start_time': time, 'burst_time': idle_time })  
            time += idle_time

        sequence.append({'key': ready_queue[0]['key'], 'start_time': time, 'burst_time': ready_queue[0]['remaining_time'] })  
        ready_queue[0]['remaining_time'] -= time_slice
        rt =  ready_queue[0]['remaining_time']
        p = next( pr for pr in processes if pr['key'] == ready_queue[0]['key'])
        if(rt <= 0):
            p['last_start_time'] = time
            completed += 1
            if(rt < 0):
                # time executing is less than time slice
                ready_queue[0]['remaining_time'] = 0
                time += time_slice + rt
                
        if(rt >= 0):
            time += time_slice
        
        popped = ready_queue.pop(0)

        arrived_ctr = 0
        for pna in not_arrived:
            if pna['arrival_time'] <= time:
                ready_queue.append(pna)
                arrived_ctr += 1
        del not_arrived[:arrived_ctr]

        if(rt > 0):
            p['time_executing'] += time_slice  
            ready_queue.append(popped)
    
    for pr in processes:
        pr['waiting_time'] = pr['last_start_time'] - pr['time_executing'] - pr['arrival_time']

    return processes, sequence


def np_ps(processes, num_processes):
    # the lower the number, the higher the priority
    # code is the same as in np_sjf only that 
    # the priority is used in selecting the process
    # to be executed instead of the burst time
    if num_processes == 1:
        time = processes[0]['arrival_time']
        sequence = [{ 'key': processes[0]['key'], 'start_time': time, 'burst_time': processes[0]['burst_time'] }]
        processes[0]['waiting_time'] = 0
    else:
        processes.sort(key = lambda p: p['arrival_time'])
        second_arrival = next( (pr for pr in processes if pr['arrival_time'] != processes[0]['arrival_time']), -1)
        sj = min( processes[: processes.index(second_arrival) if second_arrival != -1 else num_processes ], key = lambda pro: pro['priority'])
        time = sj['arrival_time']
        sj_ndx = processes.index(sj)
        processes[sj_ndx]['waiting_time'] = 0
        bt = processes[sj_ndx]['burst_time']
        ready_queue = []
        sequence = [{ 'key': sj['key'], 'start_time': time, 'burst_time': sj['burst_time'] }]
        not_arrived = processes.copy()
        not_arrived.pop(sj_ndx)
        completed = 1
    
        while completed < num_processes:
            end = time + bt
            arrived_ctr = 0
            for pna in not_arrived:
                if(pna['arrival_time'] in range(time, end + 1)):
                    ready_queue.append(pna)
                    arrived_ctr += 1
            del not_arrived[:arrived_ctr]
            time = end
            if ready_queue:
                curr_process = min(ready_queue, key = lambda p: p['priority'])
                curr_process['waiting_time'] = end - curr_process['arrival_time']
                completed += 1
                ready_queue.remove(curr_process)
                prev = processes.index(curr_process)
                bt = processes[prev]['burst_time']
                sequence.append({ 'key': processes[prev]['key'], 'start_time': time, 'burst_time': processes[prev]['burst_time'] })
            else:
                bt = not_arrived[0]['arrival_time'] - end
                sequence.append({ 'key': '-', 'start_time': end, 'burst_time': bt })

    return processes, sequence


def p_ps(processes, num_processes):
    # the lower the number, the higher the priority
    # code is the same as in p_sjf only that 
    # the priority is used in selecting the process
    # to be executed instead of the burst time

    # current code is plain preemptive priority scheduling;
    # it does not implement priority aging nor a combination
    # of round robin scheduling to prevent starvation 

    if num_processes == 1:
        time = processes[0]['arrival_time']
        sequence = [{ 'key': processes[0]['key'], 'start_time': time, 'burst_time': processes[0]['burst_time'] }]
        processes[0]['waiting_time'] = 0
    else:
        processes.sort(key = lambda p: p['arrival_time'])
        ready_queue = []
        not_arrived = []
        # first item used for comparison purposes only
        sequence = [{ 'key': -1 }]
        time = processes[0]['arrival_time']
        # time_executing: total time the process is executed minus its last burst
        for pr in processes:
            pr['remaining_time'] = pr['burst_time']
            pr['time_executing']  = 0
            pr['last_burst'] = 0
            if pr['arrival_time'] == time:
                ready_queue.append(pr)
            else:
                not_arrived.append(pr)
        has_not_arrived = True if not_arrived else False

        while not_arrived: 
            pcurr = min( ready_queue, key = lambda job: job['priority'] )
            end = time + pcurr['remaining_time']
            newly_arrived_ctr = 0
            for i, pna in enumerate(not_arrived):
                if pna['arrival_time'] in range(time, end + 1):
                    ready_queue.append(pna)
                    newly_arrived_ctr += 1
                    # only adjust time and add to sequence once if there are multiple PNAs with same arrival time
                    if i == 0 or pna['arrival_time'] != not_arrived[i-1]['arrival_time']:
                        elapsed = pna['arrival_time'] - time
                        pcurr['remaining_time'] -= elapsed
                        bt = pcurr['burst_time'] - pcurr['remaining_time']
                        pcurr['time_executing'] += bt
                        if sequence[-1]['key'] != pcurr['key']: 
                            pcurr['last_start_time'] = time
                            pcurr['last_burst'] = bt
                        else:
                            pcurr['last_burst'] += bt
                        sequence.append({ 'key': pcurr['key'], 'start_time': time, 'burst_time': bt, 'p_ndx': processes.index(pcurr) } )
                        time += elapsed
                    # if preempted
                    if( pna['priority'] < pcurr['priority'] ):
                        pcurr = pna
                        end = time + pcurr['remaining_time']
                        bt = pcurr['burst_time'] - pcurr['remaining_time']
                        pcurr['time_executing'] += bt
                        if sequence[-1]['key'] != pcurr['key']:
                            pcurr['last_start_time'] = time
                        sequence.append({ 'key': pcurr['key'], 'start_time': time, 'burst_time': bt, 'p_ndx': processes.index(pcurr) } )
                else:
                    break
            del not_arrived[:newly_arrived_ctr]

            if "last_start_time" in pcurr:
                pcurr['time_executing'] -= pcurr['last_burst']
            else:
                pcurr['last_start_time'] = time
                sequence.append({ 'key': pcurr['key'], 'start_time': time, 'burst_time': pcurr['remaining_time'] - time } )
            ready_queue.remove(pcurr)
            time = end

            if not ready_queue:
                time = not_arrived[0]['arrival_time']
                next_arrivals = []
                for pna in not_arrived:
                    if pna['arrival_time'] == time:
                        next_arrivals.append(pna)
                    else:
                        break 
                ready_queue.append( min(next_arrivals, key = lambda job: job['priority']) )
                not_arrived.pop(0)
                sequence.append({ 'key': '-', 'start_time': end, 'burst_time': time - end } )

        ready_queue.sort(key = lambda job: job['priority'])
        sequence.pop(0)

        if has_not_arrived:
            bt = sequence[-1]['burst_time'] =  time - sequence[-1]['start_time']
        for p in ready_queue:
            p['last_start_time'] = start_time = time
            time += p['remaining_time']
            bt = time - start_time
            sequence.append({ 'key': p['key'], 'start_time': start_time, 'burst_time': bt } )
        for p in processes:
            p['waiting_time'] = p['last_start_time'] - p['time_executing'] - p['arrival_time']

    return processes, sequence


def find_total_waiting_time(processes):
    return(sum( p['waiting_time'] for p in processes ))


def find_avg_waiting_time(total_waiting_time, num_processes):
    return total_waiting_time/num_processes


def print_menu():
    print("\n", 30 * f"{Color.GREEN}-", f"{Color.GREEN}MENU", 30 * f"{Color.GREEN}-")
    print(f""" 
        1. First-Come, First-Served Scheduling 
        2. Nonpreemptive Shortest-Job-First Scheduling
        3. Preemptive Shortest-Job-First Scheduling
        4. Round-Robin Scheduling
        5. Nonpreemptive Priority Scheduling
        6. Preemptive Priority Scheduling 
          (plain PP; aging and round robin not implemented)
        7. Exit
    """)
    print(67 * f"{Color.GREEN}-")


def print_chart(processes, num_processes):
    total_burst = float(sum( p['burst_time'] for p in processes ))
    print("\n", 100 * f"{Color.CYAN}-")
    for ndx, p in enumerate(processes):
        space = int(float(p['burst_time']) / total_burst * 100.0 / 2)
        if(ndx >=1 and p['key'] == processes[ndx-1]['key']): #if current is same as previous
            print(space * f"{Color.WHITE} ", end ="")
        else:
            if(p['burst_time']>9 or p['key']==1):
                print(f"{Color.CYAN}|", f"{Color.WHITE} P{p['key']}", space * f"{Color.WHITE} ", end ="")
            else:
                print(f"{Color.CYAN} |", f"{Color.WHITE} P{p['key']}", space * f"{Color.WHITE} ", end ="")
    print(f"{Color.CYAN}      |")
    print("\n",100 * f"{Color.CYAN}-")
    for i, p in enumerate(processes):
        space = int(float(p['burst_time']) / total_burst * 100.0 / 2)
        if(p['burst_time']>9):
            if(i >=1 and p['key'] == processes[i-1]['key']): #if current is same as previous
                print( space * f"{Color.WHITE} ", end ="")
            else:
                print( f"{Color.CYAN}|", f"{Color.WHITE} {p['start_time']}", space * f"{Color.WHITE} ", end ="")
        else: #has extra space at the end for better alignment
            if(i >=1 and p['key'] == processes[i-1]['key']): #if current is same as previous
                print(space * f"{Color.WHITE} ", end ="")
            else:
                print( f"{Color.CYAN}  |", f"{Color.WHITE} {p['start_time']}", space * f"{Color.WHITE} ", end ="")

    print(f"{Color.WHITE} {processes[num_processes-1]['start_time'] + processes[num_processes-1]['burst_time']}", f"{Color.CYAN}| ")
    print(100 * f"{Color.CYAN}-")


def print_tabular(processes, total_wt, avg_wt):
    processes.sort(key = lambda p: p['arrival_time'])  
    if(processes[0]['priority'] == -1):
        print("\n {:^15} {:^20} {:^20} {:^20}".format(f"{Color.YELLOW} Process", f"{Color.YELLOW} Arrival Time", f"{Color.YELLOW} Burst Time", f"{Color.YELLOW} Waiting Time"))
    else:
        print("\n {:^15} {:^20} {:^20} {:^20} {:^20}".format(f"{Color.YELLOW} Process ID", f"{Color.YELLOW} Arrival Time", f"{Color.YELLOW} Burst Time", f"{Color.YELLOW} Waiting Time", f"{Color.YELLOW} Priority"))
    for p in processes:
            if(p['priority'] == -1):
                print("\n {:^15} {:^20} {:^20} {:^20}".format(f"{Color.WHITE} P{p['key']}", f"{Color.WHITE} {p['arrival_time']}", f"{Color.WHITE} {p['burst_time']}", f"{Color.WHITE} {p['waiting_time']}"))
            else:
                print("\n {:^15} {:^20} {:^20} {:^20} {:^20}".format(f"{Color.WHITE} P{p['key']}", f"{Color.WHITE} {p['arrival_time']}", f"{Color.WHITE} {p['burst_time']}", f"{Color.WHITE} {p['waiting_time']}", f"{Color.WHITE} {p['priority']}"))
    print(f"\n {Color.YELLOW} Total Waiting Time: {Color.WHITE} {total_wt}")
    print(f" {Color.YELLOW} Average Waiting Time: {Color.WHITE} {avg_wt}")

def print_sequence(sequence):
    print("\n {:^15} {:^20} {:^20} ".format(f"{Color.YELLOW} Process ID", f"{Color.YELLOW} Start Time", f"{Color.YELLOW} Duration"))
    for s in sequence:
        print("\n {:^15} {:^20} {:^20}".format(f"{Color.WHITE} {'P' if s['key'] != '-' else ''}{s['key']}", f"{Color.WHITE} {s['start_time']}", f"{Color.WHITE} {s['burst_time']}"))


def make_process_list(burst_times, arrival_times, priority):
    processes = []
    for i, p in enumerate(burst_times):
        if(priority == -1):
            processes.append({'key': i+1, 'arrival_time': arrival_times[i], 'burst_time': p, 'priority':-1})
        else:
            processes.append({'key': i+1, 'arrival_time': arrival_times[i], 'burst_time': p, 'priority':priority[i]})

    return processes

def main():
    loop = True
    while loop:
        print_menu()
        choice = input(f"{Color.WHITE} \nEnter your choice [1-7]: ")
        try:
            choice = int(choice)
            if(choice == 7):
                print(f"{Color.RED} \n TERMINATING PROGRAM... \n {Color.WHITE}")
                loop = False
            elif(choice not in range(1, 8)):
                print(f"{Color.RED} \n Invalid choice. Choice must be from 1-7.")
            else:
                try: 
                    burst_times = [ int(time) for time in input(f"Enter {Color.YELLOW} burst times {Color.WHITE} in milliseconds separated by space (e.g., 24 3 3): ").split()]
                    try:
                        if 0 in burst_times:
                            print(f"{Color.RED} \n Burst time must not be equal to 0.")
                            continue
                        arrival_times = [ int(time) for time in input(f"Enter {Color.YELLOW} arrival times {Color.WHITE} in milliseconds separated by space (e.g, 0 1 2): ").split()]
                        num_processes = len(burst_times)
                        if len(arrival_times) != num_processes:
                            print(f"{Color.RED} \n Number of burst and arrival times must be the same.")
                            continue
                        if(choice > 4): #additional input needed for Priority Scheduling
                            try:
                                priority = [ int(time) for time in input(f"Enter order of {Color.YELLOW} priority {Color.WHITE} (the lower the number, the higher the priority), separated by space (e.g, 0 1 2): ").split()]
                                if len(priority) != num_processes:
                                    print(f"{Color.RED} \n Number of burst times, arrival times, and priority orders must be the same.")
                                    continue
                            except ValueError:
                                print(f"{Color.RED} \n Invalid input. Priority must be a number.")
                            processes = make_process_list(burst_times, arrival_times, priority)
                        else:
                            processes = make_process_list(burst_times, arrival_times, -1)

                        if(choice == 1):
                            p_and_seq = fcfs(processes, num_processes)
                        elif(choice == 2):
                            p_and_seq = np_sjf(processes, num_processes)
                        elif(choice == 3):
                            p_and_seq = p_sjf(processes, num_processes)
                        elif(choice == 4):
                            time_slice = input(f"Enter {Color.YELLOW} time slice {Color.WHITE} in milliseconds: ")
                            try:
                                time_slice = int(time_slice)
                                p_and_seq = rr(processes, num_processes, time_slice)
                            except ValueError:
                                print(f"{Color.RED} \n Invalid input. Time slice or quantum must be a number.")
                        elif(choice == 5):
                            p_and_seq = np_ps(processes, num_processes)
                        elif(choice == 6):
                            p_and_seq = p_ps(processes, num_processes)
                
                        total_wt = find_total_waiting_time(p_and_seq[0])
                        avg_wt = find_avg_waiting_time(total_wt, num_processes)

                        print(f"\n {Color.YELLOW} SEQUENCE: ")
                        print_sequence(p_and_seq[1])
                        print(f"\n {Color.YELLOW} GANTT CHART:")
                        print_chart(p_and_seq[1], len(p_and_seq[1]))
                        print_tabular(p_and_seq[0], total_wt, avg_wt)

                    except ValueError:
                         print(f"{Color.RED} \n Invalid input. Arrival time must be a number.")

                except ValueError:
                    print(f"{Color.RED} \n Invalid input. Burst time must be a number.")

        except ValueError:
            print(f"{Color.RED} \n Invalid input. Choice must be a number from 1-7.")


main()
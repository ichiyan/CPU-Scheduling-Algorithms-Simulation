class Color():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
def print_menu():
    print("\n", 30 * f"{Color.GREEN}-", f"{Color.GREEN}MENU", 30 * f"{Color.GREEN}-")
    print(f""" 
        1. First-Come, First-Served Scheduling 
        2. Nonpreemptive Shortest-Job-First Scheduling
        3. Preemptive Shortest-Job-First Scheduling
        4. Round-Robin Scheduling
        5. Nonpreemptive Priority Scheduling
        6. Preemptive Priority Scheduling 
        7. Exit
    """)
    print(67 * f"{Color.GREEN}-")


def print_chart(processes, num_processes):
    total_burst = float(sum( p['burst_time'] for p in processes ))
    print("\n", 100 * f"{Color.CYAN}-")
    for ndx, p in enumerate(processes):
        space = int(float(p['burst_time']) / total_burst * 100.0 / 2)
        if(p['key'] == processes[ndx-1]['key']): #if current is same as previous
            print(space * f"{Color.WHITE}.", end ="")
        else:
            if(p['burst_time']>9 or p['key']==1):
                print(f"{Color.CYAN}|", f"{Color.WHITE} P{p['key']}", space * f"{Color.WHITE}.", end ="")
            else:
                print(f"{Color.CYAN} |", f"{Color.WHITE} P{p['key']}", space * f"{Color.WHITE}.", end ="")

        #x print(*(["|", "P{data}:{sizeN}".format(data=p['key'], sizeN=4), space * f"{Color.WHITE}."]), end =" ")
        #print(" {:2}{:4}{:space} ".format(f"{Color.CYAN}|", f"{Color.WHITE} P{p['key']}", space * f"{Color.WHITE}."), end =" ")
    print(f"{Color.CYAN}      |")
    print("\n",100 * f"{Color.CYAN}-")
    for i, p in enumerate(processes):
        space = int(float(p['burst_time']) / total_burst * 100.0 / 2)
        if(p['burst_time']>9):
            if(p['key'] == processes[i-1]['key']): #if current is same as previous
                print( space * f"{Color.WHITE}.", end ="")
            else:
                print( f"{Color.CYAN}|", f"{Color.WHITE} {p['start_time']}", space * f"{Color.WHITE}.", end ="")
        else: #has extra space at the end for better alignment
            if(p['key'] == processes[i-1]['key']): #if current is same as previous
                print(space * f"{Color.WHITE}.", end ="")
            else:
                print( f"{Color.CYAN}  |", f"{Color.WHITE} {p['start_time']}", space * f"{Color.WHITE}.", end ="")

    print(f"{Color.WHITE} {processes[num_processes-1]['start_time'] + processes[num_processes-1]['burst_time']}", f"{Color.CYAN}| ")
    print(100 * f"{Color.CYAN}-")
    #print(processes[num_processes-1])

def print_tabular(processes, total_wt, avg_wt):
    processes.sort(key = lambda p: p['arrival_time'])  
    if(processes[0]['priority'] == -1):
        print("\n {:^15} {:^20} {:^20} {:^20}".format(f"{Color.YELLOW} Process", f"{Color.YELLOW} Arrival Time", f"{Color.YELLOW} Burst Time", f"{Color.YELLOW} Waiting Time"))
    else:
        print("\n {:^15} {:^20} {:^20} {:^20} {:^20}".format(f"{Color.YELLOW} Process", f"{Color.YELLOW} Arrival Time", f"{Color.YELLOW} Burst Time", f"{Color.YELLOW} Waiting Time", f"{Color.YELLOW} Priority"))
    for p in processes:
            if(p['priority'] == -1):
                print("\n {:^15} {:^20} {:^20} {:^20}".format(f"{Color.WHITE} P{p['key']}", f"{Color.WHITE} {p['arrival_time']}", f"{Color.WHITE} {p['burst_time']}", f"{Color.WHITE} {p['waiting_time']}"))
            else:
                print("\n {:^15} {:^20} {:^20} {:^20} {:^20}".format(f"{Color.WHITE} P{p['key']}", f"{Color.WHITE} {p['arrival_time']}", f"{Color.WHITE} {p['burst_time']}", f"{Color.WHITE} {p['waiting_time']}", f"{Color.WHITE} {p['priority']}"))
    print(f"\n {Color.YELLOW} Total Waiting Time: {Color.WHITE} {total_wt}")
    print(f" {Color.YELLOW} Average Waiting Time: {Color.WHITE} {avg_wt}")


def make_process_list(burst_times, arrival_times, priority):
    processes = []
    for i, p in enumerate(burst_times):
        if(priority == -1):
            processes.append({'key': i+1, 'arrival_time': arrival_times[i], 'burst_time': p, 'priority':-1})
        else:
            processes.append({'key': i+1, 'arrival_time': arrival_times[i], 'burst_time': p, 'priority':priority[i]})

    return processes


def fcfs(processes, num_processes):
    processes.sort(key = lambda p: p['arrival_time'])
    processes[0]['waiting_time'] = 0
    time = processes[0]['start_time'] = processes[0]['arrival_time']
    sequence = [{ 'key': processes[0]['key'], 'start_time': time, 'burst_time': processes[0]['burst_time'] }]

    for i in range(1, num_processes):
        time += processes[i - 1]['burst_time']
        if(processes[i]['arrival_time'] > time):
            idle_time = processes[i]['arrival_time'] - time
            sequence.append({ 'key': '-', 'start_time': time, 'burst_time': idle_time })
            time += idle_time

        processes[i]['waiting_time'] = time - processes[i]['arrival_time']
        sequence.append({ 'key': processes[i]['key'], 'start_time': time, 'burst_time': processes[i]['burst_time'] })

    return processes, sequence


def np_sjf(processes, num_processes):
    # add condition to skip these if num processes = 1
    processes.sort(key = lambda p: p['arrival_time'])
    second_arrival = next( (pr for pr in processes if pr['arrival_time'] != processes[0]['arrival_time']), -1)
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
        sequence = [{ 'key': -1 }]
        time = processes[0]['arrival_time']
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
            for pna in not_arrived:
                if pna['arrival_time'] in range(time, end + 1):
                    ready_queue.append(pna)
                    newly_arrived_ctr += 1
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
                    print(f"\n T1: {sequence[-1]}")
                    time += elapsed
                    if( pna['remaining_time'] < pcurr['remaining_time'] ):
                        pcurr = pna
                        end = time + pcurr['remaining_time']
                        bt = pcurr['burst_time'] - pcurr['remaining_time']
                        pcurr['time_executing'] += bt
                        if sequence[-1]['key'] != pcurr['key']:
                            pcurr['last_start_time'] = time
                        sequence.append({ 'key': pcurr['key'], 'start_time': time, 'burst_time': bt, 'p_ndx': processes.index(pcurr) } )
                        print(f"\n T2: {sequence[-1]}")
                else:
                    break
            del not_arrived[:newly_arrived_ctr]

            print(f"\n PCURR: {pcurr}")
            if "last_start_time" in pcurr:
                pcurr['time_executing'] -= pcurr['last_burst']
            else:
                pcurr['last_start_time'] = time
            ready_queue.remove(pcurr)
            time = end

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

    print(f"\n SEQUENCE")
    for x in sequence:
        print(x)

    
    print(f"\n PROCESSES")
    for x in processes:
        print(x)

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
    processes.sort(key = lambda p: p['arrival_time'])
    
    time = processes[0]['start_time'] = processes[0]['arrival_time']
    processes[0]['waiting_time'] = 0
    ready_queue = []
    completed = 1
    prev = 0
    while completed < num_processes:
        end = time + processes[prev]['burst_time']
        for p in processes:
            if(p['arrival_time'] in range(time + 1, end + 1)):
                ready_queue.append(p)
        curr_process = min(ready_queue, key = lambda p: p['priority'])
        curr_process['start_time'] = end
        curr_process['waiting_time'] = end - curr_process['arrival_time']
        completed += 1
        ready_queue.remove(curr_process)
        prev = processes.index(curr_process)
        time = end

    processes.sort(key = lambda p: p['waiting_time'])
    return processes, ' '


def p_ps(processes, num_processes):
    processes.sort(key = lambda p: p['arrival_time'])
    for x, p in enumerate(processes):
        p['remaining_time'] = p['burst_time']

    last_arrival = processes[x]['arrival_time']
    ready_queue = [processes[0]]
    curr = 0
    next = 1
    time = processes[0]['arrival_time']
    sequence = []
    time_executed = 0
    ctr=0
    print(last_arrival)

    while time <= last_arrival:
        if (time < last_arrival):
            ready_queue.append(processes[next])
            execute = ready_queue.index(  min(ready_queue, key = lambda p: p['priority']) )
            #time_executed = (processes[next]['arrival_time'] - ready_queue[execute]['arrival_time'])
            #ready_queue[execute]['remaining_time'] -= time_executed
        else: #if last process to enter ready_queue
            ready_queue.append(processes[curr])
            execute = ready_queue.index(  min(ready_queue, key = lambda p: p['priority']) )
            time_executed = ready_queue[execute]['burst_time']
            ready_queue[execute]['remaining_time'] = 0
            
        sequence.append({ 'key': ready_queue[execute]['key'], 'start_time': ready_queue[execute]['arrival_time'],  'burst_time': time_executed})
        ctr += 1
        if(ready_queue[execute]['remaining_time'] == 0):
            ready_queue.remove(ready_queue[execute])
        if (time < last_arrival):
            curr += 1
            next = curr + 1
            time = processes[next]['arrival_time']
        else:
            time += time_executed
    print("ready: ", ready_queue)
    for trav, s in enumerate(sequence):
        if(trav != 0):
            sequence[trav-1]['burst_time'] = s['start_time'] - sequence[trav-1]['start_time']
        for rem in ready_queue:
            if(sequence[trav-1]['key'] == rem['key']):
                rem['remaining_time'] -= sequence[trav-1]['burst_time']
                if(rem['remaining_time'] == 0):
                    ready_queue.remove(rem)


    while(len(ready_queue) > 0):
        execute = ready_queue.index(  min(ready_queue, key = lambda p: p['priority']) )
        time_executed = ready_queue[execute]['remaining_time']
        ready_queue[execute]['remaining_time'] = 0
        sequence.append({ 'key': ready_queue[execute]['key'], 'start_time': ready_queue[execute]['arrival_time'],  'burst_time': time_executed })
        ctr += 1
        #time_executed = (processes[next]['arrival_time'] - ready_queue[execute]['arrival_time'])
        #sequence.append({ 'key': ready_queue[x]['key'], 'start_time': ready_queue[x]['arrival_time'],  'burst_time': time_executed })
        if(ready_queue[execute]['remaining_time'] == 0):
            ready_queue.remove(ready_queue[execute])

    for x, p in enumerate(processes):
        temp = 0
        sub_wait = 0
        for trav, s in enumerate(sequence):
            if(p['key'] == s['key']):
                sub_wait += temp
                temp = s['start_time']+s['burst_time']
        p['waiting_time'] = temp - sub_wait

    print("done: ", ready_queue)
    print("seq", sequence)
    print("pro", processes)

    return processes, sequence

def find_total_waiting_time(processes):
    return(sum( p['waiting_time'] for p in processes ))


def find_avg_waiting_time(total_waiting_time, num_processes):
    return total_waiting_time/num_processes


def main():
    loop = True
    while loop:
        print_menu()
        choice = input(f"{Color.WHITE} \nEnter your choice [1-7]: ")
        try:
            choice = int(choice)
            if(choice == 7):
                print(f"{Color.RED} \n TERMINATING PROGRAM...")
                loop = False
            elif(choice not in range(1, 8)):
                print(f"{Color.RED} \n Invalid choice. Choice must be from 1-7.")
            else:
                try: 
                    # add condition: burst time must not be == 0
                    burst_times = [ int(time) for time in input(f"Enter burst times in milliseconds separated by space (e.g., 24 3 3): ").split()]
                    try:
                        arrival_times = [ int(time) for time in input(f"Enter arrival times in milliseconds separated by space (e.g, 0 1 2): ").split()]
                        num_processes = len(burst_times)
                        if(choice > 4): #additional input needed for Priority Scheduling
                            try:
                                priority = [ int(time) for time in input(f"Enter order of priority, separated by space (e.g, 0 1 2): ").split()]
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
                            time_slice = input("Enter time slice in milliseconds: ")
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

                        # for chart, use p_and_seq[0] for nonpreemptive, p_and_seq[1] for preemptive
                        # if(p_and_seq[1] == ' '):
                        #     print_chart(p_and_seq[0], num_processes)
                        # else:
                        #     num_sequence = len(p_and_seq[1])
                        #     print_chart(p_and_seq[1], num_sequence)

                        print_tabular(p_and_seq[0], total_wt, avg_wt)
                    except ValueError:
                         print(f"{Color.RED} \n Invalid input. Arrival time must be a number.")

                except ValueError:
                    print(f"{Color.RED} \n Invalid input. Burst time must be a number.")

        except ValueError:
            print(f"{Color.RED} \n Invalid input. Choice must be a number from 1-7.")


main()
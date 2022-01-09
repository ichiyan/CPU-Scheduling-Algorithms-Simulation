class Color():
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BLACK = '\033[30m'
    
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
    for i in range(1, num_processes):
        processes[i]['waiting_time'] = processes[i - 1]['burst_time'] + processes[i - 1]['waiting_time'] - (processes[i]['arrival_time'] - processes[i-1]['arrival_time'])
        time += processes[i - 1]['burst_time']
        processes[i]['start_time'] = time

    return processes, ' '


def np_sjf(processes, num_processes):
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
        curr_process = min(ready_queue, key = lambda p: p['burst_time'])
        curr_process['start_time'] = end
        curr_process['waiting_time'] = end - curr_process['arrival_time']
        completed += 1
        ready_queue.remove(curr_process)
        prev = processes.index(curr_process)
        time = end

    processes.sort(key = lambda p: p['waiting_time'])
    return processes, ' '


def p_sjf(processes, num_processes):
    processes.sort(key = lambda p: p['arrival_time'])
    for p in processes:
        p['remaining_time'] = p['burst_time']

    ready_queue = [processes[0]]
    curr = 0
    next = 1
    time = processes[0]['arrival_time']
    sequence = []

    while next < num_processes: 
        ready_queue[curr]['remaining_time'] -= processes[next]['arrival_time'] - time
        rt = ready_queue[curr]['remaining_time']
        sequence.append({ 'key': ready_queue[curr]['key'], 'start_time': time,  'burst_time': ready_queue[curr]['burst_time'] })
        if(rt <= 0):
            if(rt < 0):
                time += rt * -1

            ready_queue[curr]['waiting_time'] = ready_queue[curr]['remaining_time'] = 0
            ready_queue.remove(ready_queue[curr])
        
        if(rt >= 0):
            ready_queue.append(processes[next])
            time = processes[next]['arrival_time']
            next += 1

        curr = ready_queue.index(  min(ready_queue, key = lambda p: p['remaining_time']) )

    ready_queue.sort(key = lambda p: p['remaining_time'])
    for p in ready_queue:
        p['completion_time'] = time + p['remaining_time']
        p['waiting_time'] = p['completion_time'] - p['arrival_time'] - p['burst_time']
        sequence.append({ 'key': p['key'], 'start_time': time,  'burst_time': p['burst_time']})
        time = p['completion_time']

    return processes, sequence

def rr(processes, num_processes, time_slice):
    processes.sort(key = lambda p: p['arrival_time'])
    for p in processes:
        p['remaining_time'] = p['burst_time']
        p['time_executing'] = 0

    not_arrived = processes.copy()
    not_arrived.pop(0)
    ready_queue = [processes[0]]
    time = processes[0]['arrival_time']
    sequence = []
    completed =  0

    while(completed < num_processes):
        init_time = time
        if not ready_queue:
            ready_queue.append(not_arrived[0])
            not_arrived.pop(0)
            NP_time = ready_queue[0]['arrival_time'] - init_time
            sequence.append({'key': '-', 'start_time': init_time, 'burst_time': NP_time })  
            time += NP_time

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
            if pna['arrival_time'] in range (init_time, time + 1):
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
            ready_queue.remove(ready_queue[execute])

        sequence.append({ 'key': ready_queue[execute]['key'], 'start_time': ready_queue[execute]['arrival_time'],  'burst_time': time_executed})
        ctr += 1
        
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
                print(f"{Color.RED} \n TERMINATING PROGRAM")
                loop = False
            elif(choice not in range(1, 8)):
                print(f"{Color.RED} \n Invalid choice. Choice must be from 1-7.")
            else:
                try: 
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
                                print(f"{Color.RED} \n Invalid input. Time quantum must be a number.")
                        elif(choice == 5):
                            p_and_seq = np_ps(processes, num_processes)
                        elif(choice == 6):
                            p_and_seq = p_ps(processes, num_processes)
                
                        total_wt = find_total_waiting_time(p_and_seq[0])
                        avg_wt = find_avg_waiting_time(total_wt, num_processes)

                        # for chart, use p_and_seq[0] for nonpreemptive, p_and_seq[1] for preemptive
                        if(p_and_seq[1] == ' '):
                            print_chart(p_and_seq[0], num_processes)
                        else:
                            num_sequence = len(p_and_seq[1])
                            print_chart(p_and_seq[1], num_sequence)

                        print_tabular(p_and_seq[0], total_wt, avg_wt)
                    except ValueError:
                        print(f"{Color.RED} \n Invalid input. Arrival time must be a number.")

                except ValueError:
                    print(f"{Color.RED} \n Invalid input. Burst time must be a number.")

        except ValueError:
            print(f"{Color.RED} \n Invalid input. Choice must be a number from 1-7.")


main()
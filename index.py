class Color():
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


def print_chart_np(sched_type, processes, num_processes):
    #if(sched_type == 2):
    processes.sort(key = lambda p: p['waiting_time'])
    #remove lang ni when naa na ang sequence[]

    total_burst = float(sum( p['burst_time'] for p in processes ))
    print("\n", 100 * f"{Color.CYAN}-")
    for p in processes:
        space = float(p['burst_time']) / total_burst * 100.0 / 2
        print(f"{Color.CYAN}|", f"{Color.WHITE} P{p['key']}", int(space) * f"{Color.WHITE}.", end =" ")
    print(f"{Color.CYAN}      |")
    print("\n",100 * f"{Color.CYAN}-")
    for p in processes:
        space = float(p['burst_time']) / total_burst * 100.0 / 2
        # if(p['burst_time']>9):
        print( f"{Color.CYAN}|", f"{Color.WHITE} {p['waiting_time']}", int(space) * f"{Color.WHITE}.", end =" ")
        # else:
        #     print( f"{Color.CYAN} | ", f"{Color.WHITE} {p['waiting_time']}", int(space) * f"{Color.WHITE}.", end =" ")
    print(f"{Color.WHITE} {processes[num_processes-1]['waiting_time'] + processes[num_processes-1]['burst_time']}", f"{Color.CYAN}| ")
    print(100 * f"{Color.CYAN}-")


def print_tabular(processes, total_wt, avg_wt):
    processes.sort(key = lambda p: p['key'])  
    print("\n {:<15} {:<20} {:<20} {:<20}".format(f"{Color.YELLOW} Process", f"{Color.YELLOW} Arrival Time", f"{Color.YELLOW} Burst Time", f"{Color.YELLOW} Waiting Time"))
    for p in processes:
            print("\n {:<15} {:<20} {:<20} {:<20}".format(f"{Color.WHITE} P{p['key']}", f"{Color.WHITE} {p['arrival_time']}", f"{Color.WHITE} {p['burst_time']}", f"{Color.WHITE} {p['waiting_time']}"))
    print(f"\n {Color.YELLOW} Total Waiting Time: {Color.WHITE} {total_wt}")
    print(f" {Color.YELLOW} Average Waiting Time: {Color.WHITE} {avg_wt}")


def make_process_list(burst_times, arrival_times):
    processes = []
    for i, p in enumerate(burst_times):
        processes.append({'key': i+1, 'arrival_time': arrival_times[i], 'burst_time': p})

    return processes


def fcfs(processes, num_processes):
    processes.sort(key = lambda p: p['arrival_time'])
    processes[0]['waiting_time'] = 0
    time = processes[0]['start_time'] = processes[0]['arrival_time']
    for i in range(1, num_processes):
        processes[i]['waiting_time'] = processes[i - 1]['burst_time'] + processes[i - 1]['waiting_time'] - (processes[i]['arrival_time'] - processes[i-1]['arrival_time'])
        time += processes[i - 1]['burst_time']
        processes[i]['start_time'] = time

    return processes, ''


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
    return processes, ''


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
        sequence.append({ 'key': ready_queue[curr]['key'], 'start_time': time })
        if(rt <= 0):
            if(rt < 0):
                time += ready_queue[curr]['remaining_time'] * -1

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
        sequence.append({ 'key': p['key'], 'start_time': time })
        time = p['completion_time']

    # how do you want to solve for/display the completion time of the last process? 
    # for now, sequence just contains the key and the start time
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
                        processes = make_process_list(burst_times, arrival_times)
                        if(choice == 1):
                            p_and_seq = fcfs(processes, num_processes)
                        elif(choice == 2):
                            p_and_seq = np_sjf(processes, num_processes)
                        elif(choice == 3):
                            p_and_seq = p_sjf(processes, num_processes)
                
                        total_wt = find_total_waiting_time(p_and_seq[0])
                        avg_wt = find_avg_waiting_time(total_wt, num_processes)

                        # for chart, use p_and_seq[0] for nonpreemptive, p_and_seq[1] for preemptive
                        # options:
                        # option 1: add condition here to determine which to pass 
                        # option 2: pass p_and_seq and add condition in function to use p_and_seq[0] if p_and_seq[1] == ''
                        # print_chart_np(choice, processes, num_processes)
                        print_tabular(p_and_seq[0], total_wt, avg_wt)
                    except ValueError:
                        print(f"{Color.RED} \n Invalid input. Arrival time must be a number.")

                except ValueError:
                    print(f"{Color.RED} \n Invalid input. Burst time must be a number.")

        except ValueError:
            print(f"{Color.RED} \n Invalid input. Choice must be a number from 1-7.")


main()
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
    total_burst = float(sum( p['burst_time'] for p in processes ))
    print("\n", 100 * f"{Color.CYAN}-")
    for p in processes:
        space = float(p['burst_time']) / total_burst * 100.0 / 2
        print(f"{Color.CYAN}|", f"{Color.WHITE} P{p['key']}", int(space) * f"{Color.WHITE}.", end =" ")
    print(f"{Color.CYAN}  |")
    print("\n",100 * f"{Color.CYAN}-")
    for ndx, p in processes:
        space = float(p['burst_time']) / total_burst * 100.0 / 2
        if(p['burst_time']>9):
            print( f"{Color.CYAN}|", f"{Color.WHITE} {p['waiting_time']}", int(space) * f"{Color.WHITE}.", end =" ")
        else:
            print( f"{Color.CYAN}| ", f"{Color.WHITE} {p['waiting_time']}", int(space) * f"{Color.WHITE}.", end =" ")
    print(f"{Color.WHITE} {processes[ndx]['waiting_time'] + processes[ndx]['burst_time']}", f"{Color.CYAN}| ")
    print(100 * f"{Color.CYAN}-")


def print_tabular(processes, total_wt, avg_wt):
    processes.sort(key = lambda p: p['key'])   
    print("\n {:<15} {:<20} {:<20} {:<20}".format(f"{Color.YELLOW} Process", f"{Color.YELLOW} Arrival Time", f"{Color.YELLOW} Burst Time", f"{Color.YELLOW} Waiting Time"))
    for p in processes:
            print("\n {:<15} {:<20} {:<20} {:<20}".format(f"{Color.WHITE} P{p['key']}", f"{Color.WHITE} {p['arrival_time']}", f"{Color.WHITE} {p['burst_time']}", f"{Color.WHITE} {p['waiting_time']}"))
    print(f"\n {Color.YELLOW} Total Waiting Time: {Color.WHITE} {total_wt}")
    print(f" {Color.YELLOW} Average Waiting Time: {Color.WHITE} {avg_wt}")


def fcfs(processes, num_processes):
    processes.sort(key = lambda p: p['arrival_time'])
    processes[0]['waiting_time'] = processes[0]['arrival_time']
    for i in range(1, num_processes):
        processes[i]['waiting_time'] = processes[i - 1]['burst_time'] + processes[i - 1]['waiting_time']
    
    return processes


def np_sjf(processes, num_processes):
    processes.sort(key = lambda p: p['burst_time'])
    #processes.sort(key = lambda p: p['arrival_time'])
    time = processes[0]['waiting_time'] = processes[0]['arrival_time']
    #if the smallest arrival time is not 0, won't it make all the waiting time wrong?
    
    ready_queue = []
    completed = 1
    prev = 0
    while completed < num_processes:
        end = time + processes[prev]['burst_time']
        for p in processes:
            if(p['arrival_time'] in range(time + 1, end + 1)):
                ready_queue.append(p)
        curr_process = min(ready_queue, key = lambda p: p['burst_time'])
        curr_process['waiting_time'] = end - curr_process['arrival_time']
        completed += 1
        ready_queue.remove(curr_process)
        prev = processes.index(curr_process)
        time = end
    # processes.sort(key = lambda p: p['arrival_time'])
    return processes

def make_list(burst_times, arrival_times):
    processes = []
    for i, p in enumerate(burst_times):
        processes.append({'key': i+1, 'arrival_time': arrival_times[i], 'burst_time': p})

    return processes


def findTotalWaitingTime(processes):
    return(sum( p['waiting_time'] for p in processes ))


def findAvgWaitingTime(total_waiting_time, num_processes):
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
                        processes = make_list(burst_times, arrival_times)
                        if(choice == 1):
                            p_with_wt = fcfs(processes, num_processes)
                        elif(choice == 2):
                            p_with_wt = np_sjf(processes, num_processes)

                        total_wt = findTotalWaitingTime(p_with_wt)
                        avg_wt = findAvgWaitingTime(total_wt, num_processes)
                        print_chart_np(choice, processes, num_processes)
                        print_tabular(p_with_wt, total_wt, avg_wt)
                    except ValueError:
                        print(f"{Color.RED} \n Invalid input. Arrival time must be a number.")

                except ValueError:
                    print(f"{Color.RED} \n Invalid input. Burst time must be a number.")

        except ValueError:
            print(f"{Color.RED} \n Invalid input. Choice must be a number from 1-7.")


main()
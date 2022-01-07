
from typing import Sequence


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


def print_tabular(processes, total_wt, avg_wt):
    print("\n {:<15} {:<20} {:<20} {:<20}".format(f"{Color.YELLOW} Process", f"{Color.YELLOW} Arrival Time", f"{Color.YELLOW} Burst Time", f"{Color.YELLOW} Waiting Time"))
    for p in processes:
            print("\n {:<15} {:<20} {:<20} {:<20}".format(f"{Color.WHITE} P{p['key']}", f"{Color.WHITE} {p['arrival_time']}", f"{Color.WHITE} {p['burst_time']}", f"{Color.WHITE} {p['waiting_time']}"))
    print(f"\n {Color.YELLOW} Total Waiting Time: {Color.WHITE} {total_wt}")
    print(f" {Color.YELLOW} Average Waiting Time: {Color.WHITE} {avg_wt}")


def findWaitingTimes(burst_times, arrival_times, num_processes, algo):
    processes = []
    for i, p in enumerate(burst_times):
        processes.append({'key': i+1, 'arrival_time': arrival_times[i], 'burst_time': p})

    if(algo == 1):
        processes.sort(key = lambda p: p['arrival_time'])
    elif(algo == 2):
        processes.sort(key = lambda p: p['burst_time'])

    processes[0]['waiting_time'] = processes[0]['arrival_time']
    if(algo == 1 or algo == 2):
        for i in range(1, num_processes):
            processes[i]['waiting_time'] = processes[i - 1]['burst_time'] + processes[i - 1]['waiting_time']

    processes.sort(key = lambda p: p['key'])   
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
            try: 
                burst_times = [ int(time) for time in input(f"Enter burst times in milliseconds separated by space (e.g., 24 3 3): ").split()]
                try:
                    arrival_times = [ int(time) for time in input(f"Enter arrival times in milliseconds separated by space (e.g, 0 1 2): ").split()]
                    num_processes = len(burst_times)
                    p_with_wt = findWaitingTimes(burst_times, arrival_times, num_processes, choice)
                    total_wt = findTotalWaitingTime(p_with_wt)
                    avg_wt = findAvgWaitingTime(total_wt, num_processes)
                    print_tabular(p_with_wt, total_wt, avg_wt)
                   
                    if(choice == 7):
                        loop = False

                except ValueError:
                    print(f"{Color.RED} \n Invalid input. Arrival time must be a number.")

            except ValueError:
                print(f"{Color.RED} \n Invalid input. Burst time must be a number.")

        except ValueError:
            print(f"{Color.RED} \n Invalid input. Choice must be a number from 1-7.")


main()

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


def print_tabular(bt, at, wt, total_wt, avg_wt, num_processes):
    print("\n {:<15} {:<20} {:<20} {:<20}".format(f"{Color.YELLOW} Process", f"{Color.YELLOW} Arrival Time", f"{Color.YELLOW} Burst Time", f"{Color.YELLOW} Waiting Time"))
    for i in range(num_processes):
            print("\n {:<15} {:<20} {:<20} {:<20}".format(f"{Color.WHITE} P{i+1}", f"{Color.WHITE} {at[i]}", f"{Color.WHITE} {bt[i]}", f"{Color.WHITE} {wt[i][1]}"))
    print(f"\n {Color.YELLOW} Total Waiting Time: {Color.WHITE} {total_wt}")
    print(f" {Color.YELLOW} Average Waiting Time: {Color.WHITE} {avg_wt}")


def findWaitingTimes(burst_times, arrival_times, num_processes):
    processes = [x for x in range(1, num_processes + 1)]
    # merge 3 lists
    # result is in the form [(at, bt, p),(at, bt, p),...]
    paired_times = list(zip(arrival_times, burst_times, processes))
    # sort tuples in ascending order based on arrival time (for FCFS)
    # will do SJF next - gab
    paired_times.sort(key = lambda x: x[0])
    processes = []
    waiting_times = [paired_times[0][0]]
    for i in range(num_processes):
        waiting_times.append(paired_times[i][1] + waiting_times[i]) 
        processes.append(paired_times[i][2])

    # zip function makes it so that if the passed iterators have diff lengths, 
    # the iterator with the least items decides the length of the new iterator
    # In this case, processes[] have the least items so the last item in waiting_times[]
    # which dictates the value of the last tick in the gantt chart gets removed
    # To avoid this, an extra process is appended.
    processes.append(num_processes + 1)
    waiting_times = list(zip(processes, waiting_times))

    # sort waiting_times based on process number
    # in order to be able to display the waiting time for each process in order (see print_tabular function)  
    waiting_times.sort(key = lambda x: x[0])
    
    return waiting_times


def findTotalWaitingTime(waiting_times, num_processes):
    # waiting time is the second item (index 1) in each tuple 
    # and in adding, the last tuple (num_processes) 
    # which is just an extra process is not included  
    return(sum( wt[1] for wt in waiting_times[:num_processes]))


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
                    if(choice == 1):
                        wt = findWaitingTimes(burst_times, arrival_times, num_processes)
                        total_wt = findTotalWaitingTime(wt, num_processes)
                        avg_wt = findAvgWaitingTime(total_wt, num_processes)
                        print_tabular(burst_times, arrival_times, wt, total_wt, avg_wt, num_processes)
                    elif(choice == 7):
                        loop = False

                except ValueError:
                    print(f"{Color.RED} \n Invalid input. Arrival time must be a number.")

            except ValueError:
                print(f"{Color.RED} \n Invalid input. Burst time must be a number.")

        except ValueError:
            print(f"{Color.RED} \n Invalid input. Choice must be a number from 1-7.")


main()
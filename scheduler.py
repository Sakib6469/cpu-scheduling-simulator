# ===============================
# CPU Task Scheduling Simulator
# Preemptive Priority Scheduling
# Author: Sakib
# Description:
# Simulates CPU scheduling using a time-driven approach,
# handling CPU bursts, I/O bursts, and process states.
# ===============================

class Process:
    def __init__(self, name, priority, bursts):
        self.name = name
        self.priority = priority
        self.bursts = bursts[:]

        # Additional attributes
        self.burst_index = 0
        self.remaining_time = bursts[0]
        self.state = "READY"
        self.completion_time = 0
        self.ready_order = 0


def schedule(processes):

    time = 0
    cpu_idle_time = 0

    ready_queue = []
    io_list = []
    completed = []

    current_process = None
    ready_counter = 0

    # Initialize all processes
    for p in processes:
        p.state = "READY"
        p.ready_order = ready_counter
        ready_counter += 1
        ready_queue.append(p)

    # ===============================
    # MAIN SIMULATION LOOP
    # ===============================
    while len(completed) < len(processes):
        time += 1

        # ---------------------------
        #  Update IO processes
        # ---------------------------
        for p in io_list[:]:
            p.remaining_time -= 1

            if p.remaining_time == 0:
                p.burst_index += 1

                if p.burst_index < len(p.bursts):
                    p.remaining_time = p.bursts[p.burst_index]
                    p.state = "READY"
                    p.ready_order = ready_counter
                    ready_counter += 1
                    ready_queue.append(p)

                io_list.remove(p)

        # ---------------------------
        #  Preemption check
        # ---------------------------
        if current_process and ready_queue:
            highest = min(ready_queue, key=lambda x: (x.priority, x.ready_order))

            if highest.priority < current_process.priority:
                current_process.state = "READY"
                current_process.ready_order = ready_counter
                ready_counter += 1
                ready_queue.append(current_process)
                current_process = None

        # ---------------------------
        #  Dispatch process
        # ---------------------------
        if current_process is None and ready_queue:
            ready_queue.sort(key=lambda x: (x.priority, x.ready_order))
            current_process = ready_queue.pop(0)
            current_process.state = "RUNNING"

        # ---------------------------
        #  Execute CPU
        # ---------------------------
        if current_process:
            current_process.remaining_time -= 1
        else:
            cpu_idle_time += 1

        # ---------------------------
        #  Handle completion
        # ---------------------------
        if current_process and current_process.remaining_time == 0:

            current_process.burst_index += 1

            # Move to IO
            if current_process.burst_index < len(current_process.bursts):
                current_process.remaining_time = current_process.bursts[current_process.burst_index]
                current_process.state = "IO"
                io_list.append(current_process)

            # Process complete
            else:
                current_process.state = "DONE"
                current_process.completion_time = time
                completed.append(current_process)

            current_process = None

        # ---------------------------
        # Logging
        # ---------------------------
        print("Time:", time)
        print("CPU:", current_process.name if current_process else "Idle")
        print("Ready Queue:", [p.name for p in ready_queue])
        print("IO:", [p.name for p in io_list])
        print("-------------------------")

    # ===============================
    # FINAL METRICS
    # ===============================
    print("Simulation Complete!")

    total_time = time
    print("Total Time:", total_time)

    print("CPU Idle Time:", cpu_idle_time)

    throughput = len(processes) / total_time
    print("Throughput:", throughput)

    total_turnaround = sum(p.completion_time for p in processes)
    avg_turnaround = total_turnaround / len(processes)

    print("Average Turnaround Time:", avg_turnaround)


# ===============================
# SAMPLE TEST
# ===============================
if __name__ == "__main__":
    processes = [
        Process("P1", 1, [5, 3, 4]),
        Process("P2", 2, [3, 2, 3]),
        Process("P3", 1, [4, 1, 2]),
    ]

    schedule(processes)
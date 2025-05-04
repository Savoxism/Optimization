class Job:
    def __init__(self, job_id, deadline, profit):
        self.job_id = job_id
        self.deadline = deadline
        self.profit = profit
        
def job_sequencing(jobs, max_time):
    jobs.sort(key=lambda x: x.profit, reverse=True)
    
    result = [-1] * max_time
    job_sequence = [None] * max_time
    total_profit = 0
    
    for job in jobs:
        for j in range(min(max_time, job.deadline) - 1, -1, -1): # index starts from 0 
            if result[j] == -1: 
                result[j] = job.job_id
                job_sequence[j] = job
                total_profit += job.profit
                break
            
    final_jobs = [job.job_id for job in job_sequence if job]
    return final_jobs, total_profit
    
# Example usage:
jobs = [
    Job("J1", 2, 100),
    Job("J2", 1, 50),
    Job("J3", 2, 10),
    Job("J4", 1, 20),
    Job("J5", 3, 30)
]

# Assume the maximum time is equal to the maximum deadline among jobs
max_time = max(job.deadline for job in jobs)

selected_jobs, max_profit = job_sequencing(jobs, max_time)
print(f"Selected job sequence: {selected_jobs}")
print(f"Maximum profit: {max_profit}")
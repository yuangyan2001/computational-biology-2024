from pathlib import Path
import re
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np


media_dir='./media/'

result_dir='./test_dir_single_thread/single_thread_result/'

# pattern definition
query_length_pattern=r"\d+"

time_elapsed_pattern=re.compile(r"(\d+\.\d+) seconds time elapsed")
CPU_utilized_pattern=re.compile(r"(\d+\.\d+) CPUs utilized")
frontend_cycles_idle_pattern=re.compile(r"(\d+\.\d+)% frontend cycles idle")
backend_cycles_idle_pattern=re.compile(r"(\d+\.\d+)% backend cycles idle")
L1_dcache_load_misses_pattern=re.compile(r"L1-dcache-load-misses:u\s+.*?(\d+\.\d+)% of all L1-dcache accesses")
page_faults_pattern=re.compile(r"page-faults:u\s+.*?(\d+\.\d+)") # K/sec
page_faults_unit_pattern=re.compile(r"page-faults:u\s+.*?\d+\.\d+\s(.)/sec")


def average(l) :
    return sum(l) / len(l)



# statistic struct
class statistic_info:
    def __init__(self) :
        self.time_elapsed_l=list()
        self.CPU_utilized_l=list()
        self.frontend_cycles_idle_l=list()
        self.backend_cycles_idle_l=list()
        self.L1_dcache_load_misses_l=list()
        self.page_faults_l=list()


def parse_directory(dir, discard=0) :
    directory = Path(dir)
    all_statistics=dict()

    for filepath in directory.rglob('*') :
        if filepath.is_file() :
            querylength=int(re.search(query_length_pattern, filepath.name).group())
            # print(querylength+1)
            

            with open(filepath, 'r') as file:
                if file.read(1) :

                    if all_statistics.get(querylength) is None:
                        all_statistics[querylength] = statistic_info()

                    content=file.read()
                    time_elapsed=time_elapsed_pattern.search(content).group(1)
                    CPU_utilized=CPU_utilized_pattern.search(content).group(1)
                    frontend_cycles_idle=frontend_cycles_idle_pattern.search(content).group(1)
                    backend_cycles_idle=backend_cycles_idle_pattern.search(content).group(1)
                    L1_dcache_load_misses=L1_dcache_load_misses_pattern.search(content).group(1)
                    page_faults=page_faults_pattern.search(content).group(1)
                    page_faults_unit=page_faults_unit_pattern.search(content).group(1)
                    if page_faults_unit != 'K' :
                        print(f"page fault {page_faults}")
                        raise ValueError(f"No No No, the unit is not K, file name {filepath.name}")

                    all_statistics[querylength].time_elapsed_l.append(float(time_elapsed))
                    all_statistics[querylength].CPU_utilized_l.append(float(CPU_utilized))
                    all_statistics[querylength].frontend_cycles_idle_l.append(float(frontend_cycles_idle))
                    all_statistics[querylength].backend_cycles_idle_l.append(float(backend_cycles_idle))
                    all_statistics[querylength].L1_dcache_load_misses_l.append(float(L1_dcache_load_misses))
                    all_statistics[querylength].page_faults_l.append(float(page_faults))

    # sort dict items
    query_length_vec = list()
    time_elapsed_vec = list()
    CPU_utilized_vec = list()
    frontend_cycles_vec = list()
    backend_cycles_vec = list()
    L1_dcache_load_misses_vec = list()
    page_faults_vec = list()
    time_per_query_vec = list()

    for key, stat in all_statistics.items() :
        query_length_vec.append(key)

    query_length_vec.sort()

    for length in query_length_vec :
        stat = all_statistics[length]
        time_elapsed_vec.append(average(stat.time_elapsed_l))
        CPU_utilized_vec.append(average(stat.CPU_utilized_l))
        frontend_cycles_vec.append(average(stat.frontend_cycles_idle_l))
        backend_cycles_vec.append(average(stat.backend_cycles_idle_l))
        L1_dcache_load_misses_vec.append(average(stat.L1_dcache_load_misses_l))
        page_faults_vec.append(average(stat.page_faults_l))
        time_per_query_vec.append(average(stat.time_elapsed_l) / length)

    return query_length_vec, time_elapsed_vec, time_per_query_vec, \
        CPU_utilized_vec, frontend_cycles_vec, backend_cycles_vec, \
        L1_dcache_load_misses_vec, page_faults_vec


def plot_single_thread() :
    query_length_vec, time_elapsed_vec, time_per_query_vec, \
    CPU_utilized_vec, frontend_cycles_vec, backend_cycles_vec, \
    L1_dcache_load_misses_vec, page_faults_vec = \
    parse_directory('./test_dir_single_thread/single_thread_result/')


    # plot total time
    fig, ax = plt.subplots(figsize=(6,5))
    l_time_elapsed = ax.plot(query_length_vec, time_elapsed_vec, \
        marker='.', c='blue', linewidth=1)

    ax.set_ylabel('Time (s)')
    ax.set_xlabel('Query length')
    ax.set_xscale('log', base=2)
    ax.set_yscale('log')
    ax.grid(True)
    # ax.legend()
    fig.savefig(media_dir + 'Single_thread_total_time.pdf')





    # plot single query time and cpu util
    fig, ax = plt.subplots(figsize=(6,5))
    

    l_time_per_query = ax.plot(query_length_vec, time_per_query_vec, \
        marker='.', c='blue', linewidth=1, label='Time per query')

    ax.set_xlabel('Query size')
    ax.set_xscale('log', base=2)
    ax.set_yscale('log')
    ax.set_ylabel('Time per query (s)')
    ax.grid(True)
   
    

    ax1 = ax.twinx()


    l_CPU_util = ax1.plot(query_length_vec, CPU_utilized_vec, \
        marker='x', c='red', linewidth=1, label='CPU utilization')
    ax1.set_ylabel('CPU utilization')
    ax1.set_ylim(0, 1)
    # ax1.legend()


    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax1.get_legend_handles_labels()

    fig.legend(handles1 + handles2, labels1 + labels2)


    fig.savefig(media_dir + 'Single_thread_CPU_and_time_per_query.pdf')




    # plot front and back cycles idle
    fig, ax = plt.subplots(figsize=(6,5))
    l_front_cycles_idle = ax.plot(query_length_vec, frontend_cycles_vec, \
        marker='.', c='blue', linewidth=1, label='idled frontend cycles')

    ax.set_xlabel('Query size')
    ax.set_xscale('log', base=2)
    
    ax.set_ylabel('frontend Percentage(%)')

    ax.grid(True)

    ax1 = ax.twinx()

    

    l_back_cycles_idle = ax1.plot(query_length_vec, backend_cycles_vec, \
        marker='x', c='red', linewidth=1, label='idled backend cycles')

    ax1.set_ylabel('backend Percentage(%)')

    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax1.get_legend_handles_labels()

    fig.legend(handles1 + handles2, labels1 + labels2)
    

    fig.savefig(media_dir + 'single_thread_idled_cycles.pdf')


    # L1 cache miss plot
    fig, ax = plt.subplots(figsize=(6,5))
    l_l1_dcache_miss = ax.plot(query_length_vec, L1_dcache_load_misses_vec, \
        marker='.', c='blue', linewidth=1, label='L1 cache miss')
    
    ax.set_ylabel('L1 dcache miss (%)')
    ax.set_xlabel('Query length')
    ax.set_xscale('log', base=2)
    ax.grid(True)
    # ax.set_ylim(0, 100)
    fig.savefig(media_dir + 'Single_thread_l1_dcache_miss.pdf')

    # page fault plot
    fig, ax = plt.subplots(figsize=(6,5))
    l_l1_dcache_miss = ax.plot(query_length_vec, page_faults_vec, \
        marker='.', c='blue', linewidth=1, label='Page fault')
    
    ax.set_ylabel('Page Fault rate (K/sec)')
    ax.set_xlabel('Query length')
    ax.set_xscale('log', base=2)
    ax.grid(True)
    # ax.set_ylim(0, 100)
    fig.savefig(media_dir + 'Single_thread_page_fault.pdf')
    


def plot_split_method() :
    # q for query split, d for database split
    query_length_vec_d, time_elapsed_vec_d, time_per_query_vec_d, \
    CPU_utilized_vec_d, frontend_cycles_vec_d, backend_cycles_vec_d, \
    L1_dcache_load_misses_vec_d, page_faults_vec_d = \
    parse_directory('./test_dir_database_split/database_split_result/')

    query_length_vec_q, time_elapsed_vec_q, time_per_query_vec_q, \
    CPU_utilized_vec_q, frontend_cycles_vec_q, backend_cycles_vec_q, \
    L1_dcache_load_misses_vec_q, page_faults_vec_q = \
    parse_directory('./test_dir_query_split/query_split_result/')


    # plot total time

    fig, ax = plt.subplots(figsize=(6,5))
    l_time_elapsed_q = ax.plot(query_length_vec_q, time_elapsed_vec_q, \
        marker='.', c='blue', linewidth=1, linestyle='-', label='query_split')

    l_time_elapsed_d = ax.plot(query_length_vec_d, time_elapsed_vec_d, \
        marker='x', c='blue', linewidth=1, linestyle='--', label='database split')

    ax.set_ylabel('Time (s)')
    ax.set_xlabel('Query entries')
    ax.set_xscale('log', base=2)
    ax.set_yscale('log')
    ax.grid(True)
    ax.legend()
    fig.savefig(media_dir + '64_threads_total_time.pdf')


    # plot single query time and cpu util
    fig, ax = plt.subplots(figsize=(6,5))

    l_time_per_query_q = ax.plot(query_length_vec_q, time_per_query_vec_q, \
        marker='.', c='blue', linewidth=1, linestyle='-', label='query split, time per query')

    l_time_per_query_d = ax.plot(query_length_vec_d, time_per_query_vec_d, \
        marker='x', c='blue', linewidth=1, linestyle='--', label='database split, time per query')
    
    ax.set_xlabel('Query entries')
    ax.set_xscale('log', base=2)
    ax.set_yscale('log')
    ax.set_ylabel('Time per query (s)')
    ax.grid(True)

    ax1 = ax.twinx()

    l_CPU_util_q = ax1.plot(query_length_vec_q, CPU_utilized_vec_q, \
        marker='.', c='red', linewidth=1, linestyle='-', label='query split, CPU utilization')

    l_CPU_util_d = ax1.plot(query_length_vec_d, CPU_utilized_vec_d, \
        marker='x', c='red', linewidth=1, linestyle='--', label='database split, CPU utilization')
    
    ax1.set_ylabel('CPU utilization')

    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax1.get_legend_handles_labels()

    fig.legend(handles1 + handles2, labels1 + labels2)


    fig.savefig(media_dir + '64_thread_CPU_and_time_per_query.pdf')




    # plot front and back cycles idle
    fig, ax = plt.subplots(figsize=(6,5))
    l_front_cycles_idle_q = ax.plot(query_length_vec_q, frontend_cycles_vec_q, \
        marker='.', c='blue', linewidth=1, linestyle='-', label='query split, idled frontend cycles')
    
    l_front_cycles_idle_d = ax.plot(query_length_vec_d, frontend_cycles_vec_d, \
        marker='x', c='blue', linewidth=1, linestyle='--', label='database split, idled frontend cycles')


    ax.set_xlabel('Query entries')
    ax.set_xscale('log', base=2)
    
    ax.set_ylabel('Frontend Percentage(%)')

    ax1 = ax.twinx()

    l_back_cycles_idle_q = ax1.plot(query_length_vec_q, backend_cycles_vec_q, \
        marker='.', c='red', linewidth=1, linestyle='-', label='query split, idled backend cycles')
    
    l_back_cycles_idle_d = ax1.plot(query_length_vec_d, backend_cycles_vec_d, \
        marker='x', c='red', linewidth=1, linestyle='--', label='database split, idled backend cycles')

    ax1.set_ylabel('Backend Percentage(%)')
    
    handles1, labels1 = ax.get_legend_handles_labels()
    handles2, labels2 = ax1.get_legend_handles_labels()

    fig.legend(handles1 + handles2, labels1 + labels2)

    ax.grid(True)

    fig.savefig(media_dir + '64_thread_idled_cycles.pdf')
    


    

    # L1 cache miss plot
    fig, ax = plt.subplots(figsize=(6,5))
    l_l1_dcache_miss_q = ax.plot(query_length_vec_q, L1_dcache_load_misses_vec_q, \
        marker='.', c='blue', linewidth=1, linestyle='-', label='query split, L1 cache miss')

    l_l1_dcache_miss_d = ax.plot(query_length_vec_d, L1_dcache_load_misses_vec_d, \
        marker='x', c='blue', linewidth=1, linestyle='--', label='database split, L1 cache miss')
    
    ax.set_ylabel('L1 dcache miss (%)')
    ax.set_xlabel('Query entries')
    ax.set_xscale('log', base=2)
    ax.grid(True)
    # ax.set_ylim(0, 100)
    ax.legend()
    fig.savefig(media_dir + '64_thread_l1_dcache_miss.pdf')



    # page fault plot
    fig, ax = plt.subplots(figsize=(6,5))
    l_l1_dcache_miss_q = ax.plot(query_length_vec_q, page_faults_vec_q, \
        marker='.', c='blue', linewidth=1, linestyle='-', label='query split, page fault')

    l_l1_dcache_miss_d = ax.plot(query_length_vec_d, page_faults_vec_d, \
        marker='x', c='blue', linewidth=1, linestyle='--', label='database split, page fault')
    
    ax.set_ylabel('Page fault rate (K/sec)')
    ax.set_xlabel('Query entries')
    ax.set_xscale('log', base=2)
    ax.grid(True)
    ax.legend()
    fig.savefig(media_dir + '64_thread_page_fault.pdf')


plot_split_method()
plot_single_thread()

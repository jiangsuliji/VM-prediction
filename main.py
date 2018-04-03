# compare scheduling based on different prediction algorithms
import copy

# input trace files and preprocess
#CPUtracepath = "traces/CPU.in.csv"  
#MEMtracepath = "traces/MEM.in.csv" 
CPUtracepathout = 'traces/CPU.out.csv'
MEMtracepathout = 'traces/MEM.out.csv'

CPUtracepath = "traces/predict_AAF-FSRV.csv"

# CPUtrace[0,1,2]: 0-accurate, 1-predict, 2-baseline
with open(CPUtracepath) as f:
    lines = f.readlines()
    CPUtrace0 = []
    CPUtrace1 = []
    CPUtrace2 = []
    for line in lines[1:]:
        tmp = line.split(',')
        CPUtrace0.append(float(tmp[3]))
        CPUtrace1.append(float(tmp[7]))
        CPUtrace2.append(float(tmp[6]))



with open(CPUtracepath) as f:
    lines = f.readlines()
    MEMtrace0 = []
    MEMtrace1 = []
    MEMtrace2 = []
    for line in lines[1:]:
        tmp = line.split(',')
        MEMtrace0.append(float(tmp[5]))
        MEMtrace1.append(float(tmp[9]))
        MEMtrace2.append(float(tmp[8]))

if len(CPUtrace0) != len(MEMtrace0): print("ERROR0: len of CPU and MEM trace diff")



# generate server cluster - server[x][t][CPU,MEM] 20 servers
server_num = 100
server = [[[0,0] for _ in range(24)] for _ in range(server_num)]
server_cpu = 10000 # upper bound CPU
server_mem = 10000 # upper bound MEM
#print(server)


# calculate price
# energy price TOU
price = [0.12,0.156274943634288,0.165628818358787,0.117693804804409,0.194992254682768,0.192264958784603,0.318664473877846,0.266636511990327,0.326670564838889,0.293872217772597,0.388948689571630,0.359970142368528,0.447810550493127,0.478695373133980,0.513388465378109,0.491034024181452,0.457621946795299,0.506109999205217,0.640870819945530,0.544380483035076,0.592130716398328,0.486134789641609,0.499381554660302,0.292508084600509]
cpu_alpha = 0.5
cpu_beta = 1.5
cpu_vth = 0.7
def cal_power(used_cpu):
    if used_cpu < cpu_vth*server_cpu:
        return cpu_alpha*used_cpu/server_cpu
    return cpu_alpha*used_cpu/server_cpu + cpu_beta*(used_cpu/server_cpu-cpu_vth)**2



# generate task - task[x][CPU,MEM,server,time]
# generate based on input trace, all 1 duration
task_num = 400 
entry_per_task = len(CPUtrace0)/task_num
def generate_task(traceCPU,traceMEM):
    task = [[0,0,0,0] for _ in range(task_num)]
    for i in range(task_num):
        task[i][0] = traceCPU[i]
        task[i][1] = traceMEM[i]
        #task[i][0] += sum(traceCPU[i*entry_per_task:(i+1)*entry_per_task])
        #task[i][1] += sum(traceMEM[i*entry_per_task:(i+1)*entry_per_task])
    return task

task0 = generate_task(CPUtrace0,MEMtrace0) # accurate
task1 = generate_task(CPUtrace1,MEMtrace1) # proposed
task2 = generate_task(CPUtrace2,MEMtrace2) # baseline

#print("task0:", task1)

# negotiation algorithm - first try intra only - TODO add inter later
iteration = 1
c_a = 0.1 # intra congestion weight
c_b = 0.1 # inter congestion weight
# intra cserver_intra[t]
cserver_intra = [0 for _ in range(24)] 

#print(cserver_intra)

def run_negotiation(task, server):
    print("run negotiation")
    # rip-up intra congestion terms
    cserver_intra = [0 for _ in range(24)] 
    for i in range(task_num):
        # cost increase and best decision for now
        ci, d_s, d_t = None, None, None
        for s in range(server_num):
            for t in range(24):
                # check violation of MEM/CPU
                if task[i][0] + server[s][t][0] >= server_cpu:
                    continue
                if task[i][1] + server[s][t][1] >= server_mem:
                    continue
                thisci = (1+c_a*cserver_intra[t])*price[t]*\
                        cal_power(task[i][0]+server[s][t][0])
                if ci == None or  thisci < ci:
                    d_s = s
                    d_t = t
        if d_s == None:
            print('ERROR: No valid decision')
            break
        # use the decision    
        server[d_s][d_t][0] += task[i][0]
        server[d_s][d_t][1] += task[i][1]
        task[i][2] = d_s
        task[i][3] = d_t
        cserver_intra[d_t] += 1
    rtn =[] # decisions[server,time]
    for k in task:
        rtn.append([k[2],k[3]])
    return rtn

# cal total power: input task decisions[task][server,time], task trace
def cal_total(decision, task):
    server = [[[0,0] for _ in range(24)] for _ in range(server_num)]
    for i in range(task_num):
        server[decision[i][0]] [decision[i][1]] [0] += task[i][0]
        server[decision[i][0]] [decision[i][1]] [1] += task[i][1]

    total = 0
    power = [0 for _ in range(24)]
    for t in range(24):
        # cal total power 
        for s in range(server_num):
            power[t] += cal_power(server[s][t][0])
        total += power[t]*price[t]

    return power, total


# main program starts here
print("===1st op: run negotiation based on predicted trace -- proposed algorithm ===")

# use predict trace
decision1 = run_negotiation(task1, server)
#print("server:", server)
#print("negotiation decision-proposed:",decision1)
power1, total_negotiation1 = cal_total(decision1, task0)

print("power and total price:", power1, total_negotiation1)


print("===2nd op: eval negotiation based on real trace===")
# reset server and run using the correct trace
server = [[[0,0] for _ in range(24)] for _ in range(server_num)]

decision0 = run_negotiation(task0, server)

power0, total_negotiation0 = cal_total(decision0, task0)

print("power and total price:", power0, total_negotiation0)


print("===3rd op: run negotiation based on predicted trace -- baseline algorithm ===")
# reset server and run using the co trace
task0 = generate_task(CPUtrace0,MEMtrace0) # accurate
server = [[[0,0] for _ in range(24)] for _ in range(server_num)]

decision2 = run_negotiation(task2, server)

#print("negotiation decision-baseline:",decision2)
power2, total_negotiation2 = cal_total(decision2, task0)

print("power and total price:", power2, total_negotiation2)

print("Final comparison--accurate-proposed-baseline:", total_negotiation0, total_negotiation1, total_negotiation2)


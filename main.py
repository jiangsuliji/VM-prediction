# compare scheduling based on different prediction algorithms


# input trace files and preprocess
CPUtracepath = "traces/CPU.in.csv"  
MEMtracepath = "traces/MEM.in.csv" 

# CPUtrace[0,1,2]: 0-accurate, 1-predict, 2-baseline
with open(CPUtracepath) as f:
    lines = f.readlines()
    CPUtrace0 = []
    CPUtrace1 = []
    for line in lines[1:]:
        tmp = line.split(',')
        CPUtrace0.append(float(tmp[2]))
        CPUtrace1.append(float(tmp[3]))

with open(MEMtracepath) as f:
    lines = f.readlines()
    MEMtrace0 = []
    MEMtrace1 = []
    for line in lines[1:]:
        tmp = line.split(',')
        MEMtrace0.append(float(tmp[2]))
        MEMtrace1.append(float(tmp[3]))

if len(CPUtrace0) != len(MEMtrace0): print("ERROR0: len of CPU and MEM trace diff")

# energy price TOU
price = [0.12,0.156274943634288,0.165628818358787,0.117693804804409,0.194992254682768,0.192264958784603,0.318664473877846,0.266636511990327,0.326670564838889,0.293872217772597,0.388948689571630,0.359970142368528,0.447810550493127,0.478695373133980,0.513388465378109,0.491034024181452,0.457621946795299,0.506109999205217,0.640870819945530,0.544380483035076,0.592130716398328,0.486134789641609,0.499381554660302,0.292508084600509]

# generate server cluster - server[x][t][CPU,MEM] 20 servers
server_num = 20
server = [[[0,0] for _ in range(24)] for _ in range(server_num)]
server_cpu = 100000 # upper bound CPU
server_mem = 100000 # upper bound MEM
#print(server)

# generate task - task[x][CPU,MEM][start time]
# generate based on input trace, all 1 duration
task_num = 10
entry_per_task = len(CPUtrace0)/task_num
def generate_task(traceCPU,traceMEM):
    task = [[0,0,0] for _ in range(task_num)]
    for i in range(task_num):
        task[i][0] += sum(traceCPU[i*entry_per_task:(i+1)*entry_per_task])
        task[i][1] += sum(traceMEM[i*entry_per_task:(i+1)*entry_per_task])
    return task

task0 = generate_task(CPUtrace0,MEMtrace0)
task1 = generate_task(CPUtrace1,MEMtrace1)

print(task0)

# negotiation algorithm - first try intra only - TODO add inter later
iteration = 5
a = 0.1 # intra congestion term
b = 0.1 # inter congestion term
cserver_intra = [[0 for _ in range(24)] for _ in range(server_num)]

print(cserver_intra)






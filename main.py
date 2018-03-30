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
        CPUtrace0.append(tmp[2])
        CPUtrace1.append(tmp[3])

with open(MEMtracepath) as f:
    lines = f.readlines()
    MEMtrace0 = []
    MEMtrace1 = []
    for line in lines[1:]:
        tmp = line.split(',')
        MEMtrace0.append(tmp[2])
        MEMtrace1.append(tmp[3])

#print(len(CPUtrace0), len(MEMtrace0))





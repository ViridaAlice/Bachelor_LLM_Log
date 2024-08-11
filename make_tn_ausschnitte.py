import json
import random

def main(dir_name, file_name, allowed_len):
    direc = dir_name+"/gather/ganze_dateien/true_pos/"
    file1 = direc+file_name
    label1 = dir_name+"/gather/label_"+file_name
    output_pos = dir_name+"/gather/ausschnitte/true_neg/"

    da_list = []
    data = []
    with open(label1, 'r') as file:
        for line in file:
            data.append(json.loads(line))

    for k in data:
        line = k["line"]
        da_list.append(line)

    data2 = []
    with open(file1) as file:
        data2 = [line.rstrip() for line in file]

    intervals = []
    current_interval = [da_list[0]]
    
    for num in da_list[1:]:
        if num == current_interval[-1] + 1:
            current_interval.append(num)
        else:
            intervals.append(current_interval)
            current_interval = [num]

    intervals.append(current_interval)
    print(intervals)
    
    mom = 0
    j = 1
    fac = 1.0
    while j < 3:
        diff = (intervals[mom][0] - 1)
        if diff-2 > allowed_len*fac:
            start = random.randint(1, int(1+diff-allowed_len*fac))
            end = start + allowed_len*fac
            data3 = data2[start-1:int(end)]
            build_json = {"data": data3, "lines": (start, end), "labels": []}
            j += 1
            with open(output_pos+"tn_"+str(start)+"_to_"+str(end)+"-"+file_name, "w") as outfile:
                json.dump(build_json, outfile, indent=2)
        for mom in range(1,len(intervals)-1):
            if j >= 3:
                break
            diff = (intervals[mom][0] - intervals[mom-1][-1] )
            if diff-2 > allowed_len*fac:
                start = random.randint(intervals[mom-1][-1]+1, int(intervals[mom-1][-1]+1+diff-allowed_len*fac))
                end = start + allowed_len*fac
                data3 = data2[start-1:int(end)]
                build_json = {"data": data3, "lines": (start, end), "labels": []}
                j += 1
                with open(output_pos+"tn_"+str(start)+"_to_"+str(end)+"-"+file_name, "w") as outfile:
                    json.dump(build_json, outfile, indent=2)
        if diff-2 > allowed_len*fac:
            if j >= 3:
                break
            diff = (len(data2)-1 - intervals[mom][-1])
            if diff-2 > allowed_len*fac:
                start = random.randint(intervals[mom][-1]+1, int(len(data2)-1-allowed_len*fac))
                end = start + allowed_len*fac
                data3 = data2[start-1:int(end)]
                build_json = {"data": data3, "lines": (start, end), "labels": []}
                j += 1
                with open(output_pos+"tn_"+str(start)+"_to_"+str(end)+"-"+file_name, "w") as outfile:
                    json.dump(build_json, outfile, indent=2)
        fac = fac * 0.75
        if fac < 0.10:
            print("We had some troubles :(")
            break 
    

if __name__ == "__main__":
    file_names = ["dnsmasq.log", "audit.log", "audit_internal.log", "openvpn.log"]# "auth.log",
    dir_names = ["fox", "harrison", "russellmitchell", "santos","wardbeck", "wheeler", "wilson"]
    allowed_len = {"dnsmasq.log":50, "audit.log":43, "audit_internal.log":43, "auth.log":93, "openvpn.log":61}
    
    
    for d_n in dir_names:
        for f_n in file_names:
            main(d_n, f_n, allowed_len[f_n])
            print("finished: "+d_n+" / "+f_n+"! :D")
    
    special_file_names = {"fox":["2022-01-18-system.cpu.log", "intranet.price.fox.org-access.log.2", "intranet.price.fox.org-error.log.1"],
                            "harrison":["2022-02-08-system.cpu.log", "intranet.mannsmith.harrison.com-access.log.1", "intranet.mannsmith.harrison.com-error.log.1"], 
                            "russellmitchell":["2022-01-24-system.cpu.log", "intranet.smith.russellmitchell.com-access.log.2", "intranet.smith.russellmitchell.com-error.log.2"],
                           "santos": ["2022-01-17-system.cpu.log", "intranet.smith.santos.com-access.log", "intranet.smith.santos.com-error.log"],
                              "shaw":["2022-01-29-system.cpu.log", "intranet.thomasmurray.shaw.info-access.log.2", "intranet.thomasmurray.shaw.info-error.log.2", "auth.log.1"], 
                              "wardbeck":["2022-01-23-system.cpu.log", "intranet.hurstwong.wardbeck.info-access.log.1", "intranet.hurstwong.wardbeck.info-error.log.1"], 
                              "wheeler": ["", "intranet.flores.wheeler.biz-access.log.1","intranet.flores.wheeler.biz-error.log.1"], 
                              "wilson":["2022-02-07-system.cpu.log", "intranet.hallbrown.wilson.com-access.log.2", "intranet.hallbrown.wilson.com-error.log.2"]}
    special_file_lengths = [8, 32, 33, 93] #cpu, access, error
        
    for d_n in special_file_names:
        main(d_n, special_file_names[d_n][2], 33)
    """
    for d_n in ["wheeler"]:
        for m in range(1,3):
            main(d_n, special_file_names[d_n][m], special_file_lengths[m])
            print("finished: "+d_n+" / "+special_file_names[d_n][m]+"! :D")
        if d_n == "shaw":
            main(d_n, special_file_names[d_n][3], special_file_lengths[3])
            print("finished: "+d_n+" / "+special_file_names[d_n][3]+"! :D")
            """
            


            
    #main("wilson","dnsmasq.log", 32)

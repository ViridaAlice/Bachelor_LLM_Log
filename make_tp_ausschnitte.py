import json
import random
from pathlib import Path


def main(dir_name, file_name, allowed_len):
    direc = dir_name+"/gather/ganze_dateien/true_pos/"
    file1 = direc+file_name
    label1 = dir_name+"/gather/label_"+file_name
    output_pos = dir_name+"/gather/ausschnitte/true_pos/"
    
    Path(output_pos).mkdir(parents=True, exist_ok=True)

    line_list = []  # alle verdaechtigen zeilen
    line_gt_list = {}   # zeilennr : art der attacke in der jeweiligen zeile
    # open file & compile all lines into line_list dict
    with open(label1, 'r') as file:
        for line in file:
            line_list.append(json.loads(line)["line"])
            line_gt_list[json.loads(line)["line"]] = json.loads(line)["labels"]

            
    data2 = []
    with open(file1) as file:
        data2 = [line.rstrip() for line in file]
            
    intervals = []
    current_interval = [line_list[0]]
    
    # Split lines into consecutive attacks and save in intervals as list in list
    for num in line_list[1:]:
        # speichere in Intv_dict die labels aller zeilen, die zum intervall x gehoeren: intv_dict[2] = [a, b, c] 
        # -> intervall beginnend in zeile 2 (!) hat die labels a, b und c 
        if num == current_interval[-1] + 1:
            current_interval.append(num)
        else:
            intervals.append(current_interval)
            current_interval = [num]

    intervals.append(current_interval)
    
    curr_labels_dict = {}
    build_json = {}
    done_deal = {}
    
    if not intervals:
        print(file1+" was not properly considered! beware")
        

    for intv_list in intervals:
        curr_labels_dict = {}
        intv_end = intv_list[-1]
        if intv_end - allowed_len < 0:
            continue
        intv_start = -1
        while intv_start < 0:
            ran = random.randint(0, len(intv_list)-1)
            intv_start = intv_list[ran] - allowed_len
            intv_end = intv_list[ran]         
        
        data2 = data2[intv_start:intv_end]

        for jede_zeile in intv_list:
            if jede_zeile > intv_end:
                break
            if jede_zeile < intv_start:
                continue
            for b in line_gt_list[jede_zeile]:
                if b in curr_labels_dict:
                    curr_labels_dict[b].append(jede_zeile-intv_start)
                else:
                    curr_labels_dict[b] = [jede_zeile-intv_start]

        if set(curr_labels_dict.keys()).issubset(done_deal.keys()):
            break
        #else:
            #print(curr_labels_dict)
            

        build_json = {"data": data2, "lines": (intv_start, intv_end), "labels": curr_labels_dict}

        done_deal.update(curr_labels_dict)

        with open(output_pos+"tp_"+str(intv_start)+"_to_"+str(intv_end)+"-"+file_name, "w") as outfile:
            print("just wrote the file :3")
            json.dump(build_json, outfile, indent=2)
            return True
    return False
    

if __name__ == "__main__":
    file_names = ["dnsmasq.log", "audit_intranet.log", "audit_internal.log", "openvpn.log", "auth.log"]
    dir_names = ["fox", "harrison", "russellmitchell", "santos","shaw", "wardbeck", "wheeler", "wilson"]
    allowed_len = {"dnsmasq.log":39, "audit_intranet.log":43, "audit_internal.log":43, "auth.log":93, "openvpn.log":61}
    
    
    for d_n in dir_names:
        for f_n in ["dnsmasq.log"]:
            print("now processing: "+d_n+" / "+f_n+"! :D")
            main(d_n, f_n, allowed_len[f_n])
            print("just finished :)")
    """
    
    
    special_file_names = {"fox":["2022-01-18-system.cpu.log", "intranet.price.fox.org-access.log.2", "intranet.price.fox.org-error.log.1"],
                            "harrison":["2022-02-08-system.cpu.log", "intranet.mannsmith.harrison.com-access.log.1", "intranet.mannsmith.harrison.com-error.log.1"], 
                            "russellmitchell":["2022-01-24-system.cpu.log", "intranet.smith.russellmitchell.com-access.log.2", "intranet.smith.russellmitchell.com-error.log.2"],
                           "santos": ["2022-01-17-system.cpu.log", "intranet.smith.santos.com-access.log", "intranet.smith.santos.com-error.log"],
                              "shaw":["2022-01-29-system.cpu.log", "intranet.thomasmurray.shaw.info-access.log.2", "intranet.thomasmurray.shaw.info-error.log.2", "auth.log.1"], 
                              "wardbeck":["2022-01-23-system.cpu.log", "intranet.hurstwong.wardbeck.info-access.log.1", "intranet.hurstwong.wardbeck.info-error.log.1"], 
                              "wheeler": ["", "intranet.flores.wheeler.biz-access.log.1","intranet.flores.wheeler.biz-error.log.1"], 
                              "wilson":["2022-02-07-system.cpu.log", "intranet.hallbrown.wilson.com-access.log.2", "intranet.hallbrown.wilson.com-error.log.2"]}
    special_file_lengths = [8, 32, 33, 93] #cpu, access, error
        
    main("wheeler","intranet.flores.wheeler.biz-access.log.1",32)
    for d_n in ["wilson"]:
        print("now processing: "+d_n+" / "+d_n[0]+"! :D")
        fac = 1.0
        if d_n[0] == "":
            continue
        while not main(d_n, special_file_names[d_n][0], int(8*fac)) and fac > 0.2:
            fac = fac * 0.75
        if fac <= 0.2:
            print("sad dog :/")
        print("just finished :)")
    
    for d_n in special_file_names:
        for o in range(0,3):
            if special_file_names[d_n][o] == "":
                continue
            print("now processing: "+d_n+" / "+special_file_names[d_n][o]+"! :D")
            main(d_n, special_file_names[d_n][o], special_file_lengths[o])
            print("just finished :)")
    """
    """
    for d_n in ["wheeler"]:
        for m in range(1,3):
            print("now processing: "+d_n+" / "+special_file_names[d_n][m]+"! :D")
            main(d_n, special_file_names[d_n][m], special_file_lengths[m])
            print("just finished :)")   
        if d_n == "shaw":
            print("now processing: "+d_n+" / "+special_file_names[d_n][3]+"! :D")
            main(d_n, special_file_names[d_n][3], special_file_lengths[3])
            print("just finished :)")
    # only remaining one, get the auth log
    #main("wheeler", "auth.log", 93)
    """

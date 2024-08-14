import json
import random
from pathlib import Path

def main(dir_name, file_name, allowed_len):
    direc = dir_name+"/gather/"
    file1 = direc+file_name
    label1 = dir_name+"/gather/label_"+file_name
    output_pos = dir_name+"/gather/ausschnitte/true_neg/"
    
    Path(output_pos).mkdir(parents=True, exist_ok=True)

    da_list = [] # alle lines die suspicious sind
    data = [] # alle groundtruth labels der datei
    with open(label1, 'r') as file:
        for line in file:
            data.append(json.loads(line))

    for k in data:
        line = k["line"]
        da_list.append(line)

    data2 = [] # alle lines der log datei
    with open(file1) as file:
        data2 = [line.rstrip() for line in file]

    intervals = []
    # erste verdaechtige line:
    current_interval = [da_list[0]] 
    
    # fruehestes start und end intervall, das true neg 
    # ausschnitt zulaesst. chosen_interval_start[j] 
    # korrespondiert zu chosen_interval_end[j]
    chosen_interval_start = []
    chosen_interval_end = []
    

    #fact = 1.0
    #while fact > 0.2:
    for i in range(0, len(da_list)):
        if i == 0 and da_list[i] > allowed_len:
            chosen_interval_start.append(0)
            chosen_interval_end.append(da_list[i])
            continue
        if i == len(da_list)-1 and len(data2)-1 - da_list[i] > allowed_len:
            chosen_interval_start.append(da_list[i])
            chosen_interval_end.append(len(data2))
            continue
        else: 
            if da_list[i] - da_list[i-1] > allowed_len:
                chosen_interval_start.append(da_list[i-1])
                chosen_interval_end.append(da_list[i])
                continue
        #fact = fact * 0.75
        #allowed_len = int(allowed_len * fact)

    if not chosen_interval_start:
        print("Not a single fitting intervall was found! for len "+ str(allowed_len))
        return False

    for j in range(0, len(chosen_interval_start)):
        intv_start = random.randint(chosen_interval_start[j], chosen_interval_end[j]-allowed_len)
        intv_end = intv_start + allowed_len

    data3 = data2[intv_start-1:intv_end]
    build_json = {"data": data3, "lines": (intv_start, intv_end), "labels": []}

    with open(output_pos+"tn_"+str(intv_start)+"_to_"+str(intv_end)+"-"+file_name, "w") as outfile:
        print("just wrote the file!! :3")
        json.dump(build_json, outfile, indent=2)
        return True
    

if __name__ == "__main__":
    """
    file_names = ["dnsmasq.log", "audit_intranet.log", "audit_internal.log", "openvpn.log", "auth.log"]
    dir_names = ["fox", "harrison", "russellmitchell", "santos","shaw", "wardbeck", "wheeler", "wilson"]
    allowed_len = {"dnsmasq.log":50, "audit_intranet.log":43, "audit_internal.log":43, "auth.log":93, "openvpn.log":61}
    
    for d_n in dir_names:
        for f_n in file_names:
            print("now processing: "+d_n+" / "+f_n+"! :D")
            main(d_n, f_n, allowed_len[f_n])
            print("finished :)")
    """
    
    special_file_names = {"fox":["2022-01-18-system.cpu.log", "intranet.price.fox.org-access.log.2"],
                            "harrison":["2022-02-08-system.cpu.log", "intranet.mannsmith.harrison.com-access.log.1"], 
                            "russellmitchell":["2022-01-24-system.cpu.log", "intranet.smith.russellmitchell.com-access.log.2"],
                           "santos": ["2022-01-17-system.cpu.log", "intranet.smith.santos.com-access.log", "intranet.smith.santos.com-error.log"],
                              "shaw":["2022-01-29-system.cpu.log", "intranet.thomasmurray.shaw.info-access.log.2"], 
                              "wardbeck":["2022-01-23-system.cpu.log", "intranet.hurstwong.wardbeck.info-access.log.1"], 
                              "wheeler": ["", "intranet.flores.wheeler.biz-access.log.1"], 
                              "wilson":["2022-02-07-system.cpu.log", "intranet.hallbrown.wilson.com-access.log.2"]}
    special_file_lengths = [8, 32] #cpu, access, error
    d_n = "wilson"
    f_n = "intranet.hallbrown.wilson.com-access.log.2"
    leng = 32
    fac = 1.0
    while not main(d_n, f_n, int(leng*fac)) and fac > 0.1:
        fac = fac * 0.75
    if fac <= 0.1:
        print("we have NOT succeeded. sad dog :/")
    else:
        print("YAY :)")
    print("just finished processing: "+d_n+" / "+f_n+"! :)")


    """
    for d_n in special_file_names:
        for o in range(0,2):
            if special_file_names[d_n][o] == "":
                continue
            fac = 1.0
            while not main(d_n, special_file_names[d_n][o], int(special_file_lengths[o]*fac)) and fac > 0.1:
                fac = fac * 0.75
            if fac <= 0.1:
                print("we have NOT succeeded. sad dog :/")
            else:
                print("YAY :)")
            print("just finished processing: "+d_n+" / "+special_file_names[d_n][o]+"! :)")
    
    for d_n in ["wheeler"]:
        for m in range(1,3):
            fac = 1.0
            while not main(d_n, special_file_names[d_n][m], int(special_file_lengths[m]*fac)) and fac > 0.1:
                fac = fac * 0.75            
            if fac <= 0.1:
                print("we have NOT succeeded. sad dog :/")
            print("finished: "+d_n+" / "+special_file_names[d_n][m]+"! :D")
        if d_n == "shaw":
            fac = 1.0
            while not main(d_n, special_file_names[d_n][3], int(special_file_lengths[3]*fac)) and fac > 0.1:
                fac = fac * 0.75
            if fac <= 0.1:
                print("we have NOT succeeded. sad dog :/")
            print("finished: "+d_n+" / "+special_file_names[d_n][3]+"! :D")
    """
    
           
            

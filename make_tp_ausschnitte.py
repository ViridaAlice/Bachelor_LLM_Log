import json
import random


def main(dir_name, file_name, allowed_len):
    direc = dir_name+"/gather/ganze_dateien/true_pos/"
    file1 = direc+file_name
    label1 = dir_name+"/gather/label_"+file_name
    output_pos = dir_name+"/gather/ausschnitte/true_pos/"

    line_list = []
    line_gt_list = {}
    # open file & compile all lines into line_list dict
    with open(label1, 'r') as file:
        for line in file:
            line_list.append(json.loads(line)["line"])
            line_gt_list[json.loads(line)["line"]] = json.loads(line)["labels"]
            
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
    #allowed_intv = intervals
    
    allowed_intv = []
    # Filter alle intervalle kleiner max erlaubt length
    for l in intervals:
        if len(l) < allowed_len:
            allowed_intv.append(l)
            

    i = 1 
    curr_labels_dict = {}
    build_json = {}
    done_deal = {}
    if not allowed_intv:
        print(file1+" was not properly considered! beware")

    for j in allowed_intv:
        curr_labels_dict = {}
        intv_start = j[0]
        start = -1
        while start < 0:
            ran = random.randint(1, allowed_len-len(j))
            start = intv_start - ran
            end = start + allowed_len
        
        
        data2 = []
        with open(file1) as file:
            data2 = [line.rstrip() for line in file]

        data2 = data2[start:end]
            
        i += 1
        

        for k in j:
            if k > end:
                break
            for b in line_gt_list[k]:
                if b in curr_labels_dict:
                    curr_labels_dict[b].append(k-start)
                else:
                    curr_labels_dict[b] = [k-start]

        if set(curr_labels_dict.keys()).issubset(done_deal.keys()):
            break
        else:
            print(curr_labels_dict)
            

        build_json = {"data": data2, "lines": (start, end), "labels": curr_labels_dict}

        done_deal.update(curr_labels_dict)

        with open(output_pos+"tp_"+str(start)+"_to_"+str(end)+"-"+file_name, "w") as outfile:
            json.dump(build_json, outfile, indent=2)
    

if __name__ == "__main__":
    file_names = ["dnsmasq.log", "audit.log", "audit_internal.log", "auth.log", "openvpn.log"]
    dir_names = ["wheeler", "wilson"]
    allowed_len = {"dnsmasq.log":50, "audit.log":43, "audit_internal.log":43, "auth.log":93, "openvpn.log":61}
    """
    for d_n in dir_names:
        for f_n in file_names:
            main(d_n, f_n, allowed_len[f_n])
            print("ya!")
    """

    main("wilson","intranet.hallbrown.wilson.com-access.log.2", 32)
            

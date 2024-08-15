
import json
import os
from pathlib import Path



def main(dir_name, file_name):
    direc = dir_name+"/gather/ausschnitte/true_pos/"
    file1 = direc+file_name
    output_pos = dir_name+"/gather/ausschnitte/true_pos/clean/"

    Path(output_pos).mkdir(parents=True, exist_ok=True)


    with open(file1) as json_file:
        json_dict = json.load(json_file)
        tobe_cleaned = json_dict["data"]
        #labels = json_dict["labels"]

    with open(output_pos+file_name, "w") as outp_file:
        i = 1
        for a in tobe_cleaned:
            outp_file.write(str(i)+": "+a+"\n")
            i += 1
        #json.dump(labels, outp_file)

    """
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
    """
    

if __name__ == "__main__":
    dir_names = ["fox", "harrison", "russellmitchell", "santos", "shaw", "wardbeck", "wheeler", "wilson"]
    
    directory = os.getcwd()

    for d_n in dir_names:
        for file in os.listdir(directory+"/"+d_n+"/gather/ausschnitte/true_pos/"):
            f_n = os.fsdecode(file)
            if f_n.startswith("!"): 
                print("now working on "+ d_n +"/"+ f_n)
                main(directory+"/"+d_n, f_n)
                continue
            else:
                continue

            

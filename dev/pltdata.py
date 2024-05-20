import re
import math

def parse_metrics(text):
    # Define regular expression patterns
    batch_pattern = re.compile(r"batch\s+(\d+)\s+\(.*?\):")
    eval_train_pattern = re.compile(r"EvalTraincurrent metrics:\s*\{([^}]*)\}")
    test_pattern = re.compile(r"Test current metrics:\s*\{([^}]*)\}")

    # Find all matches for batch numbers
    batch_matches = batch_pattern.finditer(text)
    eval_train_matches = eval_train_pattern.finditer(text)
    test_matches = test_pattern.finditer(text)
    
    # Helper function to convert metrics string to dictionary
    def convert_to_dict(metrics_str):
        metrics_items = metrics_str.split(',')
        metrics_dict = {}
        for item in metrics_items:
            key, value = item.split(':')
            key = key.strip().strip("'")
            value = value.strip()
            if value == 'nan':
                value = float('nan')
            else:
                value = float(value)
            metrics_dict[key] = value
        return metrics_dict

    metrics_data = []

    # Iterate over batch matches and extract corresponding metrics
    for batch_match in batch_matches:
        batch_number = int(batch_match.group(1))
        eval_train_match = next(eval_train_matches, None)
        test_match = next(test_matches, None)

        if eval_train_match and test_match:
            eval_train_metrics = convert_to_dict(eval_train_match.group(1))
            test_metrics = convert_to_dict(test_match.group(1))

            metrics_data.append({
                "batch_number": batch_number,
                "EvalTraincurrent_metrics": eval_train_metrics,
                "Test_current_metrics": test_metrics
            })

    return metrics_data

text=file_to_text(opjD('nohup.out'))

a=text.split('\nout_folder = ')
b={}
for i in range(1,len(a)):
    c=a[i]
    d=c.split('\n')
    e=d[0]
    b[e]=c
e=select_from_list(kys(b))

text=b[e]

metrics_data = parse_metrics(text)
categories=kys(metrics_data[0]['EvalTraincurrent_metrics'])
stats={}



for k in categories:
    if 'IoU' in k or 'fprate' in k or 'bump' in k or 'island' in k or 'bike' in k or 'edge' in k:
        continue
    bn=[]
    a=[]
    b=[]
    n=len(metrics_data)
    #for i in range(6052,6441):
    for i in range(0,n):
        data=metrics_data[i]
        d=data['batch_number']
        bn.append(d)
        #a.append(data['EvalTraincurrent_metrics'][k])
        b.append(data['Test_current_metrics'][k])
    a=na(a);a[np.isnan(a)]=0
    b=na(b);b[np.isnan(b)]=0
    figure(k)
    #clf()
    s=0.985
    #s=1-1/(0.3*len(bn))
    #plot(bn,smooth(a,s),'-',label='train')
    if e[-1]=='/':
        e=e[:-1]
    plot(bn,smooth(b,s),'-',label=fname(e)+' test')#'test')
    #plot(bn,a,'-',label='train')
    #plot(bn,b,'-',label='test')
    plt.legend(loc='lower right')
    plt.title(k)
    ctr=0
    val=0
    """
    for i in rlen(bn):
        if bn[i]<200e3 or bn[i]>400e3:
            continue
        val+=b[i]
        ctr+=1
    val/=ctr
    stats[k]=val
    """
kprint(stats)
        
if False:
    data={}
    for k in s7:
        data[k]=[]
    for k in s6:
        data[k].append(s6[k])
    for k in s7:
        data[k].append(s7[k])
    df=pd.DataFrame(data)
    df.to_excel(opjD('output.xlsx'),index=False)

#EOF

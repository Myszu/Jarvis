
from datetime import datetime, timedelta

def calculate_progress(current, max, delta=0):
    emptySegment = '-'
    fullsegment = '█'
    percent = int(((current+1) / max) * 100)
    if delta == 0:
        progressBar = f'[ {emptySegment*25} ] {percent}% ({current+1} / {max})'
    else:
        now = datetime.now()
        eta = (now + timedelta(seconds=(max*delta))).strftime("%d.%m.%Y %H:%M:%S")
        progressBar = f'[ {emptySegment*25} ] {percent}% ({current+1} / {max}) || ETA: {eta}'
        
    toChange = percent // 4
        
    progressBar = progressBar.replace(emptySegment, fullsegment, toChange)
    print(progressBar)

export JOBNAME=$parsl.localprovider.1634004880.189384
set -e
export CORES=$(getconf _NPROCESSORS_ONLN)
[[ "1" == "1" ]] && echo "Found cores : $CORES"
WORKERCOUNT=1
FAILONANY=0
PIDS=""

CMD() {
process_worker_pool.py --debug  -a 221.186.103.38,GoichiMacBook.local,192.168.11.4 -p 0 -c 1 -m None --poll 10 --task_port=54712 --result_port=54331 --logdir=/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Parsl/01_Intro/runinfo/001/htex_Local --block_id=0 --hb_period=30  --hb_threshold=120 --cpu-affinity none 
}
for COUNT in $(seq 1 1 $WORKERCOUNT); do
    [[ "1" == "1" ]] && echo "Launching worker: $COUNT"
    CMD $COUNT &
    PIDS="$PIDS $!"
done

ALLFAILED=1
ANYFAILED=0
for PID in $PIDS ; do
    wait $PID
    if [ "$?" != "0" ]; then
        ANYFAILED=1
    else
        ALLFAILED=0
    fi
done

[[ "1" == "1" ]] && echo "All workers done"
if [ "$FAILONANY" == "1" ]; then
    exit $ANYFAILED
else
    exit $ALLFAILED
fi

# nonperiodic-nlmt

Run Python script to increase the frame counter with respect to any distribution. Shared memory location is `/dev/shm/5gue_frame`:
```
python main.py
```

Run NLMT server:
```
./nlmt server -i 0 -d 0 -l 0 -o d --outdir=/tmp/
```

Run NLMT client Using a shared memory location as a clock:
```
./nlmt client --tripm=oneway -i 10ms -f 5ms -p /dev/shm/5gue_frame -y 10ms -g nlmt/t1 -l 100 -m 1 -d 10s -o d --outdir=/tmp/ 192.168.1.1
```

After the test is done, download the file:
```
cp /tmp/nlmt/t1/server/se_192-168-2-2_49247_20240130_150636.json.gz ~/here/results
```

Plot arrival times histogram:
```
python validate.py se_192-168-2-2_49247_20240130_150636.json.gz
```

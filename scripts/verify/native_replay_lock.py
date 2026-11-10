"""One writer per native unit report, including independent retry passes."""
import atexit,os,time

def acquire_report_lock(folder):
    stream=(folder/'.replay.lock').open('a+b')
    stream.seek(0,2)
    if not stream.tell():stream.write(b'0');stream.flush()
    stream.seek(0)
    if os.name=='nt':
        import msvcrt
        while True:
            try:msvcrt.locking(stream.fileno(),msvcrt.LK_NBLCK,1);break
            except OSError:time.sleep(.1)
    else:
        import fcntl
        fcntl.flock(stream.fileno(),fcntl.LOCK_EX)
    atexit.register(stream.close)
    return stream

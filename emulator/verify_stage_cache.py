import stage_cache as s
from PIL import Image

def main():
    s.begin_stage('test-a');cache=s.StageCache();loads=0
    for i in range(200):
        cache[i]=Image.new('RGBA',(16,16));loads+=1
        while len(cache)>2:cache.popitem(last=False)
    assert len(cache)==2 and len(cache.retained)==198
    assert cache.pop(0) is not None # reuse after normal LRU spill, same stage
    before=s.cache_stats()['bytes'];s.begin_stage('test-a');assert s.cache_stats()['bytes']==before
    s.begin_stage('test-b');assert not cache and not cache.retained and s.cache_stats()['bytes']==0
    old=s.MAX_BYTES;s.MAX_BYTES=3072
    try:
        for i in range(3):cache[i]=Image.new('RGBA',(16,16))
        cache.get(0);cache[3]=Image.new('RGBA',(16,16))
        assert 0 in cache and 1 not in cache and 2 in cache and 3 in cache
        assert s.cache_stats()['bytes']<=s.MAX_BYTES
    finally:s.MAX_BYTES=old;s.begin_stage('test-end')
    print('Stage retention, same-stage reuse, stage change and global LRU budget passed')

if __name__=='__main__':main()

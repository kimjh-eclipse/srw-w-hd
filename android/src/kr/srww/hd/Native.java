package kr.srww.hd;

final class Native {
    static {
        android.util.Log.i("srwwhd", "load retro");
        System.loadLibrary("retro");
        android.util.Log.i("srwwhd", "load host");
        System.loadLibrary("srwwhost");
        android.util.Log.i("srwwhd", "libs loaded");
    }
    static native boolean init(String rom, String dir, String hdDir);
    static native void setHd(boolean on);
    static native boolean hdReady();
    /** battle rumble event: out = {low, high, beam}; returns ms, 0 = stop, -1 = none */
    static native int rumble(float[] out);
    static native void surface(int w, int h);
    static native void frame(int run, float[] top, float[] bottom, int linear);
    static native void reset();
    static native void input(int buttons, int touching, int x, int y);
    static native int audio(short[] out);
    static native boolean saveState(String path);
    static native boolean loadState(String path);
}

package kr.srww.hd;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.graphics.RectF;
import android.media.AudioFormat;
import android.media.AudioManager;
import android.media.AudioTrack;
import android.net.Uri;
import android.opengl.GLSurfaceView;
import android.os.Bundle;
import android.view.InputDevice;
import android.view.KeyEvent;
import android.view.MotionEvent;
import android.view.View;
import android.view.WindowManager;
import android.widget.FrameLayout;
import android.widget.Toast;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;

import javax.microedition.khronos.egl.EGLConfig;
import javax.microedition.khronos.opengles.GL10;

/** Plays the game with the original screens (no HD composition yet), translucent on-screen pad,
 *  game pads, options menu and quick save slots. */
public class MainActivity extends Activity implements GLSurfaceView.Renderer, ControlsView.Listener {
    static final int B = 0, Y = 1, SELECT = 2, START = 3, UP = 4, DOWN = 5, LEFT = 6, RIGHT = 7, A = 8, X = 9, L = 10, R = 11;
    static final int PICK_ROM = 1;

    Settings settings;
    GLSurfaceView view;
    ControlsView controls;
    File rom, autoState;
    volatile boolean ready, paused, fast, fastKey;
    volatile boolean tabFast;
    boolean l2Axis, r2Axis;
    final float[] rumbleEvent = new float[3];
    volatile float[] topRect = new float[4], bottomRect = new float[4];
    volatile int touchButtons, keyButtons, axisButtons, touching, touchX, touchY;
    long last; double owed;
    AudioTrack track;
    Thread audioThread;

    @Override protected void onCreate(Bundle b) {
        super.onCreate(b);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON | WindowManager.LayoutParams.FLAG_FULLSCREEN);
        settings = new Settings(this);
        applyOrientation();
        rom = new File(getFilesDir(), "game.nds");
        autoState = new File(getFilesDir(), "auto.state");
        if (rom.exists()) start(); else pickRom();
    }

    void pickRom() {
        Intent i = new Intent(Intent.ACTION_OPEN_DOCUMENT);
        i.addCategory(Intent.CATEGORY_OPENABLE);
        i.setType("*/*");
        startActivityForResult(i, PICK_ROM);
        Toast.makeText(this, "게임 롬(.nds) 파일을 선택하세요", Toast.LENGTH_LONG).show();
    }

    @Override protected void onActivityResult(int req, int res, Intent data) {
        if (req != PICK_ROM) return;
        if (res != RESULT_OK || data == null) { if (!rom.exists()) finish(); else resumeGame(); return; }
        Uri uri = data.getData();
        File tmp = new File(getFilesDir(), "game.tmp");
        try (InputStream in = getContentResolver().openInputStream(uri); FileOutputStream out = new FileOutputStream(tmp)) {
            byte[] buf = new byte[1 << 16]; int n;
            while ((n = in.read(buf)) > 0) out.write(buf, 0, n);
        } catch (Exception e) {
            Toast.makeText(this, "롬을 복사하지 못했습니다: " + e.getMessage(), Toast.LENGTH_LONG).show();
            tmp.delete(); if (!rom.exists()) finish(); return;
        }
        boolean restart = rom.exists();
        rom.delete(); tmp.renameTo(rom); autoState.delete();
        if (restart) { Toast.makeText(this, "새 롬으로 다시 시작합니다", Toast.LENGTH_SHORT).show(); restartProcess(); }
        else start();
    }

    void restartProcess() {
        Intent i = new Intent(this, MainActivity.class);
        i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
        startActivity(i);
        android.os.Process.killProcess(android.os.Process.myPid());
    }

    void start() {
        view = new GLSurfaceView(this);
        view.setEGLContextClientVersion(2);
        view.setRenderer(this);
        controls = new ControlsView(this, settings, this) {
            @Override protected void onSizeChanged(int w, int h, int ow, int oh) {
                super.onSizeChanged(w, h, ow, oh);
                layoutScreens(w, h);
            }
        };
        if (settings.buttonMode == 2) controls.setButtonsVisible(false);
        FrameLayout root = new FrameLayout(this);
        root.addView(view);
        root.addView(controls);
        setContentView(root);
        hideBars();
        int rate = 44100;
        int min = AudioTrack.getMinBufferSize(rate, AudioFormat.CHANNEL_OUT_STEREO, AudioFormat.ENCODING_PCM_16BIT);
        track = new AudioTrack(AudioManager.STREAM_MUSIC, rate, AudioFormat.CHANNEL_OUT_STEREO, AudioFormat.ENCODING_PCM_16BIT, Math.max(min, 8192) * 2, AudioTrack.MODE_STREAM);
        track.play();
        audioThread = new Thread(new Runnable() { public void run() {
            short[] buf = new short[2048];
            while (!Thread.interrupted()) {
                int n = Native.audio(buf);
                if (n > 0) { if (settings.sound && !fast) track.write(buf, 0, n); }
                else try { Thread.sleep(4); } catch (InterruptedException e) { return; }
            }
        }});
        audioThread.start();
    }

    void hideBars() {
        getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_FULLSCREEN
                | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY | View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN);
    }

    @Override public void onWindowFocusChanged(boolean f) { super.onWindowFocusChanged(f); if (f) hideBars(); }

    /** Screens as large as the chosen layout allows; the pad is drawn over them. */
    void layoutScreens(int w, int h) {
        if (w == 0 || h == 0) return;
        float aspect = 256f / 192f;
        RectF top = new RectF(), bot = new RectF();
        int lay = settings.layout;
        if (lay == 0) lay = w > h ? 2 : 0;              // auto: landscape = main screen large
        else if (lay == 3) lay = 0;
        float band = 0;
        if (lay == 0) {                                  // stacked
            float sw = w, sh = sw / aspect;
            boolean strip = h > w && (controls == null || controls.visibleButtons);
            float room = strip ? h * 0.76f : h;          // portrait: keep a strip for the pad under the screens (not when it is hidden)
            if (sh * 2 > room) { sh = room / 2f; sw = sh * aspect; }
            float x = (w - sw) / 2, y = strip ? 0 : (h - sh * 2) / 2;
            top.set(x, y, x + sw, y + sh); bot.set(x, y + sh, x + sw, y + sh * 2);
            if (strip) band = bot.bottom;
        } else if (lay == 1) {                           // side by side
            float sw = w / 2f, sh = sw / aspect;
            if (sh > h) { sh = h; sw = sh * aspect; }
            float x = (w - sw * 2) / 2, y = h > w ? Math.max(0, (h - sh) * 0.15f) : (h - sh) / 2;
            top.set(x, y, x + sw, y + sh); bot.set(x + sw, y, x + sw * 2, y + sh);
        } else {                                         // main screen fills the height, the other fits the space left
            float th = h, tw = th * aspect;
            if (tw > w * 0.8f) { tw = w * 0.8f; th = tw / aspect; }
            float rw = w - tw, bw = rw, bh = bw / aspect;
            if (bh > h) { bh = h; bw = bh * aspect; }
            float y = 0;                                 // top-aligned like the small screen (a wide phone leaves room below)
            top.set(0, y, tw, y + th);
            float bx = tw + (rw - bw) / 2;
            bot.set(bx, 0, bx + bw, bh);                 // top of the right column; the buttons go below it
            if (settings.swap) { RectF t = top; top = bot; bot = t; }
            topRect = new float[]{top.left, top.top, top.width(), top.height()};
            bottomRect = new float[]{bot.left, bot.top, bot.width(), bot.height()};
            controls.setBottomScreen(bot);
            controls.setBand(-1);
            controls.setStrip(tw, bh);
            return;
        }
        if (settings.swap) { RectF t = top; top = bot; bot = t; }
        topRect = new float[]{top.left, top.top, top.width(), top.height()};
        bottomRect = new float[]{bot.left, bot.top, bot.width(), bot.height()};
        controls.setBottomScreen(bot);
        controls.setStrip(-1, 0);
        controls.setBand(band > 0 && h - band > Math.min(w, h) * 0.25f ? band : -1);
    }

    void padUsed() {
        if (controls != null && settings.buttonMode == 0) runOnUiThread(new Runnable() { public void run() { controls.setButtonsVisible(false); } });
    }

    // ---------- GL ----------
    @Override public void onSurfaceCreated(GL10 gl, EGLConfig c) {
        if (!ready) {
            File hd = new File(getExternalFilesDir(null), "hd");
            ready = Native.init(rom.getAbsolutePath(), getFilesDir().getAbsolutePath(), hd.getAbsolutePath());
            if (ready) Native.setHd(settings.hd);
            if (ready && autoState.exists()) Native.loadState(autoState.getAbsolutePath());
            if (!ready) runOnUiThread(new Runnable() { public void run() { Toast.makeText(MainActivity.this, "롬을 열지 못했습니다", Toast.LENGTH_LONG).show(); } });
        }
    }

    @Override public void onSurfaceChanged(GL10 gl, int w, int h) { Native.surface(w, h); }

    @Override public void onDrawFrame(GL10 gl) {
        Native.input(touchButtons | keyButtons | axisButtons, touching, touchX, touchY);
        long now = System.nanoTime();
        if (last == 0) last = now;
        double speed = fast ? settings.fastSpeed : 1;
        owed += (now - last) * 59.8261 * speed / 1e9; last = now;
        int cap = (int) Math.max(3, speed * 3);
        int n = (int) Math.min(owed, cap); owed -= n; if (owed > cap) owed = 0;
        Native.frame(ready && !paused ? n : 0, topRect, bottomRect, settings.filter);
        int d = Native.rumble(rumbleEvent);           // PC: only at normal speed
        if (d >= 0 && (d == 0 || (settings.rumble && !fast && (rumbleEvent[2] == 0 || settings.rumbleBeam))))
            Haptics.rumble(rumbleEvent[0], rumbleEvent[1], d, settings.rumbleStrength);
    }

    // ---------- on-screen pad ----------
    @Override public void controls(int buttons, int t, int x, int y) { touchButtons = buttons; touching = t; touchX = x; touchY = y; }
    @Override public void fastForward(boolean on) { fast = on; }
    @Override public void openMenu() { showMenu(); }
    @Override public void buttonsShown(boolean v) { if (controls != null && controls.getWidth() > 0) relayout(); }

    // ---------- menu ----------
    void showMenu() {
        paused = true;
        final String[] items = {"빠른 저장…", "빠른 불러오기…", "화면 방향: " + Settings.ORIENTATIONS[settings.orientation], "화면 배치: " + Settings.LAYOUTS[settings.layout],
                "위·아래 화면 바꾸기: " + onOff(settings.swap), "HD 그림: " + (Native.hdReady() || !settings.hd ? onOff(settings.hd) : "팩 없음"), "화면 필터: " + Settings.FILTERS[settings.filter],
                "화면 버튼: " + Settings.BUTTON_MODES[settings.buttonMode], "버튼 크기: " + Math.round(settings.size * 100) + "%",
                "버튼 투명도: " + Math.round(settings.opacity * 100) + "%", "빨리 감기 배속: " + settings.fastSpeed + "배",
                "진동: " + onOff(settings.vibrate), "전투 진동: " + onOff(settings.rumble), "전투 진동 세기: " + settings.rumbleStrength + "%", "빔 진동: " + onOff(settings.rumbleBeam), "소리: " + onOff(settings.sound), "게임 리셋", "롬 다시 고르기", "패드 단축키 설정…"};
        new AlertDialog.Builder(this, android.R.style.Theme_DeviceDefault_Dialog_Alert).setTitle("SRW W HD")
            .setItems(items, new DialogInterface.OnClickListener() { public void onClick(DialogInterface d, int i) { menuPick(i); } })
            .setOnCancelListener(new DialogInterface.OnCancelListener() { public void onCancel(DialogInterface d) { resumeGame(); } })
            .setNegativeButton("게임으로", new DialogInterface.OnClickListener() { public void onClick(DialogInterface d, int i) { resumeGame(); } })
            .show();
    }

    static String onOff(boolean b) { return b ? "켜짐" : "꺼짐"; }

    void resumeGame() { paused = false; last = 0; owed = 0; hideBars(); }

    void menuPick(int i) {
        switch (i) {
            case 0: slots(true); return;
            case 1: slots(false); return;
            case 2: choose("화면 방향", Settings.ORIENTATIONS, settings.orientation, new Pick() { public void pick(int k) { settings.orientation = k; applyOrientation(); } }); return;
            case 3: choose("화면 배치", Settings.LAYOUTS, settings.layout, new Pick() { public void pick(int k) { settings.layout = k; relayout(); } }); return;
            case 4: settings.swap = !settings.swap; relayout(); break;
            case 5: settings.hd = !settings.hd; final boolean on = settings.hd; view.queueEvent(new Runnable() { public void run() { Native.setHd(on); } }); break;
            case 6: choose("화면 필터", Settings.FILTERS, settings.filter, new Pick() { public void pick(int k) { settings.filter = k; } }); return;
            case 7: choose("화면 버튼", Settings.BUTTON_MODES, settings.buttonMode, new Pick() { public void pick(int k) { settings.buttonMode = k; controls.setButtonsVisible(k != 2); } }); return;
            case 8: choose("버튼 크기", new String[]{"80%", "90%", "100%", "115%", "130%"}, idx(settings.size, new float[]{0.8f, 0.9f, 1f, 1.15f, 1.3f}),
                    new Pick() { public void pick(int k) { settings.size = new float[]{0.8f, 0.9f, 1f, 1.15f, 1.3f}[k]; controls.place(controls.getWidth(), controls.getHeight()); } }); return;
            case 9: choose("버튼 투명도", new String[]{"15%", "25%", "35%", "50%", "65%"}, idx(settings.opacity, new float[]{0.15f, 0.25f, 0.35f, 0.5f, 0.65f}),
                    new Pick() { public void pick(int k) { settings.opacity = new float[]{0.15f, 0.25f, 0.35f, 0.5f, 0.65f}[k]; controls.invalidate(); } }); return;
            case 10: choose("빨리 감기 배속", new String[]{"2배", "3배", "4배", "6배"}, idx(settings.fastSpeed, new float[]{2, 3, 4, 6}),
                    new Pick() { public void pick(int k) { settings.fastSpeed = new int[]{2, 3, 4, 6}[k]; } }); return;
            case 11: settings.vibrate = !settings.vibrate; break;
            case 12: settings.rumble = !settings.rumble; break;
            case 13: choose("전투 진동 세기", new String[]{"25%", "45%", "65%", "85%", "100%"}, idx(settings.rumbleStrength, new float[]{25, 45, 65, 85, 100}),
                    new Pick() { public void pick(int k) { settings.rumbleStrength = new int[]{25, 45, 65, 85, 100}[k]; Haptics.rumble(1, 1, 180, settings.rumbleStrength); } }); return;
            case 14: settings.rumbleBeam = !settings.rumbleBeam; break;
            case 15: settings.sound = !settings.sound; break;
            case 16: view.queueEvent(new Runnable() { public void run() { Native.reset(); } }); break;
            case 17: settings.save(); pickRom(); return;
            case 18: shortcutList(); return;
        }
        settings.save();
        resumeGame();
    }

    interface Pick { void pick(int k); }

    void choose(String title, String[] opts, int cur, final Pick p) {
        new AlertDialog.Builder(this, android.R.style.Theme_DeviceDefault_Dialog_Alert).setTitle(title)
            .setSingleChoiceItems(opts, cur, new DialogInterface.OnClickListener() { public void onClick(DialogInterface d, int k) {
                p.pick(k); settings.save(); d.dismiss(); resumeGame(); } })
            .setOnCancelListener(new DialogInterface.OnCancelListener() { public void onCancel(DialogInterface d) { resumeGame(); } })
            .show();
    }

    static int idx(float v, float[] a) { int best = 0; for (int i = 1; i < a.length; i++) if (Math.abs(a[i] - v) < Math.abs(a[best] - v)) best = i; return best; }

    void applyOrientation() {
        setRequestedOrientation(settings.orientation == 1 ? android.content.pm.ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
                : settings.orientation == 2 ? android.content.pm.ActivityInfo.SCREEN_ORIENTATION_SENSOR_PORTRAIT
                : android.content.pm.ActivityInfo.SCREEN_ORIENTATION_FULL_SENSOR);
    }

    void relayout() { layoutScreens(controls.getWidth(), controls.getHeight()); }

    void slots(final boolean save) {
        final String[] names = new String[3];
        java.text.DateFormat f = java.text.DateFormat.getDateTimeInstance(java.text.DateFormat.SHORT, java.text.DateFormat.SHORT);
        for (int k = 0; k < 3; k++) {
            File s = slot(k);
            names[k] = "슬롯 " + (k + 1) + "  —  " + (s.exists() ? f.format(new java.util.Date(s.lastModified())) : "비어 있음");
        }
        new AlertDialog.Builder(this, android.R.style.Theme_DeviceDefault_Dialog_Alert).setTitle(save ? "빠른 저장" : "빠른 불러오기")
            .setItems(names, new DialogInterface.OnClickListener() { public void onClick(DialogInterface d, final int k) {
                final File s = slot(k);
                if (!save && !s.exists()) { Toast.makeText(MainActivity.this, "비어 있는 슬롯입니다", Toast.LENGTH_SHORT).show(); resumeGame(); return; }
                view.queueEvent(new Runnable() { public void run() {
                    final boolean ok = save ? Native.saveState(s.getAbsolutePath()) : Native.loadState(s.getAbsolutePath());
                    runOnUiThread(new Runnable() { public void run() {
                        Toast.makeText(MainActivity.this, (save ? "저장" : "불러오기") + (ok ? " 완료: 슬롯 " : " 실패: 슬롯 ") + (k + 1), Toast.LENGTH_SHORT).show(); } });
                } });
                resumeGame(); } })
            .setOnCancelListener(new DialogInterface.OnCancelListener() { public void onCancel(DialogInterface d) { resumeGame(); } })
            .show();
    }

    /** Quick save/load to slot 1 without opening the menu. */
    void quick(final boolean save) {
        final File s = slot(0);
        if (!save && !s.exists()) { Toast.makeText(this, "슬롯 1이 비어 있습니다", Toast.LENGTH_SHORT).show(); return; }
        view.queueEvent(new Runnable() { public void run() {
            final boolean ok = save ? Native.saveState(s.getAbsolutePath()) : Native.loadState(s.getAbsolutePath());
            runOnUiThread(new Runnable() { public void run() {
                if (ok && settings.vibrate && controls != null) controls.haptics.confirm();
                Toast.makeText(MainActivity.this, (save ? "상태 저장" : "상태 불러오기") + (ok ? " 완료 (슬롯 1)" : " 실패"), Toast.LENGTH_SHORT).show(); } });
        } });
    }

    File slot(int k) { return new File(getFilesDir(), "slot" + (k + 1) + ".state"); }

    // ---------- game pads and keyboards ----------
    static int keyButton(int code) {
        switch (code) {
            case KeyEvent.KEYCODE_DPAD_UP: return UP;
            case KeyEvent.KEYCODE_DPAD_DOWN: return DOWN;
            case KeyEvent.KEYCODE_DPAD_LEFT: return LEFT;
            case KeyEvent.KEYCODE_DPAD_RIGHT: return RIGHT;
            case KeyEvent.KEYCODE_BUTTON_A: return A;
            case KeyEvent.KEYCODE_BUTTON_B: return B;
            case KeyEvent.KEYCODE_BUTTON_X: return X;
            case KeyEvent.KEYCODE_BUTTON_Y: return Y;
            case KeyEvent.KEYCODE_BUTTON_L1: return L;
            case KeyEvent.KEYCODE_BUTTON_R1: return R;
            case KeyEvent.KEYCODE_BUTTON_START: case KeyEvent.KEYCODE_ENTER: return START;
            case KeyEvent.KEYCODE_BUTTON_SELECT: case KeyEvent.KEYCODE_SPACE: return SELECT;
            case KeyEvent.KEYCODE_Z: return A;
            case KeyEvent.KEYCODE_X: return B;
            case KeyEvent.KEYCODE_C: return X;
            case KeyEvent.KEYCODE_V: return Y;
            case KeyEvent.KEYCODE_A: return L;
            case KeyEvent.KEYCODE_S: return R;
            default: return -1;
        }
    }

    static boolean fromPad(int source) {
        return (source & InputDevice.SOURCE_GAMEPAD) == InputDevice.SOURCE_GAMEPAD || (source & InputDevice.SOURCE_JOYSTICK) == InputDevice.SOURCE_JOYSTICK;
    }

    // ---------- pad shortcuts (remappable in the menu) ----------
    static final int SC_MENU = 0, SC_SWAP = 1, SC_FAST = 2, SC_SAVE = 3, SC_LOAD = 4;
    static final String[] SC_NAMES = {"메뉴 열기", "주·보조 화면 바꾸기", "빨리 감기 (누르는 동안)", "빠른 저장 (슬롯 1)", "빠른 불러오기 (슬롯 1)"};
    final java.util.HashSet<Integer> held = new java.util.HashSet<>(), usedMod = new java.util.HashSet<>(), taken = new java.util.HashSet<>();

    /** L3 and R3 are separate buttons (only R3 swaps the screens by default); a pad that reports its right stick
     *  click as THUMBL can be remapped in the shortcut menu. */
    static int norm(int code) { return code; }

    static String keyName(int code) {
        switch (code) {
            case 0: return "";
            case KeyEvent.KEYCODE_BUTTON_A: return "A"; case KeyEvent.KEYCODE_BUTTON_B: return "B";
            case KeyEvent.KEYCODE_BUTTON_X: return "X"; case KeyEvent.KEYCODE_BUTTON_Y: return "Y";
            case KeyEvent.KEYCODE_BUTTON_L1: return "L1"; case KeyEvent.KEYCODE_BUTTON_R1: return "R1";
            case KeyEvent.KEYCODE_BUTTON_L2: return "L2"; case KeyEvent.KEYCODE_BUTTON_R2: return "R2";
            case KeyEvent.KEYCODE_BUTTON_THUMBL: return "L3"; case KeyEvent.KEYCODE_BUTTON_THUMBR: return "R3";
            case KeyEvent.KEYCODE_BUTTON_START: return "START"; case KeyEvent.KEYCODE_BUTTON_SELECT: return "SELECT";
            case KeyEvent.KEYCODE_BUTTON_MODE: return "홈";
            case KeyEvent.KEYCODE_DPAD_UP: return "↑"; case KeyEvent.KEYCODE_DPAD_DOWN: return "↓";
            case KeyEvent.KEYCODE_DPAD_LEFT: return "←"; case KeyEvent.KEYCODE_DPAD_RIGHT: return "→";
            default: return KeyEvent.keyCodeToString(code).replace("KEYCODE_", "").replace("BUTTON_", "");
        }
    }

    String binding(int i) { return settings.scMod[i] != 0 ? keyName(settings.scMod[i]) + " + " + keyName(settings.scKey[i]) : settings.scKey[i] != 0 ? keyName(settings.scKey[i]) : "없음"; }

    boolean isModifier(int code) { for (int m : settings.scMod) if (m != 0 && m == code) return true; return false; }

    void fire(int i, boolean down) {
        if (i == SC_FAST) { fastKey = down; fast = fastKey || tabFast; return; }
        if (!down) return;
        switch (i) {
            case SC_MENU: showMenu(); break;
            case SC_SWAP: settings.swap = !settings.swap; relayout(); settings.save(); break;
            case SC_SAVE: quick(true); break;
            case SC_LOAD: quick(false); break;
        }
    }

    /** Pad button (or trigger) for the shortcuts; true when it is used up and must not reach the game.
     *  A modifier button's own action fires when it is released without a combination (R3 tap). */
    boolean shortcutKey(int code, boolean down) {
        code = norm(code);
        boolean mod = isModifier(code), game = keyButton(code) >= 0;
        if (down) {
            if (held.contains(code)) return taken.contains(code) || (mod && !game);      // key repeat / key + axis twins
            held.add(code);
            for (int i = 0; i < settings.scKey.length; i++)
                if (settings.scMod[i] != 0 && settings.scKey[i] == code && held.contains(settings.scMod[i])) {
                    usedMod.add(settings.scMod[i]); taken.add(code); fire(i, true); return true;
                }
            if (mod) { usedMod.remove(code); return !game; }
            for (int i = 0; i < settings.scKey.length; i++)
                if (settings.scMod[i] == 0 && settings.scKey[i] == code) { taken.add(code); fire(i, true); return true; }
            return false;
        }
        if (!held.remove(code)) return taken.contains(code) || (mod && !game);
        if (taken.remove(code)) { for (int i = 0; i < settings.scKey.length; i++) if (settings.scKey[i] == code) fire(i, false); return true; }
        if (mod) {
            if (!usedMod.remove(code))
                for (int i = 0; i < settings.scKey.length; i++) if (settings.scMod[i] == 0 && settings.scKey[i] == code && i != SC_FAST) fire(i, true);
            return !game;
        }
        return false;
    }

    void shortcutList() {
        String[] items = new String[SC_NAMES.length + 1];
        for (int i = 0; i < SC_NAMES.length; i++) items[i] = SC_NAMES[i] + ":  " + binding(i);
        items[SC_NAMES.length] = "기본값으로 되돌리기";
        new AlertDialog.Builder(this, android.R.style.Theme_DeviceDefault_Dialog_Alert).setTitle("패드 단축키 설정")
            .setItems(items, new DialogInterface.OnClickListener() { public void onClick(DialogInterface d, int k) {
                if (k == SC_NAMES.length) {
                    settings.scMod = Settings.SC_MOD_DEFAULT.clone(); settings.scKey = Settings.SC_KEY_DEFAULT.clone(); settings.save();
                    Toast.makeText(MainActivity.this, "기본값으로 되돌렸습니다", Toast.LENGTH_SHORT).show(); shortcutList();
                } else captureShortcut(k); } })
            .setOnCancelListener(new DialogInterface.OnCancelListener() { public void onCancel(DialogInterface d) { resumeGame(); } })
            .setNegativeButton("게임으로", new DialogInterface.OnClickListener() { public void onClick(DialogInterface d, int i) { resumeGame(); } })
            .show();
    }

    /** Waits for one pad button, or two (hold the first, press the second), and binds it to action `which`. */
    void captureShortcut(final int which) {
        held.clear(); usedMod.clear(); taken.clear(); fastKey = false; fast = tabFast;
        final AlertDialog d = new AlertDialog(this, android.R.style.Theme_DeviceDefault_Dialog_Alert) {
            int first; float lt, rt;
            void press(int code, boolean down) {
                code = norm(code);
                if (down) { if (first == 0) first = code; else if (code != first) { assign(which, first, code); dismiss(); } }
                else if (code == first) { assign(which, 0, code); dismiss(); }
            }
            @Override public boolean dispatchKeyEvent(KeyEvent e) {
                int c = e.getKeyCode(); boolean pad = fromPad(e.getSource());
                if (!pad && (c == KeyEvent.KEYCODE_BACK || c == KeyEvent.KEYCODE_ESCAPE)) return super.dispatchKeyEvent(e);
                if (c == KeyEvent.KEYCODE_DPAD_CENTER && pad) return true;
                if (e.getRepeatCount() == 0) press(c, e.getAction() == KeyEvent.ACTION_DOWN);
                return true;
            }
            @Override public boolean dispatchGenericMotionEvent(MotionEvent e) {
                if (!fromPad(e.getSource())) return super.dispatchGenericMotionEvent(e);
                float l = Math.max(e.getAxisValue(MotionEvent.AXIS_LTRIGGER), e.getAxisValue(MotionEvent.AXIS_BRAKE));
                float r = Math.max(e.getAxisValue(MotionEvent.AXIS_RTRIGGER), e.getAxisValue(MotionEvent.AXIS_GAS));
                if ((l > 0.5f) != (lt > 0.5f)) press(KeyEvent.KEYCODE_BUTTON_L2, l > 0.5f);
                if ((r > 0.5f) != (rt > 0.5f)) press(KeyEvent.KEYCODE_BUTTON_R2, r > 0.5f);
                lt = l; rt = r;
                return true;
            }
        };
        d.setTitle(SC_NAMES[which] + "  (지금: " + binding(which) + ")");
        d.setMessage("지정할 패드 버튼을 누르세요.\n두 버튼 조합: 첫 버튼을 누른 채로 두 번째 버튼을 누르세요.");
        d.setButton(DialogInterface.BUTTON_NEGATIVE, "취소", new DialogInterface.OnClickListener() { public void onClick(DialogInterface x, int i) { } });
        d.setOnDismissListener(new DialogInterface.OnDismissListener() { public void onDismiss(DialogInterface x) { shortcutList(); } });
        d.show();
    }

    void assign(int which, int mod, int key) {
        if (mod == 0 && keyButton(key) >= 0) {
            Toast.makeText(this, keyName(key) + " 버튼은 게임 조작에 쓰여서 혼자 지정할 수 없습니다. 다른 버튼과 조합해 주세요.", Toast.LENGTH_LONG).show();
            return;
        }
        for (int i = 0; i < settings.scKey.length; i++)                // the action that had this binding takes the old one
            if (i != which && settings.scMod[i] == mod && settings.scKey[i] == key) { settings.scMod[i] = settings.scMod[which]; settings.scKey[i] = settings.scKey[which]; }
        settings.scMod[which] = mod; settings.scKey[which] = key; settings.save();
        Toast.makeText(this, SC_NAMES[which] + ": " + binding(which), Toast.LENGTH_SHORT).show();
    }

    @Override public boolean dispatchKeyEvent(KeyEvent e) {
        int code = e.getKeyCode();
        boolean pad = fromPad(e.getSource());
        if (code == KeyEvent.KEYCODE_BACK && !pad) { if (e.getAction() == KeyEvent.ACTION_UP) showMenu(); return true; }
        boolean down = e.getAction() == KeyEvent.ACTION_DOWN;
        if (code == KeyEvent.KEYCODE_TAB) { tabFast = down; fast = fastKey || tabFast; return true; }   // keyboard: fast-forward
        if (code == KeyEvent.KEYCODE_DPAD_CENTER && pad) return true;
        if (pad && shortcutKey(code, down)) return true;
        if (code == KeyEvent.KEYCODE_BUTTON_MODE || code == KeyEvent.KEYCODE_ESCAPE
                || (code == KeyEvent.KEYCODE_BACK && pad)) {
            if (down && e.getRepeatCount() == 0) showMenu();
            return true;
        }
        int b = keyButton(code);
        if (b < 0) return super.dispatchKeyEvent(e);
        if (down) keyButtons |= 1 << b; else keyButtons &= ~(1 << b);
        if (pad || (e.getSource() & InputDevice.SOURCE_DPAD) == InputDevice.SOURCE_DPAD) padUsed();
        return true;
    }

    @Override public boolean dispatchGenericMotionEvent(MotionEvent e) {
        if (!fromPad(e.getSource()) || e.getAction() != MotionEvent.ACTION_MOVE) return super.dispatchGenericMotionEvent(e);
        float hx = e.getAxisValue(MotionEvent.AXIS_HAT_X), hy = e.getAxisValue(MotionEvent.AXIS_HAT_Y);
        float sx = e.getAxisValue(MotionEvent.AXIS_X), sy = e.getAxisValue(MotionEvent.AXIS_Y);
        float lt = Math.max(e.getAxisValue(MotionEvent.AXIS_LTRIGGER), e.getAxisValue(MotionEvent.AXIS_BRAKE));
        float rt = Math.max(e.getAxisValue(MotionEvent.AXIS_RTRIGGER), e.getAxisValue(MotionEvent.AXIS_GAS));
        int b = 0;
        if (hx < -0.5f || sx < -0.5f) b |= 1 << LEFT;
        if (hx > 0.5f || sx > 0.5f) b |= 1 << RIGHT;
        if (hy < -0.5f || sy < -0.5f) b |= 1 << UP;
        if (hy > 0.5f || sy > 0.5f) b |= 1 << DOWN;
        boolean l2 = lt > 0.5f, r2 = rt > 0.5f;     // analog triggers count as the L2 / R2 buttons for the shortcuts
        if (l2 != l2Axis) { l2Axis = l2; shortcutKey(KeyEvent.KEYCODE_BUTTON_L2, l2); }
        if (r2 != r2Axis) { r2Axis = r2; shortcutKey(KeyEvent.KEYCODE_BUTTON_R2, r2); }
        if (b != 0 || r2) padUsed();
        axisButtons = b;
        return true;
    }

    // ---------- lifecycle ----------
    @Override protected void onPause() {
        super.onPause();
        paused = true;
        if (view != null) {
            view.queueEvent(new Runnable() { public void run() { if (ready) Native.saveState(autoState.getAbsolutePath()); } });
            view.onPause();
        }
        if (track != null) track.pause();
    }

    @Override protected void onResume() {
        super.onResume();
        if (view != null) view.onResume();
        if (track != null) track.play();
        paused = false; last = 0; owed = 0;
    }

    @Override protected void onDestroy() {
        if (audioThread != null) audioThread.interrupt();
        super.onDestroy();
    }
}

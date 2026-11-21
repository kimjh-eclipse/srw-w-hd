package kr.srww.hd;

import android.content.Context;
import android.content.SharedPreferences;

/** User options, kept in SharedPreferences. */
final class Settings {
    static final String[] LAYOUTS = {"자동 (세로: 위아래, 가로: 주 화면 크게)", "나란히", "주 화면 크게", "위아래 (항상)"};
    static final String[] ORIENTATIONS = {"자동 (기기 방향)", "가로 고정", "세로 고정"};
    static final String[] BUTTON_MODES = {"자동 (패드 쓰면 숨김)", "항상 보이기", "숨기기"};

    int layout = 0;           // 0 auto (portrait stacked, landscape main large), 1 side by side, 2 main large, 3 stacked
    int orientation = 0;      // 0 sensor, 1 landscape, 2 portrait
    boolean swap;             // bottom screen where the top screen would be
    static final String[] FILTERS = {"선명하게 (원본 픽셀)", "부드럽게", "xBRZ 4배"};
    int filter = 2;           // 0 sharp, 1 bilinear, 2 xBRZ 4x
    int buttonMode = 0;       // see BUTTON_MODES
    float opacity = 0.35f;    // on-screen buttons
    float size = 1.0f;        // on-screen buttons scale
    boolean vibrate = true;
    boolean sound = true;
    int fastSpeed = 3;        // fast-forward multiplier
    boolean hd = true;        // HD parts composition
    boolean rumble = true;    // battle rumble on the pad (PC defaults: on, 65, beams on)
    int rumbleStrength = 65;
    boolean rumbleBeam = true;

    private final SharedPreferences p;

    Settings(Context c) {
        p = c.getSharedPreferences("settings", Context.MODE_PRIVATE);
        layout = p.getInt("layout", layout);
        orientation = p.getInt("orientation", orientation);
        swap = p.getBoolean("swap", swap);
        filter = p.getInt("filter", filter);
        buttonMode = p.getInt("buttonMode", buttonMode);
        opacity = p.getFloat("opacity", opacity);
        size = p.getFloat("size", size);
        vibrate = p.getBoolean("vibrate", vibrate);
        sound = p.getBoolean("sound", sound);
        fastSpeed = p.getInt("fastSpeed", fastSpeed);
        hd = p.getBoolean("hd", hd);
        rumble = p.getBoolean("rumble", rumble);
        rumbleStrength = p.getInt("rumbleStrength", rumbleStrength);
        rumbleBeam = p.getBoolean("rumbleBeam", rumbleBeam);
    }

    void save() {
        p.edit().putInt("layout", layout).putInt("orientation", orientation).putBoolean("swap", swap).putInt("filter", filter)
                .putInt("buttonMode", buttonMode).putFloat("opacity", opacity).putFloat("size", size)
                .putBoolean("vibrate", vibrate).putBoolean("sound", sound).putInt("fastSpeed", fastSpeed).putBoolean("hd", hd).putBoolean("rumble", rumble).putInt("rumbleStrength", rumbleStrength).putBoolean("rumbleBeam", rumbleBeam).apply();
    }
}

package kr.srww.hd;

import android.content.Context;
import android.os.Build;
import android.os.CombinedVibration;
import android.os.VibrationAttributes;
import android.os.VibrationEffect;
import android.os.Vibrator;
import android.os.VibratorManager;
import android.util.Log;
import android.view.InputDevice;

/** Short vibration: the device's own vibrator when Android reports one, otherwise the rumble of a
 *  connected game pad (InputDevice vibrator, Android 12+). Needs android.permission.VIBRATE.
 *  On TB710FU Android reports no device vibrator (hasVibrator false); the Sony pad has one. */
final class Haptics {
    private final Vibrator device;

    Haptics(Context c) {
        Vibrator v;
        if (Build.VERSION.SDK_INT >= 31) v = ((VibratorManager) c.getSystemService(Context.VIBRATOR_MANAGER_SERVICE)).getDefaultVibrator();
        else v = (Vibrator) c.getSystemService(Context.VIBRATOR_SERVICE);
        device = v != null && v.hasVibrator() ? v : null;
        Log.i("srwwhd", "device vibrator " + (device != null ? "present" : "missing") + ", pad vibrator " + (pad() != null ? "present" : "missing"));
    }

    /** first connected game pad that has a vibrator */
    static VibratorManager pad() {
        if (!padEnabled) return null;
        if (Build.VERSION.SDK_INT < 31) return null;
        for (int id : InputDevice.getDeviceIds()) {
            InputDevice d = InputDevice.getDevice(id);
            if (d == null || d.isVirtual()) continue;
            int s = d.getSources();
            if ((s & InputDevice.SOURCE_GAMEPAD) != InputDevice.SOURCE_GAMEPAD && (s & InputDevice.SOURCE_JOYSTICK) != InputDevice.SOURCE_JOYSTICK) continue;
            VibratorManager m = d.getVibratorManager();
            if (m.getVibratorIds().length > 0) return m;
        }
        return null;
    }

    /** on-screen button press */
    void tap() { buzz(25, 120); }

    /** confirmation (quick save / load): always the pad if there is one */
    void confirm() { padBuzz(120, 200); }

    private void buzz(int ms, int amplitude) {
        if (device != null) {
            try {
                if (Build.VERSION.SDK_INT >= 33)
                    device.vibrate(VibrationEffect.createOneShot(ms, VibrationEffect.DEFAULT_AMPLITUDE),
                            new VibrationAttributes.Builder().setUsage(VibrationAttributes.USAGE_MEDIA).build());
                else if (Build.VERSION.SDK_INT >= 26) device.vibrate(VibrationEffect.createOneShot(ms, VibrationEffect.DEFAULT_AMPLITUDE));
                else device.vibrate(ms);
                return;
            } catch (RuntimeException e) { Log.w("srwwhd", "vibrate failed: " + e); }
        }
        padBuzz(ms, amplitude);
    }

    /** Battle rumble (PC player_rumble.PadRumble): two pad motors, low = heavy, high = light.
     *  gain = strength/100, duration clamped to 20..600 ms; duration 0 stops. */
    static void rumble(float low, float high, int duration, int strength) {
        if (!padEnabled || Build.VERSION.SDK_INT < 31) return;
        try {
            VibratorManager m = pad();
            if (m == null) return;
            if (duration <= 0 || strength <= 0) { m.cancel(); return; }
            float gain = Math.max(0, Math.min(100, strength)) / 100f;
            int ms = Math.max(20, Math.min(600, duration));
            int[] ids = m.getVibratorIds();
            int a = Math.max(1, Math.min(255, Math.round(Math.max(0, Math.min(1, low * gain)) * 255)));
            int b = Math.max(1, Math.min(255, Math.round(Math.max(0, Math.min(1, high * gain)) * 255)));
            if (ids.length >= 2) {
                m.vibrate(CombinedVibration.startParallel()
                        .addVibrator(ids[0], VibrationEffect.createOneShot(ms, a))
                        .addVibrator(ids[1], VibrationEffect.createOneShot(ms, b)).combine());
            } else m.vibrate(CombinedVibration.createParallel(VibrationEffect.createOneShot(ms, Math.max(a, b))));
        } catch (RuntimeException e) { Log.w("srwwhd", "rumble failed: " + e); }
    }

    /** On. (11/21: the DS4 also dropped its link with this switched off, so rumble was not the cause.) */
    static boolean padEnabled = true;

    private static void padBuzz(int ms, int amplitude) {
        if (!padEnabled || Build.VERSION.SDK_INT < 31) return;
        try {
            VibratorManager m = pad();
            if (m != null) m.vibrate(CombinedVibration.createParallel(VibrationEffect.createOneShot(ms, amplitude)));
        } catch (RuntimeException e) { Log.w("srwwhd", "pad vibrate failed: " + e); }
    }
}

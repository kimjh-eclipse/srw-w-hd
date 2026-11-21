package kr.srww.hd;

import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Rect;
import android.graphics.Typeface;

/** HD lettering for recognised DS glyphs (called from native code on the GL thread).
 *  Same shaping rules as emulator/hd_fonts.FontRenderer._glyph_shape: bold face, size = cell height x
 *  .92 (compact HUD figures) / .80 (selected buttons) / .94 (text), a 1px dark outline except on
 *  buttons, ink box centred in the cell (punctuation sits on the line of a full-height character),
 *  squeezed to the cell width when wider. The PC uses Malgun Gothic; Android uses the system Korean
 *  font (it may not be shipped with the app). */
final class Glyphs {
    private static final Paint base = new Paint(Paint.ANTI_ALIAS_FLAG | Paint.SUBPIXEL_TEXT_FLAG);
    static { base.setTypeface(Typeface.create(Typeface.SANS_SERIF, Typeface.BOLD)); base.setTextSize(48); base.setColor(0xffffffff); }
    private static final String BASELINE_MARKS = ",.。．，_";

    static boolean has(String s) {
        for (int i = 0; i < s.length(); ) {
            int cp = s.codePointAt(i); i += Character.charCount(cp);
            if (Character.isWhitespace(cp)) continue;
            if (!base.hasGlyph(new String(Character.toChars(cp)))) return false;
        }
        return s.length() > 0;
    }

    /** returns w*h*2 bytes: luminance = fill coverage, alpha = fill or outline coverage */
    static byte[] render(String s, int w, int h, int mode) {
        boolean compact = (mode & 1) != 0, button = (mode & 2) != 0;
        Paint p = new Paint(base);
        p.setTextSize(Math.max(6, Math.round(h * (compact ? .92f : button ? .80f : .94f))));
        int stroke = button ? 0 : Math.max(1, h / 45);
        Rect box = new Rect(); p.getTextBounds(s, 0, s.length(), box);
        Rect ref = box;
        if (BASELINE_MARKS.contains(s)) { ref = new Rect(); p.getTextBounds("가", 0, 1, ref); }
        int rw = Math.max(w, box.width() + 2 * stroke + 2);
        float x = (rw - box.width()) / 2 - box.left, y = (h - ref.height()) / 2 - ref.top;
        Bitmap fill = Bitmap.createBitmap(rw, h, Bitmap.Config.ARGB_8888), line = null;
        p.setStyle(Paint.Style.FILL); new Canvas(fill).drawText(s, x, y, p);
        if (stroke > 0) {
            line = Bitmap.createBitmap(rw, h, Bitmap.Config.ARGB_8888);
            p.setStyle(Paint.Style.FILL_AND_STROKE); p.setStrokeWidth(2 * stroke); p.setStrokeJoin(Paint.Join.ROUND);
            new Canvas(line).drawText(s, x, y, p);
        }
        if (rw != w) {
            fill = Bitmap.createScaledBitmap(fill, w, h, true);
            if (line != null) line = Bitmap.createScaledBitmap(line, w, h, true);
        }
        int[] f = new int[w * h], o = line != null ? new int[w * h] : null;
        fill.getPixels(f, 0, w, 0, 0, w, h);
        if (o != null) line.getPixels(o, 0, w, 0, 0, w, h);
        byte[] out = new byte[w * h * 2];
        for (int i = 0; i < w * h; i++) {
            int a = f[i] >>> 24, b = o != null ? Math.max(a, o[i] >>> 24) : a;
            out[i * 2] = (byte) a; out[i * 2 + 1] = (byte) b;
        }
        return out;
    }
}

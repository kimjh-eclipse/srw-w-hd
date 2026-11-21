package kr.srww.hd;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.RectF;
import android.view.HapticFeedbackConstants;
import android.view.MotionEvent;
import android.view.View;

/** Translucent on-screen pad drawn OVER the game: D-pad (8 directions), A/B/X/Y, L/R, SELECT/START,
 *  fast-forward and menu. Touches on the bottom DS screen that miss every button go to the game. */
public class ControlsView extends View {
    interface Listener {
        void controls(int buttons, int touching, int x, int y);
        void fastForward(boolean on);
        void openMenu();
        void buttonsShown(boolean visible);
    }

    static final int B = 0, Y = 1, SELECT = 2, START = 3, UP = 4, DOWN = 5, LEFT = 6, RIGHT = 7, A = 8, X = 9, L = 10, R = 11;

    final Listener listener;
    final Settings settings;
    final Haptics haptics;
    final Paint fill = new Paint(Paint.ANTI_ALIAS_FLAG), edge = new Paint(Paint.ANTI_ALIAS_FLAG), text = new Paint(Paint.ANTI_ALIAS_FLAG);
    RectF bottomScreen = new RectF();
    float padX, padY, padR, unit;
    final float[][] face = new float[4][3];
    final int[] faceId = {A, B, X, Y};
    final String[] faceLabel = {"A", "B", "X", "Y"};
    final RectF lRect = new RectF(), rRect = new RectF(), selRect = new RectF(), startRect = new RectF(), ffRect = new RectF(), menuRect = new RectF();
    int buttons, lastButtons;
    boolean ff, menuDown, visibleButtons = true;

    public ControlsView(Context c, Settings s, Listener l) {
        super(c);
        settings = s; listener = l; haptics = new Haptics(c);
        edge.setStyle(Paint.Style.STROKE);
        text.setTextAlign(Paint.Align.CENTER);
        text.setFakeBoldText(true);
    }

    float bandTop = -1;                          // portrait: top of the free strip under the screens, -1 = overlay only
    float stripLeft = -1, stripTop = 0;          // landscape main-large: free column right of the main screen, below the small screen
    void setStrip(float left, float top) { if (left != stripLeft || top != stripTop) { stripLeft = left; stripTop = top; place(getWidth(), getHeight()); } }
    void setBottomScreen(RectF r) { bottomScreen = r; }
    void setBand(float top) { if (top != bandTop) { bandTop = top; place(getWidth(), getHeight()); } }
    void setButtonsVisible(boolean v) { if (v != visibleButtons) { visibleButtons = v; invalidate(); listener.buttonsShown(v); } }

    @Override protected void onSizeChanged(int w, int h, int ow, int oh) { super.onSizeChanged(w, h, ow, oh); place(w, h); }

    void place(int w, int h) {
        float u = Math.min(w, h) / 9f * settings.size;
        unit = u;
        float m = u * 0.35f;                                  // margin from the edges
        padR = u * 1.35f;
        padX = m + padR; padY = h - m - padR - u * 0.2f;
        if (bandTop > 0) {                            // controls sit in the strip under the screens
            float band = h - bandTop;
            u = Math.min(u, band / 4.2f); unit = u; m = u * 0.35f; padR = u * 1.35f;
            padX = m + padR; padY = bandTop + u * 0.95f + (band - u * 0.95f - u * 0.8f) / 2;
        }
        float d = u * 0.95f, r = u * 0.5f;
        float fx = w - m - d - r, fy = padY;
        face[0] = new float[]{fx + d, fy, r}; face[1] = new float[]{fx, fy + d, r};
        face[2] = new float[]{fx, fy - d, r}; face[3] = new float[]{fx - d, fy, r};
        float sh = u * 0.6f, top = bandTop > 0 ? bandTop + u * 0.2f : padY - padR - u * 1.15f;
        lRect.set(m, top, m + u * 2.4f, top + sh);
        rRect.set(w - m - u * 2.4f, top, w - m, top + sh);
        float by = h - m - u * 0.55f;
        selRect.set(w / 2f - u * 1.9f, by, w / 2f - u * 0.2f, by + u * 0.55f);
        startRect.set(w / 2f + u * 0.2f, by, w / 2f + u * 1.9f, by + u * 0.55f);
        float s = u * 0.75f;
        menuRect.set(w - m - s, m, w - m, m + s);
        ffRect.set(w - m - s * 2.3f, m, w - m - s * 1.2f, m + s);
        if (stripLeft > 0 && w - stripLeft > 0) {     // right column: menu row, R, face buttons, SELECT/START
            float sw = w - stripLeft, sx = stripLeft, avail = h - stripTop;
            float uf = Math.min(u, Math.min(sw / 3.1f, avail / 5.4f)), mf = uf * 0.3f, cx = sx + sw / 2;
            float y = stripTop + mf, s2 = uf * 0.75f;
            ffRect.set(cx - s2 * 1.15f, y, cx - s2 * 0.05f, y + s2); menuRect.set(cx + s2 * 0.15f, y, cx + s2 * 1.25f, y + s2);
            y += s2 + mf;
            rRect.set(sx + mf, y, sx + sw - mf, y + uf * 0.6f); y += uf * 0.6f + mf;
            float df = uf * 0.95f, rf = uf * 0.5f, fy2 = y + df + rf;
            face[0] = new float[]{cx + df, fy2, rf}; face[1] = new float[]{cx, fy2 + df, rf};
            face[2] = new float[]{cx, fy2 - df, rf}; face[3] = new float[]{cx - df, fy2, rf};
            float by2 = h - mf - uf * 0.55f;
            selRect.set(sx + mf, by2, cx - mf / 2, by2 + uf * 0.55f); startRect.set(cx + mf / 2, by2, sx + sw - mf, by2 + uf * 0.55f);
        }
        text.setTextSize(u * 0.42f);
        edge.setStrokeWidth(Math.max(2f, u / 30f));
        invalidate();
    }

    boolean on(int b) { return (buttons >> b & 1) != 0; }

    void style(boolean pressed) {
        int a = (int) (255 * Math.min(1f, settings.opacity * (pressed ? 2.0f : 1f)));
        fill.setColor((Math.min(255, a) << 24) | (pressed ? 0xffffff : 0x202838));
        edge.setColor((Math.min(255, (int) (a * 1.8f)) << 24) | 0xffffff);
        text.setColor((Math.min(255, (int) (a * 2.4f)) << 24) | 0xffffff);
    }

    @Override protected void onDraw(Canvas c) {
        // menu and fast-forward are always shown (small), the pad only when buttons are visible
        style(menuDown); round(c, menuRect, "≡");
        style(ff); round(c, ffRect, "▶▶");
        if (!visibleButtons) return;
        float a = padR, t = padR * 0.36f;
        style(false); c.drawCircle(padX, padY, padR * 1.08f, fill);
        arm(c, padX - t, padY - a, padX + t, padY - t, on(UP), 0);
        arm(c, padX - t, padY + t, padX + t, padY + a, on(DOWN), 180);
        arm(c, padX - a, padY - t, padX - t, padY + t, on(LEFT), 270);
        arm(c, padX + t, padY - t, padX + a, padY + t, on(RIGHT), 90);
        for (int i = 0; i < 4; i++) {
            style(on(faceId[i]));
            c.drawCircle(face[i][0], face[i][1], face[i][2], fill);
            c.drawCircle(face[i][0], face[i][1], face[i][2], edge);
            c.drawText(faceLabel[i], face[i][0], face[i][1] + text.getTextSize() * 0.36f, text);
        }
        style(on(L)); pill(c, lRect, "L"); style(on(R)); pill(c, rRect, "R");
        style(on(SELECT)); pill(c, selRect, "SELECT"); style(on(START)); pill(c, startRect, "START");
    }

    void arm(Canvas c, float l, float t, float r, float b, boolean pressed, int rot) {
        style(pressed);
        float rad = Math.min(r - l, b - t) * 0.18f;
        c.drawRoundRect(l, t, r, b, rad, rad, fill);
        // arrow
        float cx = (l + r) / 2, cy = (t + b) / 2, s = Math.min(r - l, b - t) * 0.22f;
        c.save(); c.rotate(rot, cx, cy);
        Path p = new Path(); p.moveTo(cx, cy - s); p.lineTo(cx + s, cy + s * 0.7f); p.lineTo(cx - s, cy + s * 0.7f); p.close();
        Paint ap = new Paint(text); ap.setStyle(Paint.Style.FILL); c.drawPath(p, ap);
        c.restore();
    }

    void pill(Canvas c, RectF r, String label) {
        float rad = r.height() / 2;
        c.drawRoundRect(r, rad, rad, fill); c.drawRoundRect(r, rad, rad, edge);
        float s = text.getTextSize(); text.setTextSize(Math.min(s, r.height() * 0.5f));
        c.drawText(label, r.centerX(), r.centerY() + text.getTextSize() * 0.36f, text);
        text.setTextSize(s);
    }

    void round(Canvas c, RectF r, String label) {
        float rad = r.height() * 0.3f;
        c.drawRoundRect(r, rad, rad, fill); c.drawRoundRect(r, rad, rad, edge);
        float s = text.getTextSize(); text.setTextSize(r.height() * 0.45f);
        c.drawText(label, r.centerX(), r.centerY() + text.getTextSize() * 0.36f, text);
        text.setTextSize(s);
    }

    @Override public boolean onTouchEvent(MotionEvent e) {
        int b = 0, touching = 0, tx = 0, ty = 0;
        boolean ffNow = false, menuNow = false;
        int act = e.getActionMasked();
        if (!visibleButtons && act == MotionEvent.ACTION_DOWN && !bottomScreen.contains(e.getX(), e.getY())
                && !menuRect.contains(e.getX(), e.getY()) && !ffRect.contains(e.getX(), e.getY()) && settings.buttonMode == 0) {
            setButtonsVisible(true);                   // auto mode: a touch away from the game brings the pad back
        }
        for (int p = 0; p < e.getPointerCount(); p++) {
            if (act == MotionEvent.ACTION_CANCEL) break;
            if ((act == MotionEvent.ACTION_UP || act == MotionEvent.ACTION_POINTER_UP) && p == e.getActionIndex()) continue;
            float x = e.getX(p), y = e.getY(p);
            if (grow(menuRect).contains(x, y)) { menuNow = true; continue; }
            if (grow(ffRect).contains(x, y)) { ffNow = true; continue; }
            if (visibleButtons) {
                float dx = x - padX, dy = y - padY, d = (float) Math.hypot(dx, dy);
                if (d < padR * 1.3f) {
                    if (d > padR * 0.18f) {
                        double ang = Math.toDegrees(Math.atan2(-dy, dx)); if (ang < 0) ang += 360;
                        switch ((int) Math.round(ang / 45) % 8) {
                            case 0: b |= 1 << RIGHT; break; case 1: b |= 1 << RIGHT | 1 << UP; break;
                            case 2: b |= 1 << UP; break;    case 3: b |= 1 << UP | 1 << LEFT; break;
                            case 4: b |= 1 << LEFT; break;  case 5: b |= 1 << LEFT | 1 << DOWN; break;
                            case 6: b |= 1 << DOWN; break;  case 7: b |= 1 << DOWN | 1 << RIGHT; break;
                        }
                    }
                    continue;
                }
                boolean hit = false;
                for (int i = 0; i < 4; i++) {
                    float fx = x - face[i][0], fy = y - face[i][1];
                    if (fx * fx + fy * fy < face[i][2] * face[i][2] * 1.7f) { b |= 1 << faceId[i]; hit = true; }
                }
                if (hit) continue;
                if (grow(lRect).contains(x, y)) { b |= 1 << L; continue; }
                if (grow(rRect).contains(x, y)) { b |= 1 << R; continue; }
                if (grow(selRect).contains(x, y)) { b |= 1 << SELECT; continue; }
                if (grow(startRect).contains(x, y)) { b |= 1 << START; continue; }
            }
            RectF s = bottomScreen;
            if (s.width() > 0 && s.contains(x, y)) {
                touching = 1;
                tx = Math.round(((x - s.left) / s.width() * 2 - 1) * 32767);
                ty = Math.round(((y - s.top) / s.height() * 2 - 1) * 32767);
            }
        }
        boolean changed = b != lastButtons || ffNow != ff || menuNow != menuDown;
        if (settings.vibrate && ((b & ~lastButtons) != 0 || (ffNow && !ff) || (menuNow && !menuDown)))
            haptics.tap();
        if (menuDown && !menuNow) listener.openMenu();
        if (ffNow != ff) listener.fastForward(ffNow);
        buttons = b; lastButtons = b; ff = ffNow; menuDown = menuNow;
        if (changed) invalidate();
        listener.controls(b, touching, tx, ty);
        return true;
    }

    RectF grow(RectF r) { float m = unit * 0.15f; return new RectF(r.left - m, r.top - m, r.right + m, r.bottom + m); }
}

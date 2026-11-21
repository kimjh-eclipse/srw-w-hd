"""Opt-in switches for judging the original robot sprites against the HD paint.

SRWW_ROBOT_SPRITE_HD=0
    Robot OBJ bindings of graphics/kazuma_parts_library.json are not
    registered with the core, so the core draws those sprites natively
    (SRWWHD_ShouldSkipRobot only skips a sprite that has a binding).
    Runtime assembly of unknown OBJ rectangles is switched off as well,
    otherwise the unbound robot sprites would come back as assembled HD.
    Effects, secondary (mini) units and menu/UI bindings stay HD.

SRWW_NATIVE_OBJ_FILTER=xbrz
    The native OBJ pixels of the top screen are upscaled with xBRZ 4x
    (tools/xbrz_compare.dll, DeSmuME's bundled xBRZ 1.4) instead of nearest.
    BG, cut-ins and UI keep their present path.

Both default to the current behaviour (robot HD on, no filter).
"""
import os

UI_ATLASES = ('favorite_menu',)
UI_ATLAS_PREFIXES = ('start_menu',)


def robot_sprite_hd():
    return os.environ.get('SRWW_ROBOT_SPRITE_HD', '1') != '0'


def native_obj_filter():
    value = os.environ.get('SRWW_NATIVE_OBJ_FILTER', '').strip().lower()
    return value if value in ('xbrz',) else None


def _resolved(bindings, identifier, key):
    """Field value following source_binding aliases (first explicit value wins)."""
    seen = set()
    while isinstance(identifier, int) and 0 < identifier <= len(bindings) and identifier not in seen:
        seen.add(identifier)
        spec = bindings[identifier - 1]
        if key in spec:
            return spec[key]
        identifier = spec.get('source_binding')
    return None


def classify(bindings):
    """Return (robot_ids, reasons) for 1-based binding ids.

    Rule (fields only):
      kept HD (not robot): effect_part true (own or via source_binding),
        secondary_unit (own or via source), atlas_id 'favorite_menu' or
        'start_menu*' (UI), atlas_id 'effect*'.
      robot: every other OBJ binding - base Kazuma atlas, unit_* robot sets,
        all_batch_*, full_attack_*, registered_attack_bank parts and the named
        robot atlases (deathscythe_*, wing_primary, big_volfog_* ...).
    Disabled / rgb_enabled=false bindings are never registered anyway.
    """
    robot = set()
    reasons = {}
    for i, spec in enumerate(bindings, 1):
        atlas = spec.get('atlas_id') or _resolved(bindings, i, 'atlas_id') or 'base'
        if spec.get('disabled') or not spec.get('rgb_enabled', True):
            reasons['disabled'] = reasons.get('disabled', 0) + 1
            continue
        if _resolved(bindings, i, 'effect_part') is True:
            reason = 'effect_part'
        elif _resolved(bindings, i, 'secondary_unit'):
            reason = 'secondary_unit'
        elif atlas in UI_ATLASES or atlas.startswith(UI_ATLAS_PREFIXES):
            reason = 'ui_menu'
        elif atlas.startswith('effect'):
            reason = 'effect_atlas'
        else:
            reason = 'robot'
            robot.add(i)
        reasons[reason] = reasons.get(reason, 0) + 1
    return robot, reasons


def robot_ids(bindings, library_digest=None):
    """classify(bindings)[0], kept between starts.

    classify walks every binding (about a second for 110k); the answer only depends on the
    parts library and on this file, so it is stored next to the parts catalog cache under
    the library digest and this file's own digest. Any read/write problem falls back to
    computing it.
    """
    if not library_digest:
        return classify(bindings)[0]
    import hashlib, json, tempfile
    from pathlib import Path
    try:
        from runtime_paths import data_dir
        code = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        folder = data_dir() / 'cache'
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / 'robot-binding-ids.json'
    except OSError:
        return classify(bindings)[0]
    try:
        saved = json.loads(path.read_text())
        if saved['library'] == library_digest and saved['code'] == code and saved['count'] == len(bindings):
            return set(saved['ids'])
    except (OSError, ValueError, KeyError, TypeError):
        pass
    ids = classify(bindings)[0]
    temporary = None
    try:
        with tempfile.NamedTemporaryFile('w', dir=folder, suffix='.tmp', delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(dict(library=library_digest, code=code, count=len(bindings), ids=sorted(ids)), stream, separators=(',', ':'))
        temporary.replace(path)
    except OSError:
        pass
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return ids

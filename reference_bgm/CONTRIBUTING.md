# Contributing

## Ground rules

- Do not submit ROM images, ROM fragments, save files, extracted game assets,
  copyrighted music, Nintendo SDK material, or credentials.
- Keep changes compatible with the supported ROM hash unless a separate,
  fully verified revision profile is added.
- Preserve the MPL-2.0 notice in modified covered files.
- Explain behavioral changes and add or update tests when practical.
- Do not weaken ROM hash, original-byte, code-cave, size, or BPS roundtrip
  validation to make an unsupported build pass.

## Development check

```powershell
python -m unittest discover -s tests -v
python -m compileall -q .
```

ARM9 changes also require a successful build with devkitARM and emulator or
hardware regression testing. Reports should identify the BGM ID, transition,
emulator/version, audio settings, and exact reproduction steps without
attaching copyrighted inputs.

By contributing, you agree that your contribution is available under
MPL-2.0 and that you have the right to submit it.

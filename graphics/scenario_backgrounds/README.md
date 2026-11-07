# Scenario background and CG asset bank

The canonical Korean ROM scene bank contains **247 mapped images**: 141 scenario/intermission backgrounds and 106 story CG or geographic maps. The native references were decoded from their original PLT, IMG and SCR resources. Resource identity, palette linkage and native dimensions are in `catalog.json`.

`scenario_<SCR resource>_hd.png` is the runtime artwork. The matching `_native.png` remains the original pixel reference used by the emulator matcher. The native reference must not be replaced by generated art.

`coverage_all.json` reports actual file readiness, decoded dimensions, original and HD SHA-256 values, missing resources and the unchanged canonical ROM hash. `coverage.json` retains the original 141-background subset audit. `asset_lineage.json` connects individual resources with retained generated atlases and provenance manifests. `cg_batches.json` contains all 26 CG batches, and `cg_support_generation.json` retains the supporting agent's generation and localization records.

The nine geographic map labels are Korean. Other baked text localization is recorded in the CG manifests. Resource 4797 reuses the existing Earth-region HD map only after an exact native-reference comparison. The original uniform white scene 5099 and uniform black scene 5276 are deliberately preserved as uniform display textures.

Artwork is split from exact 2 by 2 or 1 by 2 atlas panels. Most textures are approximately 700 pixels wide to balance the displayed scene size and loading costs; no artwork is loaded synchronously by these asset preparation scripts. Runtime texture loading and matching are implemented separately by the emulator.

Recheck files and synchronize catalog readiness with:

```powershell
python -X utf8 emulator/audit_all_scenario_assets.py
```

The audit also overwrites the fixed CG contact sheets in `test_current/scenario_backgrounds/`. File readiness alone does not establish actual game coverage: registration and game verification remain separate fields and must come from runtime testing. No ROM copy or extra patch version is produced by this asset workflow.

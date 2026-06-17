# EMSWebTest

This repository contains NetAtlas EMS automated test assets.

## Projects

- `GlobalTest_20260616` - legacy pytest-based global EMS cases.
- `Olt140xConfigTest_20260616` - legacy OLT140x configuration cases.
- `ChassisConfigTest_260616` - legacy chassis configuration cases.
- `EMSNewCaseTest_20260616` - new pytest project for future automated cases.

The legacy projects are independent and should receive only basic maintenance. Do not add new test cases to the three legacy folders. Modify a legacy folder only when explicitly requested for a small maintenance change.

Add all new automated test cases under `EMSNewCaseTest_20260616`.

When a new test needs logic from a legacy project, copy the required file or helper into `EMSNewCaseTest_20260616` and maintain it there. Do not import modules directly from the legacy folders.

## Reference Documents

- `NetAtlasEMS_UserGuide.pdf` - EMS operation guide.
- `TestPlan_NetAtlasEMS-20260615.xlsx` - full EMS test plan and automation target list.

## GitHub Upload Notes

This folder is not currently initialized as a Git repository. To upload all four project folders and the reference documents to GitHub, initialize the repository, add a remote, commit, and push:

```powershell
git init
git add README.md .gitignore NetAtlasEMS_UserGuide.pdf TestPlan_NetAtlasEMS-20260615.xlsx GlobalTest_20260616 Olt140xConfigTest_20260616 ChassisConfigTest_260616 EMSNewCaseTest_20260616
git commit -m "Add EMS web test projects"
git branch -M main
git remote add origin <GITHUB_REPOSITORY_URL>
git push -u origin main
```

Before the first upload, review whether runtime artifacts such as reports, downloads, logs, drivers, and local credentials should be excluded or kept.

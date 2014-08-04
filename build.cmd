@echo off
rem If unable to find project.json, keep going up a directory (maximum of 3) till project.json is found
if exist project.json (
	kpm build
) else (
	cd ..
	if exist project.json (
		kpm build
	) else (
		cd ..
		if exist project.json (
			kpm build
		)
	)
)
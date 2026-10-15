param(
    [string]$WorkspaceRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$PythonExecutable = "python"
)

$sourceRoot = Join-Path $WorkspaceRoot "GlobalTest_20260616"
$newCaseSourceRoot = Join-Path $WorkspaceRoot "EMSNewCaseTest_20260616"
$targetRoot = Join-Path $WorkspaceRoot "GlobalCase"
$sourceFiles = @("Icat.py", "Restful.py", "Provision.py", "Unicase.py")
$newCaseFiles = Get-ChildItem -LiteralPath (Join-Path $newCaseSourceRoot "tests") -Filter "test_ems1_*.py" | Sort-Object Name
$forcedSkipCases = @("test_EMS1_7214_deviceStatusDown")
$excludedPythonFiles = @(
    "ClickTest.py", "commonPrf.py", "Configuration.py", "e2e.py", "forFail.py",
    "maxPm.py", "maxPrf.py", "maxUsr.py", "model_0614.py", "prfApply.py",
    "sessionTest.py", "Test.py", "Test3.py"
)
$excludedProjectFiles = @(
    "environment_parameterBackup.json", "env_pmtest.json", "geckodriver.log",
    "pmconfig.json", "README.docx", "USER_RUN_GUIDE.md",
    "Web_EMS_ICAT.list", "Web_EMS_ICAT_emsVer_2024-07-18_17-29-41.txt",
    "Web_EMS_Profile.list", "Web_EMS_Provision.list", "Web_EMS_Restful.list",
    "Web_EMS_Unicase.list"
)

if (-not (Test-Path -LiteralPath $targetRoot)) {
    New-Item -ItemType Directory -Path $targetRoot | Out-Null
}

$excludedDirectories = @(".pytest_cache", ".vs", "__pycache__", "download", "report")
Get-ChildItem -LiteralPath $sourceRoot -Force | Where-Object {
    $_.Name -notin $excludedDirectories `
        -and $_.Name -notin $excludedPythonFiles `
        -and $_.Name -notin $excludedProjectFiles
} | ForEach-Object {
    $targetItem = Join-Path $targetRoot $_.Name
    if ($_.PSIsContainer -or -not (Test-Path -LiteralPath $targetItem)) {
        Copy-Item -LiteralPath $_.FullName -Destination $targetRoot -Recurse -Force
    }
}

$mergedPath = Join-Path $targetRoot "GlobalCase.py"
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$mergedParts = [System.Collections.Generic.List[string]]::new()
$mergedParts.Add("# Generated from Icat.py, Restful.py, Provision.py, and Unicase.py.")
$mergedParts.Add("# Source projects are read-only; rebuild this file from copies only.")

foreach ($sourceFile in $sourceFiles) {
    $sourcePath = Join-Path $sourceRoot $sourceFile
    $marker = [System.IO.Path]::GetFileNameWithoutExtension($sourceFile)
    $content = [System.IO.File]::ReadAllText($sourcePath)
    $pattern = '(?m)^(\s+)((?:async\s+)?def\s+test_EMS1_)'
    $replacement = "`$1@pytest.mark.$marker`r`n`$1`$2"
    $content = [regex]::Replace($content, $pattern, $replacement)
    $disallowedMarkerPattern = '(?m)^\s+@pytest\.mark\.(?!(?:Restful|Icat|Provision|Unicase|skip|asyncio)(?:\s|\(|$))[^\r\n]*\r?\n'
    $content = [regex]::Replace($content, $disallowedMarkerPattern, "")
    $sourceClass = "Test$marker"
    $mixinClass = "_${marker}Cases"
    $content = $content -replace "class $sourceClass\(\):", "class $mixinClass():"
    $fixturePattern = '(?m)^\s+@pytest\.fixture\(autouse=True, scope="(?:class|function)"\)\r?\n(?=\s+def\s+(?:_inject_config|setup_browser))'
    $content = [regex]::Replace($content, $fixturePattern, "")
    $mergedParts.Add("`r`n# ===== Source: $sourceFile =====`r`n")
    $mergedParts.Add($content)
}

# Copy the standalone helper modules required by EMSNewCaseTest cases.
$targetLibRoot = Join-Path $targetRoot "libs"
Get-ChildItem -LiteralPath (Join-Path $newCaseSourceRoot "libs") -File -Filter "*.py" | Where-Object {
    $_.Name -ne "__init__.py"
} | ForEach-Object {
    $targetHelper = Join-Path $targetLibRoot $_.Name
    if (-not (Test-Path -LiteralPath $targetHelper)) {
        Copy-Item -LiteralPath $_.FullName -Destination $targetHelper
    }
}

# GlobalCase unregisters an ONT by its configured AID. Keep this overlay here
# so the read-only EMSNewCaseTest source project is never modified.
$deviceCliPath = Join-Path $targetLibRoot "device_cli.py"
$deviceCliContent = [System.IO.File]::ReadAllText($deviceCliPath)
$unregisterPattern = '(?s)def unregister_ont_by_flag\(host, username, password, ont_flag, sn, registration_password=None, port=22, timeout=60\):.*?(?=\r?\n    client = paramiko\.SSHClient\(\))'
$unregisterReplacement = @'
def unregister_ont_by_flag(host, username, password, ont_flag, slot_id, port_id, ont_id, port=22, timeout=60):
    """Remove ONT remote interface on the DUT so EMS sees it as unregistered."""
    import paramiko

    flag = (ont_flag or "").strip().lower()
    if not all(str(value).strip() for value in (slot_id, port_id, ont_id)):
        raise ValueError(
            f"Missing ONT AID fields: slot={slot_id!r}, port={port_id!r}, ont={ont_id!r}"
        )
    if flag == "xont":
        delete_command = f"no interface remote xont {slot_id}-{port_id}-{ont_id}"
    elif flag == "ont":
        delete_command = f"no interface remote ont {slot_id}-{port_id}-{ont_id}"
    elif flag == "ont-14":
        delete_command = f"no remote ont ont-{port_id}-{ont_id}"
    else:
        raise ValueError(f"Unsupported ONT flag: {ont_flag!r}")
    commands = ["configure", delete_command, "exit"]
'@
$deviceCliContent = [regex]::Replace(
    $deviceCliContent,
    $unregisterPattern,
    $unregisterReplacement,
    1
)
[System.IO.File]::WriteAllText($deviceCliPath, $deviceCliContent, $utf8NoBom)

# Close the ONT Service Result modal before later actions (such as Filter).
$emsTablesPath = Join-Path $targetLibRoot "ems_tables.py"
$emsTablesContent = [System.IO.File]::ReadAllText($emsTablesPath)
$serviceResultClosePattern = '(?s)    _click_first_present\(\r?\n        driver,\r?\n        \[\r?\n            \(By\.ID, "alarm_detail_close_btn"\),\r?\n            \(By\.CSS_SELECTOR, "#alarm_clear_note_dialog \.close"\),\r?\n            \(By\.CSS_SELECTOR, "#alarm_clear_note_dialog button"\),\r?\n        \],\r?\n    \)\r?\n    return detail'
$serviceResultCloseReplacement = @'
    modal_locator = (By.ID, "provision_service_result_modal")
    close_locators = [
        (By.XPATH, "//*[@id='provision_service_result_modal']//*[self::button or self::input][normalize-space()='Close' or @value='Close']"),
        (By.CSS_SELECTOR, "#provision_service_result_modal [data-dismiss='modal']"),
        (By.CSS_SELECTOR, "#provision_service_result_modal .close"),
        (By.CSS_SELECTOR, "#provision_service_result_modal .button"),
    ]

    for _ in range(3):
        if EC.invisibility_of_element_located(modal_locator)(driver):
            break
        for by, value in close_locators:
            visible_elements = [
                element
                for element in driver.find_elements(by, value)
                if element.is_displayed() and element.is_enabled()
            ]
            for element in visible_elements:
                try:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                    element.click()
                except (ElementClickInterceptedException, StaleElementReferenceException):
                    try:
                        driver.execute_script("arguments[0].click();", element)
                    except StaleElementReferenceException:
                        continue
                try:
                    WebDriverWait(driver, 5).until(
                        EC.invisibility_of_element_located(modal_locator)
                    )
                    break
                except TimeoutException:
                    continue
            if EC.invisibility_of_element_located(modal_locator)(driver):
                break
        if not EC.invisibility_of_element_located(modal_locator)(driver):
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            time.sleep(1)

    assert EC.invisibility_of_element_located(modal_locator)(driver), (
        "#provision_service_result_modal remained visible after Close retries"
    )
    return detail
'@
$emsTablesContent = [regex]::Replace(
    $emsTablesContent,
    $serviceResultClosePattern,
    $serviceResultCloseReplacement,
    1
)
[System.IO.File]::WriteAllText($emsTablesPath, $emsTablesContent, $utf8NoBom)

# Overlay GlobalCase-only helper changes without modifying either source project.
$globalCaseLibRoot = Join-Path $PSScriptRoot "global_case_libs"
Get-ChildItem -LiteralPath $globalCaseLibRoot -File -Filter "*.py" | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $targetLibRoot $_.Name) -Force
}
Copy-Item -LiteralPath (Join-Path $newCaseSourceRoot "environment_parameter.json") `
    -Destination (Join-Path $targetRoot "new_case_environment_parameter.json") -Force

# Preserve the Markdown documentation from EMSNewCaseTest without replacing
# GlobalCase's own run guide.
$targetDocsRoot = Join-Path $targetRoot "docs"
if (-not (Test-Path -LiteralPath $targetDocsRoot)) {
    New-Item -ItemType Directory -Path $targetDocsRoot | Out-Null
}
Get-ChildItem -LiteralPath (Join-Path $newCaseSourceRoot "docs") -File -Filter "*.md" | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $targetDocsRoot -Force
}
Copy-Item -LiteralPath (Join-Path $newCaseSourceRoot "README.md") `
    -Destination (Join-Path $targetRoot "EMSNewCaseTest_20260616_README.md") -Force
Copy-Item -LiteralPath (Join-Path $newCaseSourceRoot "USER_RUN_GUIDE.md") `
    -Destination (Join-Path $targetRoot "EMSNewCaseTest_20260616_USER_RUN_GUIDE.md") -Force

$newMixinClasses = [System.Collections.Generic.List[string]]::new()
$newCaseMapEntries = [System.Collections.Generic.List[string]]::new()
$newCaseNumber = 0
foreach ($newCaseFile in $newCaseFiles) {
    $newCaseNumber++
    $caseId = "{0:D2}" -f $newCaseNumber
    $mixinClass = "_NewCase${caseId}Cases"
    $helperPrefix = "_newcase_${caseId}_"
    $content = [System.IO.File]::ReadAllText($newCaseFile.FullName)
    $content = $content.Replace(
        "unregister_ont_by_flag(self.dutIp, self.dutAdminName, self.dutAdminPwd, flag, sn, password)",
        "unregister_ont_by_flag(self.dutIp, self.dutAdminName, self.dutAdminPwd, flag, self.serviceOntSlotID, self.serviceOntPortID, self.serviceOntID)"
    )
    $content = $content.Replace(
        "unregister_ont_by_flag(self.dutIp, self.dutAdminName, self.dutAdminPwd, self.serviceOntFlag, sn, password)",
        "unregister_ont_by_flag(self.dutIp, self.dutAdminName, self.dutAdminPwd, self.serviceOntFlag, self.serviceOntSlotID, self.serviceOntPortID, self.serviceOntID)"
    )

    # These two standalone classes both used self.statuses. After merging them
    # into one MRO, the earlier mixin's class attribute shadows the later one.
    if ($newCaseFile.Name -eq "test_ems1_6089_device_status_sort.py") {
        $content = $content.Replace("    statuses =", "    device_statuses =")
        $content = $content.Replace("self.statuses", "self.device_statuses")
    }
    elseif ($newCaseFile.Name -eq "test_ems1_7065_7066_7068_ethernet_access_port_status.py") {
        $content = $content.Replace("    statuses =", "    ethernet_access_statuses =")
        $content = $content.Replace("self.statuses", "self.ethernet_access_statuses")
    }

    # New standalone cases are individual/unified cases, so they join Unicase.
    $content = [regex]::Replace(
        $content,
        '(?m)^(\s+)((?:async\s+)?def\s+test_EMS1_)',
        "`$1@pytest.mark.Unicase`r`n`$1`$2"
    )
    foreach ($forcedSkipCase in $forcedSkipCases) {
        $content = [regex]::Replace(
            $content,
            "(?m)^(\s+)(?=(?:async\s+)?def\s+$forcedSkipCase\s*\()",
            "`$1@pytest.mark.skip`r`n`$1"
        )
    }
    $content = [regex]::Replace(
        $content,
        '(?m)^\s+@pytest\.mark\.(?!(?:Restful|Icat|Provision|Unicase|skip|asyncio)(?:\s|\(|$))[^\r\n]*\r?\n',
        ""
    )
    $content = [regex]::Replace($content, '(?m)^@pytest\.mark\.[^\r\n]*\r?\n', "")
    $content = [regex]::Replace(
        $content,
        '(?m)^\s+@pytest\.fixture\(autouse=True(?:,\s*scope="(?:class|function)")?\)\r?\n(?=\s+def\s+setup_browser)',
        ""
    )
    $content = [regex]::new('(?m)^class\s+Test\w+(?:\([^)]*\))?:').Replace($content, "class ${mixinClass}:", 1)

    $helperNames = [regex]::Matches($content, '(?m)^    def\s+(?<name>(?!test_EMS1_)\w+)\s*\(') |
        ForEach-Object { $_.Groups["name"].Value } | Select-Object -Unique
    foreach ($helperName in $helperNames) {
        $renamedHelper = $helperPrefix + $helperName
        $content = [regex]::Replace($content, "(?m)^(    def\s+)$helperName(?=\s*\()", "`$1$renamedHelper")
        $content = [regex]::Replace($content, "(?<=self\.)$helperName\b", $renamedHelper)
    }

    $testNames = [regex]::Matches($content, '(?m)^    (?:async\s+)?def\s+(?<name>test_EMS1_\w+)\s*\(') |
        ForEach-Object { $_.Groups["name"].Value }
    foreach ($testName in $testNames) {
        $newCaseMapEntries.Add("        `"$testName`": ($mixinClass, `"${helperPrefix}setup_browser`"),")
    }

    $newMixinClasses.Add($mixinClass)
    $mergedParts.Add("`r`n# ===== Source: EMSNewCaseTest_20260616/$($newCaseFile.Name) =====`r`n")
    $mergedParts.Add($content)
}

$mergedParts.Add("`r`nfrom libs.ems_map import assert_ont_dashboard_ddmi_charts_valid, map_tree_node_order_groups, map_tree_node_order_key, ont_dashboard_ddmi_chart_data`r`n")
$mergedParts.Add("from libs.ems_power_supply import capture_restful_debug_files, power_supply_image_states`r`n")
$mergedParts.Add(@'

class _CustomCases:

    @pytest.mark.Unicase
    def test_ontFullService_192_168_168_85_5A5958458CBCA751(self):
        """Copy of serviceExport setup: configure one ONT and retain its service."""
        target_ip = "192.168.168.85"
        target_sn = "5A5958458CBCA751"
        # Read existing names once per profile type; never rely on current page order.
        existing_profiles = {}
        required_profiles = {
            "ONT QoS Bandwidth Profile": {
                prefix + str(i) for prefix in (
                    "$py_ONTQoSBandwidthFull85G", "$py_ONTQoSBandwidthFull85T",
                    "$py_newFull85G", "$py_newFull85T") for i in range(1, 17)
            },
            "ONT Service Profile": {"$py_ONTServiceFull85" + str(i) for i in range(1, 9)},
            "ONT Template": {"$py_TempONTServiceFull85"},
        }

        def profile_exists(_self, profile_type, profile_name):
            if profile_type not in existing_profiles:
                from libs.ems_tables import navigate_to
                navigate_to(self.driver, "Provision", "Profile")
                Select(self.driver.find_element(By.ID, "profile_filtertype")).select_by_visible_text(profile_type)
                time.sleep(3)
                if pageCount(self, "profile_table") > 1:
                    self.driver.find_element(By.CSS_SELECTOR, "#profile_table .first").click()
                    time.sleep(3)
                names = set()
                for _ in range(pageCount(self, "profile_table")):
                    names.update(self.driver.execute_script("""
                        const headers = Array.from(document.querySelectorAll('#profile_table_head th'));
                        const index = headers.findIndex(h => h.getAttribute('name') === 'Name');
                        if (index < 0) throw new Error('Profile name column missing');
                        return Array.from(document.querySelectorAll('#profile_table_body tbody tr'))
                            .map(row => row.cells[index].innerText.trim());
                    """))
                    if required_profiles[profile_type] <= names:
                        break
                    if pageCurrent(self, "profile_table") >= pageCount(self, "profile_table"):
                        break
                    self.driver.find_element(By.CSS_SELECTOR, "#profile_table .next").click()
                    time.sleep(3)
                existing_profiles[profile_type] = names
                found = len(required_profiles[profile_type] & names)
                print(f"Reuse {profile_type}: {found}/{len(required_profiles[profile_type])} profiles exist", flush=True)
            return profile_name in existing_profiles[profile_type]

        xponPirGem = 361600
        gponPirGem = -5760        
        xponPirTcont = 1808000
        gponPirTcont = -57600
        for indPrf in range (16):
            xponPirGem = 361600 + 102400 * (indPrf + 1)
            gponPirGem = -5760 + 15360 * (indPrf + 1)
            xponPirTcont = 1808000 + 512000 * (indPrf + 1)
            gponPirTcont = -57600 + 153600 * (indPrf + 1)
            #Create ONT QoS Bandwidth Profile: "$py_ONTQoSBandwidthFull85G"
            if not profile_exists (self, "ONT QoS Bandwidth Profile", "$py_ONTQoSBandwidthFull85G" + str(indPrf+1)):
                createProfile (self, "ONT QoS Bandwidth Profile", "$py_ONTQoSBandwidthFull85G" + str(indPrf+1))
                self.driver.find_element(By.NAME, "bwprofile_sir").send_keys(Keys.CONTROL + "a")
                self.driver.find_element(By.NAME, "bwprofile_sir").send_keys(Keys.DELETE) 
                self.driver.find_element(By.NAME, "bwprofile_sir").send_keys("0")
                self.driver.find_element(By.NAME, "bwprofile_air").send_keys(Keys.CONTROL + "a")
                self.driver.find_element(By.NAME, "bwprofile_air").send_keys(Keys.DELETE) 
                self.driver.find_element(By.NAME, "bwprofile_air").send_keys("0")
                self.driver.find_element(By.NAME, "bwprofile_pir").send_keys(Keys.CONTROL + "a")
                self.driver.find_element(By.NAME, "bwprofile_pir").send_keys(Keys.DELETE) 
                self.driver.find_element(By.NAME, "bwprofile_pir").send_keys(str(xponPirGem))
                self.driver.find_element(By.NAME, "bwprofile_gpon_sir").send_keys(Keys.CONTROL + "a")
                self.driver.find_element(By.NAME, "bwprofile_gpon_sir").send_keys(Keys.DELETE) 
                self.driver.find_element(By.NAME, "bwprofile_gpon_sir").send_keys("0")
                self.driver.find_element(By.NAME, "bwprofile_gpon_air").send_keys(Keys.CONTROL + "a")
                self.driver.find_element(By.NAME, "bwprofile_gpon_air").send_keys(Keys.DELETE) 
                self.driver.find_element(By.NAME, "bwprofile_gpon_air").send_keys("0")
                self.driver.find_element(By.NAME, "bwprofile_gpon_pir").send_keys(Keys.CONTROL + "a")
                self.driver.find_element(By.NAME, "bwprofile_gpon_pir").send_keys(Keys.DELETE)
                self.driver.find_element(By.NAME, "bwprofile_gpon_pir").send_keys(str(gponPirGem))
                saveProfile (self)
            #Create ONT QoS Bandwidth Profile: "$py_ONTQoSBandwidthFull85T"
            if not profile_exists (self, "ONT QoS Bandwidth Profile", "$py_ONTQoSBandwidthFull85T" + str(indPrf+1)):
                createProfile (self, "ONT QoS Bandwidth Profile", "$py_ONTQoSBandwidthFull85T" + str(indPrf+1))
                self.driver.find_element(By.NAME, "bwprofile_sir").send_keys(Keys.CONTROL + "a")
                self.driver.find_element(By.NAME, "bwprofile_sir").send_keys(Keys.DELETE) 
                self.driver.find_element(By.NAME, "bwprofile_sir").send_keys("0")
                self.driver.find_element(By.NAME, "bwprofile_air").send_keys(Keys.CONTROL + "a")
                self.driver.find_element(By.NAME, "bwprofile_air").send_keys(Keys.DELETE) 
                self.driver.find_element(By.NAME, "bwprofile_air").send_keys("0")
                self.driver.find_element(By.NAME, "bwprofile_pir").send_keys(Keys.CONTROL + "a")
                self.driver.find_element(By.NAME, "bwprofile_pir").send_keys(Keys.DELETE) 
                self.driver.find_element(By.NAME, "bwprofile_pir").send_keys(str(xponPirTcont))
                self.driver.find_element(By.NAME, "bwprofile_gpon_sir").send_keys(Keys.CONTROL + "a")
                self.driver.find_element(By.NAME, "bwprofile_gpon_sir").send_keys(Keys.DELETE) 
                self.driver.find_element(By.NAME, "bwprofile_gpon_sir").send_keys("0")
                self.driver.find_element(By.NAME, "bwprofile_gpon_air").send_keys(Keys.CONTROL + "a")
                self.driver.find_element(By.NAME, "bwprofile_gpon_air").send_keys(Keys.DELETE) 
                self.driver.find_element(By.NAME, "bwprofile_gpon_air").send_keys("0")
                self.driver.find_element(By.NAME, "bwprofile_gpon_pir").send_keys(Keys.CONTROL + "a")
                self.driver.find_element(By.NAME, "bwprofile_gpon_pir").send_keys(Keys.DELETE)
                self.driver.find_element(By.NAME, "bwprofile_gpon_pir").send_keys(str(gponPirTcont))
                saveProfile (self)
            #Create ONT QoS Bandwidth Profile: "$py_newFull85G"
            if not profile_exists (self, "ONT QoS Bandwidth Profile", "$py_newFull85G" + str(indPrf+1)):
                createProfile (self, "ONT QoS Bandwidth Profile", "$py_newFull85G" + str(indPrf+1))
                self.driver.find_element(By.NAME, "bwprofile_sir").send_keys(Keys.CONTROL + "a")
                self.driver.find_element(By.NAME, "bwprofile_sir").send_keys(Keys.DELETE) 
                self.driver.find_element(By.NAME, "bwprofile_sir").send_keys("0")
                self.driver.find_element(By.NAME, "bwprofile_air").send_keys(Keys.CONTROL + "a")
                self.driver.find_element(By.NAME, "bwprofile_air").send_keys(Keys.DELETE) 
                self.driver.find_element(By.NAME, "bwprofile_air").send_keys("0")
                self.driver.find_element(By.NAME, "bwprofile_pir").send_keys(Keys.CONTROL + "a")
                self.driver.find_element(By.NAME, "bwprofile_pir").send_keys(Keys.DELETE) 
                self.driver.find_element(By.NAME, "bwprofile_pir").send_keys(str(xponPirGem))
                self.driver.find_element(By.NAME, "bwprofile_gpon_sir").send_keys(Keys.CONTROL + "a")
                self.driver.find_element(By.NAME, "bwprofile_gpon_sir").send_keys(Keys.DELETE) 
                self.driver.find_element(By.NAME, "bwprofile_gpon_sir").send_keys("0")
                self.driver.find_element(By.NAME, "bwprofile_gpon_air").send_keys(Keys.CONTROL + "a")
                self.driver.find_element(By.NAME, "bwprofile_gpon_air").send_keys(Keys.DELETE) 
                self.driver.find_element(By.NAME, "bwprofile_gpon_air").send_keys("0")
                self.driver.find_element(By.NAME, "bwprofile_gpon_pir").send_keys(Keys.CONTROL + "a")
                self.driver.find_element(By.NAME, "bwprofile_gpon_pir").send_keys(Keys.DELETE)
                self.driver.find_element(By.NAME, "bwprofile_gpon_pir").send_keys(str(gponPirGem))
                saveProfile (self)
            #Create ONT QoS Bandwidth Profile: "$py_newFull85T"
            if not profile_exists (self, "ONT QoS Bandwidth Profile", "$py_newFull85T" + str(indPrf+1)):
                createProfile (self, "ONT QoS Bandwidth Profile", "$py_newFull85T" + str(indPrf+1))
                self.driver.find_element(By.NAME, "bwprofile_sir").send_keys(Keys.CONTROL + "a")
                self.driver.find_element(By.NAME, "bwprofile_sir").send_keys(Keys.DELETE) 
                self.driver.find_element(By.NAME, "bwprofile_sir").send_keys("0")
                self.driver.find_element(By.NAME, "bwprofile_air").send_keys(Keys.CONTROL + "a")
                self.driver.find_element(By.NAME, "bwprofile_air").send_keys(Keys.DELETE) 
                self.driver.find_element(By.NAME, "bwprofile_air").send_keys("0")
                self.driver.find_element(By.NAME, "bwprofile_pir").send_keys(Keys.CONTROL + "a")
                self.driver.find_element(By.NAME, "bwprofile_pir").send_keys(Keys.DELETE) 
                self.driver.find_element(By.NAME, "bwprofile_pir").send_keys(str(xponPirTcont))
                self.driver.find_element(By.NAME, "bwprofile_gpon_sir").send_keys(Keys.CONTROL + "a")
                self.driver.find_element(By.NAME, "bwprofile_gpon_sir").send_keys(Keys.DELETE) 
                self.driver.find_element(By.NAME, "bwprofile_gpon_sir").send_keys("0")
                self.driver.find_element(By.NAME, "bwprofile_gpon_air").send_keys(Keys.CONTROL + "a")
                self.driver.find_element(By.NAME, "bwprofile_gpon_air").send_keys(Keys.DELETE) 
                self.driver.find_element(By.NAME, "bwprofile_gpon_air").send_keys("0")
                self.driver.find_element(By.NAME, "bwprofile_gpon_pir").send_keys(Keys.CONTROL + "a")
                self.driver.find_element(By.NAME, "bwprofile_gpon_pir").send_keys(Keys.DELETE)
                self.driver.find_element(By.NAME, "bwprofile_gpon_pir").send_keys(str(gponPirTcont))
                saveProfile (self)
        #Create ONT Service Profile: "$py_ONTServiceFull85"
        for indPrf in range (8):
            if profile_exists (self, "ONT Service Profile", "$py_ONTServiceFull85" + str(indPrf+1)):
                continue
            createProfile (self, "ONT Service Profile", "$py_ONTServiceFull85" + str(indPrf+1))
            self.driver.find_element(By.ID, "ont_service_vlan_text").send_keys(str(indPrf+101))
            self.driver.find_element(By.XPATH, "//label[contains(.,\'Bridge\')]").click()
            self.driver.find_element(By.XPATH, "//label[contains(.,\'XLAN\')]").click()
            Select(self.driver.find_element(By.ID, "ont_service_xlan_combobox")).select_by_visible_text("XLAN " + str(indPrf+1))
            saveProfile (self)
        #Create ONT Template Profile: "$py_TempONTServiceFull85"
        if profile_exists (self, "ONT Template", "$py_TempONTServiceFull85")==False:
            createProfile (self, "ONT Template", "$py_TempONTServiceFull85")
            for ind in range (8):
                self.driver.find_element(By.XPATH, "//label[@for=\"ont_template_service_enable_checkbox" + str(ind + 1) + "\"]").click()
                selectProfile(self,"ont_template_service_combobox" + str(ind + 1), "$py_ONTServiceFull85" + str(ind + 1))
                Select(self.driver.find_element(By.ID, "ont_template_service_combobox" + str(ind + 1))).select_by_visible_text("$py_ONTServiceFull85" + str(ind + 1))
                Select(self.driver.find_element(By.ID, "ont_template_service_shared_combobox" + str(ind + 1))).select_by_visible_text(str(ind))
                selectProfile(self,"ont_template_service_us_bw_combobox" + str(ind + 1), "$py_ONTQoSBandwidthFull85G" + str(ind+1))
                Select(self.driver.find_element(By.ID, "ont_template_service_us_bw_combobox" + str(ind + 1))).select_by_visible_text("$py_ONTQoSBandwidthFull85G" + str(ind+1))
                selectProfile(self,"ont_template_service_ds_bw_combobox" + str(ind + 1), "$py_ONTQoSBandwidthFull85G" + str(ind+9))
                Select(self.driver.find_element(By.ID, "ont_template_service_ds_bw_combobox" + str(ind + 1))).select_by_visible_text("$py_ONTQoSBandwidthFull85G" + str(ind+9))
                self.driver.find_element(By.XPATH, "//label[@for=\"ont_template_tcont_enable_checkbox" + str(ind + 1) + "\"]").click()
                Select(self.driver.find_element(By.ID, "ont_template_tcont_combobox" + str(ind + 1))).select_by_visible_text(str(ind+1))
                selectProfile(self,"ont_template_tcont_us_bw_combobox" + str(ind + 1), "$py_ONTQoSBandwidthFull85T" + str(ind+1))
                Select(self.driver.find_element(By.ID, "ont_template_tcont_us_bw_combobox" + str(ind + 1))).select_by_visible_text("$py_ONTQoSBandwidthFull85T" + str(ind+1))
                selectProfile(self,"ont_template_tcont_ds_bw_combobox" + str(ind + 1), "$py_ONTQoSBandwidthFull85T" + str(ind+9))
                Select(self.driver.find_element(By.ID, "ont_template_tcont_ds_bw_combobox" + str(ind + 1))).select_by_visible_text("$py_ONTQoSBandwidthFull85T" + str(ind+9))
                Select(self.driver.find_element(By.ID, "ont_template_tcont_type_combobox" + str(ind + 1))).select_by_visible_text("Best-Effort")
            saveProfile (self)
        #Create service with "$py_TempONTServiceFull85"
        self.driver.find_element(By.LINK_TEXT, "Provision").click()
        time.sleep (3)
        self.driver.find_element(By.LINK_TEXT, "Service").click()
        time.sleep (3)
        self.driver.find_element(By.ID, "service_tab_ont").click()
        time.sleep (3)
        self.driver.find_element(By.CSS_SELECTOR, "#provision_service_create > a").click()
        time.sleep (3)
        self.driver.find_element(By.XPATH, "//input[@value='Select ONT']").click()
        time.sleep(3)
        self.driver.find_element(By.XPATH, "//label[@for='provision_select_ont_ip_checkbox']").click()
        self.driver.find_element(By.ID, "provision_select_ont_ip_text").send_keys(target_ip)
        self.driver.find_element(By.XPATH, "//label[@for='provision_select_ont_sn_checkbox']").click()
        self.driver.find_element(By.ID, "provision_select_ont_sn_text").send_keys(target_sn)
        self.driver.find_element(By.ID, "provision_select_ont_search_btn").click()
        target_row = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH,
                "//div[@id='provision_select_ont_table']/div[div[normalize-space(.)='" + target_sn + "']]"))
        )
        target_row.find_element(By.TAG_NAME, "label").click()
        self.driver.find_element(By.CSS_SELECTOR, "#modal_select_ont .modal-footer > .button").click()
        time.sleep(3)
        from libs.ems_tables import edit_new_ont_service_row
        edit_new_ont_service_row(self.driver)
        self.driver.find_element(By.XPATH, "//label[@for=\"provision_service_active_checkbox\"]").click()
        Select(self.driver.find_element(By.ID, "provision_service_onttemplate_combbox")).select_by_visible_text("$py_TempONTServiceFull85")
        time.sleep(5)
        self.driver.find_element(By.ID, "provision_service_desc_text").send_keys("Full service 5A5958458CBCA751")
        self.driver.find_element(By.ID, "provision_service_dspir_text").send_keys("10000000")
        #Wan Setting
        for ind in range (8):
            self.driver.find_element(By.XPATH, "//label[@for=\"provision_service_wan_table_active_" + str(ind + 1) + "\"]").click()
            self.driver.find_element(By.ID, "provision_service_wan_table_address_" + str(ind + 1)).send_keys("192.168.10" + str(ind + 1) + ".1")
            self.driver.find_element(By.ID, "provision_service_wan_table_mask_" + str(ind + 1)).send_keys("255.255.255.0")
            self.driver.find_element(By.ID, "provision_service_wan_table_gateway_" + str(ind + 1)).send_keys("192.168.10" + str(ind + 1) + ".254")
            self.driver.find_element(By.ID, "provision_service_wan_table_pridns_" + str(ind + 1)).send_keys("1.2.3.4" + str(ind + 1))
            self.driver.find_element(By.ID, "provision_service_wan_table_secdns_" + str(ind + 1)).send_keys("5.6.7.8" + str(ind + 1))
            self.driver.find_element(By.ID, "provision_service_wan_table_username_" + str(ind + 1)).send_keys("Usr" + str(ind + 1) + "@hinet.net")
            self.driver.find_element(By.ID, "provision_service_wan_table_password_" + str(ind + 1)).send_keys("Pwd" + str(ind + 1))
        #Wifi Setting
        for ind in range (4):
            self.driver.find_element(By.XPATH, "//label[@for=\"provision_service_wify24g_table_active_" + str(ind + 1) + "\"]").click()
            self.driver.find_element(By.ID, "provision_service_wify24g_table_ssid_" + str(ind + 1)).send_keys("SSID24_Test" + str(ind + 1))
            self.driver.find_element(By.ID, "provision_service_wify24g_table_password_" + str(ind + 1)).send_keys("Password24_Test" + str(ind + 1))
            self.driver.find_element(By.XPATH, "//label[@for=\"provision_service_wify5g_table_active_" + str(ind + 1) + "\"]").click()
            self.driver.find_element(By.ID, "provision_service_wify5g_table_ssid_" + str(ind + 1)).send_keys("SSID5_Test" + str(ind + 1))
            self.driver.find_element(By.ID, "provision_service_wify5g_table_password_" + str(ind + 1)).send_keys("Password5_Test" + str(ind + 1))
        #VoIP Setting
        for ind in range (2):
            self.driver.find_element(By.XPATH, "//label[@for=\"provision_service_voip_table_active_" + str(ind + 1) + "\"]").click()
            Select(self.driver.find_element(By.ID, "provision_service_voip_table_uniport_" + str(ind + 1))).select_by_visible_text(str(ind + 1))
            self.driver.find_element(By.ID, "provision_service_voip_table_username_" + str(ind + 1)).send_keys("VoIPUsr" + str(ind + 1))
            self.driver.find_element(By.ID, "provision_service_voip_table_password_" + str(ind + 1)).send_keys("VoIPPwd" + str(ind + 1))
            self.driver.find_element(By.ID, "provision_service_voip_table_aor_" + str(ind + 1)).send_keys("+88603123456" + str(ind + 1))
        #QoS
        #Service T-cont Setting
        for ind in range (8):
            self.driver.find_element(By.ID, "provision_service_profile_qos_table_new").click()
            time.sleep(3)
            Select(self.driver.find_element(By.ID, "provision_service_qos_tcont_combbox")).select_by_visible_text("service" + str(ind + 1))
            Select(self.driver.find_element(By.ID, "provision_service_qos_usbandwidth_combbox")).select_by_visible_text("$py_newFull85G" + str(ind + 1))
            Select(self.driver.find_element(By.ID, "provision_service_qos_dsbandwidth_combbox")).select_by_visible_text("$py_newFull85G" + str(ind + 9))
            self.driver.find_element(By.ID, "provision_service_qos_vlan_text").send_keys(str(ind + 201))
            self.driver.find_element(By.ID, "provision_service_qos_svlan_text").send_keys(str(ind + 301))
            self.driver.find_element(By.ID, "provision_service_qos_cvlan_text").send_keys(str(ind + 401))
            self.driver.find_element(By.CSS_SELECTOR, "#modal_provision_service_qos .button").click()
            time.sleep(3)
            self.driver.find_element(By.ID, "provision_service_profile_qos_table_new").click()
            time.sleep(3)
            Select(self.driver.find_element(By.ID, "provision_service_qos_tcont_combbox")).select_by_visible_text("tcont" + str(ind + 1))
            Select(self.driver.find_element(By.ID, "provision_service_qos_usbandwidth_combbox")).select_by_visible_text("$py_newFull85T" + str(ind + 1))
            Select(self.driver.find_element(By.ID, "provision_service_qos_dsbandwidth_combbox")).select_by_visible_text("$py_newFull85T" + str(ind + 9))
            self.driver.find_element(By.CSS_SELECTOR, "#modal_provision_service_qos .button").click()
            time.sleep(3)
        #IP-Host setting
        self.driver.find_element(By.ID, "provision_service_hostip_vlan_text").send_keys("4094")
        self.driver.find_element(By.ID, "provision_service_hostip_pbit_text").send_keys("7")
        Select(self.driver.find_element(By.ID, "provision_service_hostip_mode_combbox")).select_by_visible_text("Static")
        self.driver.find_element(By.ID, "provision_service_hostip_staticip_text").send_keys("192.168.123.4")
        self.driver.find_element(By.ID, "provision_service_hostip_mask_text").send_keys("255.255.255.0")
        self.driver.find_element(By.ID, "provision_service_hostip_gateway_text").send_keys("192.168.123.254")
        self.driver.find_element(By.ID, "provision_service_hostip_pridns_text").send_keys("1.2.3.4")
        self.driver.find_element(By.ID, "provision_service_hostip_secdns_text").send_keys("5.6.7.8")
        self.driver.find_element(By.ID, "provision_save_service_btn").click()
        time.sleep(3)
        # Submit only the selected ONT and retain the configuration.
        self.driver.find_element(By.XPATH, "//*[@id='create_service_background']/div[2]/input").click()
        WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#message_diag .button"))
        ).click()



    # Maintenance / Firmware File Management / Upload / Access Log
    @pytest.mark.Unicase
    def test_EMS1_6317_fwManagementAccessLog(self):
        dut_type = str(self.dutType)
        if "NeoX" in dut_type:
            upload_key = "NXC"
        elif "IES" in dut_type:
            upload_key = "MSC"
        elif "OLT14" in dut_type:
            upload_key = "Image"
        else:
            pytest.skip(f"EMS1-6317 has no firmware upload mapping for DUT type {dut_type!r}.")

        upload_file = os.path.abspath(os.path.join(self.uploadPath, upload_key))
        assert os.path.isfile(upload_file), f"Firmware upload file does not exist: {upload_file}"

        self.driver.find_element(By.LINK_TEXT, "Maintenance").click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Firmware File Management"))
        ).click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#i_action_create_collector > a"))
        )

        main_window = self.driver.current_window_handle
        handles_before = set(self.driver.window_handles)
        self.driver.find_element(By.CSS_SELECTOR, "#i_action_create_collector > a").click()
        upload_window = WebDriverWait(self.driver, 30).until(
            lambda driver: next(
                (handle for handle in driver.window_handles if handle not in handles_before),
                None,
            )
        )
        self.driver.switch_to.window(upload_window)
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.ID, "loadfile"))
        ).click()
        file_input = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, "load"))
        )
        file_input.send_keys(upload_file)

        upload_time = datetime.now().replace(microsecond=0)
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".button"))
        ).click()

        def wait_for_upload_result(driver):
            if upload_window not in driver.window_handles:
                return "upload window closed automatically"
            try:
                driver.switch_to.window(upload_window)
                alert = driver.switch_to.alert
                alert_text = alert.text.strip()
                alert.accept()
                return alert_text
            except Exception:
                # The EMS upload popup may close itself at the same instant that
                # Selenium detects the success alert. Treat the closed popup as
                # completion; the table row and Access Log are verified below.
                if upload_window not in driver.window_handles:
                    return "upload window closed automatically"
                return False

        upload_alert_text = WebDriverWait(self.driver, 600).until(wait_for_upload_result)
        if "closed automatically" not in upload_alert_text.casefold():
            assert "success" in upload_alert_text.casefold(), (
                f"Firmware upload did not report success: {upload_alert_text!r}"
            )
        upload_complete_time = datetime.now().replace(microsecond=0)
        print(
            f"EMS1-6317: upload completed, message={upload_alert_text!r}, "
            f"started={upload_time}, completed={upload_complete_time}",
            flush=True,
        )
        self.driver.switch_to.window(main_window)

        if upload_window in self.driver.window_handles:
            self.driver.switch_to.window(upload_window)
            self.driver.close()
            self.driver.switch_to.window(main_window)

        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#i_action_refresh > a"))
        ).click()
        upload_table_end = upload_complete_time + timedelta(minutes=1)
        total_pages = pageCount(self, "schedule_fw_table")
        if total_pages > 1:
            self.driver.find_element(
                By.CSS_SELECTOR,
                "#schedule_fw_table .first",
            ).click()

        upload_rows = []
        for page_index in range(1, total_pages + 1):
            headers = self.driver.find_elements(
                By.XPATH,
                "//table[@id='schedule_fw_table_head']/thead/tr/th",
            )
            column_indexes = {
                header.get_attribute("name"): index + 1
                for index, header in enumerate(headers)
            }
            assert "name" in column_indexes and "time" in column_indexes, (
                f"Firmware table columns do not include name/time: {column_indexes!r}"
            )
            rows = self.driver.find_elements(
                By.XPATH,
                "//table[@id='schedule_fw_table_body']/tbody/tr",
            )
            for row_index in range(1, len(rows) + 1):
                filename = self.driver.find_element(
                    By.XPATH,
                    "//table[@id='schedule_fw_table_body']/tbody/"
                    f"tr[{row_index}]/td[{column_indexes['name']}]",
                ).text.strip()
                row_time_text = self.driver.find_element(
                    By.XPATH,
                    "//table[@id='schedule_fw_table_body']/tbody/"
                    f"tr[{row_index}]/td[{column_indexes['time']}]",
                ).text.strip()
                try:
                    row_time = parser.parse(
                        re.sub(r"\s*\(.*$", "", row_time_text).strip()
                    ).replace(tzinfo=None)
                except (TypeError, ValueError, OverflowError):
                    continue
                if upload_time <= row_time <= upload_table_end and filename:
                    upload_rows.append((row_time, filename, [page_index, row_index]))
            if page_index < total_pages:
                self.driver.find_element(
                    By.CSS_SELECTOR,
                    "#schedule_fw_table .next",
                ).click()

        assert upload_rows, (
            "Firmware File Management has no row in the upload-time range. "
            f"local_file={upload_file!r}, range={upload_time}..{upload_table_end}"
        )
        _, uploaded_filename, uploaded_table_position = max(
            upload_rows,
            key=lambda row: row[0],
        )
        query_from = (upload_time - timedelta(minutes=1)).strftime(self.dateFormat)
        query_to = (datetime.now().replace(microsecond=0) + timedelta(minutes=1)).strftime(
            self.dateFormat
        )

        self.driver.find_element(By.LINK_TEXT, "System").click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Security"))
        ).click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.ID, "access_log_browse"))
        ).click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#i_action_filter > a"))
        ).click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='filter_background']/div[2]/input[@value='Reset']")
            )
        ).click()

        for field_id, value in (
            ("accesslog_datepickerFrom_filter", query_from),
            ("accesslog_datepickerTo_filter", query_to),
        ):
            field = self.driver.find_element(By.ID, field_id)
            field.click()
            field.clear()
            field.send_keys(value)
            close_buttons = [
                button for button in self.driver.find_elements(
                    By.CSS_SELECTOR,
                    ".ui-datepicker-close",
                )
                if button.is_displayed()
            ]
            if close_buttons:
                close_buttons[0].click()
        self.driver.find_element(By.ID, "accesslog_query_button").click()

        expected_description = (
            "[Maintenance - firmware file management] new success "
            f"(filename [{uploaded_filename}])"
        )
        position = [-1, -1]
        log_deadline = time.monotonic() + 120
        while time.monotonic() < log_deadline:
            position = getPositionByCol(
                self,
                "accessLog_table",
                "Description",
                expected_description,
            )
            if position != [-1, -1]:
                break
            refresh_buttons = self.driver.find_elements(
                By.CSS_SELECTOR,
                "#i_action_refresh > a",
            )
            if refresh_buttons:
                refresh_buttons[0].click()
            time.sleep(2)

        print(
            f"EMS1-6317: upload_time={upload_time}, local_file={upload_file!r}, "
            f"uploaded_filename={uploaded_filename!r}, "
            f"uploaded_table_position={uploaded_table_position}, "
            f"query={query_from}..{query_to}, position={position}",
            flush=True,
        )
        with assume:
            assert position != [-1, -1], (
                f"Firmware upload Access Log was not found: "
                f"{expected_description!r} between {query_from} and {query_to}"
            )

        self.driver.find_element(By.LINK_TEXT, "Maintenance").click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Firmware File Management"))
        ).click()
        uploaded_position = getPositionByCol(
            self,
            "schedule_fw_table",
            "name",
            uploaded_filename,
        )
        assert uploaded_position != [-1, -1], (
            f"Uploaded firmware cannot be selected for deletion: {uploaded_filename!r}"
        )
        getElementByPositionCol(
            self,
            "schedule_fw_table",
            uploaded_position,
            "Checkbox",
        ).click()

        delete_time = datetime.now().replace(microsecond=0)
        self.driver.find_element(By.CSS_SELECTOR, "#i_action_delete > a").click()

        expected_delete_description = (
            "[Maintenance - firmware file management] delete success "
            f"(filename [{uploaded_filename}])"
        )
        delete_query_from = (delete_time - timedelta(minutes=1)).strftime(
            self.dateFormat
        )
        delete_query_to = (
            datetime.now().replace(microsecond=0) + timedelta(minutes=1)
        ).strftime(self.dateFormat)

        self.driver.find_element(By.LINK_TEXT, "System").click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Security"))
        ).click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.ID, "access_log_browse"))
        ).click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#i_action_filter > a"))
        ).click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='filter_background']/div[2]/input[@value='Reset']")
            )
        ).click()

        for field_id, value in (
            ("accesslog_datepickerFrom_filter", delete_query_from),
            ("accesslog_datepickerTo_filter", delete_query_to),
        ):
            field = self.driver.find_element(By.ID, field_id)
            field.click()
            field.clear()
            field.send_keys(value)
            close_buttons = [
                button for button in self.driver.find_elements(
                    By.CSS_SELECTOR,
                    ".ui-datepicker-close",
                )
                if button.is_displayed()
            ]
            if close_buttons:
                close_buttons[0].click()
        self.driver.find_element(By.ID, "accesslog_query_button").click()

        delete_position = [-1, -1]
        delete_log_deadline = time.monotonic() + 120
        while time.monotonic() < delete_log_deadline:
            delete_position = getPositionByCol(
                self,
                "accessLog_table",
                "Description",
                expected_delete_description,
            )
            if delete_position != [-1, -1]:
                break
            refresh_buttons = self.driver.find_elements(
                By.CSS_SELECTOR,
                "#i_action_refresh > a",
            )
            if refresh_buttons:
                refresh_buttons[0].click()
            time.sleep(2)

        print(
            f"EMS1-6317: delete_time={delete_time}, "
            f"uploaded_filename={uploaded_filename!r}, "
            f"query={delete_query_from}..{delete_query_to}, "
            f"delete_position={delete_position}",
            flush=True,
        )
        with assume:
            assert delete_position != [-1, -1], (
                f"Firmware delete Access Log was not found: "
                f"{expected_delete_description!r} between "
                f"{delete_query_from} and {delete_query_to}"
            )


    # Maintenance / Result Log / Delete / Access Log
    @pytest.mark.Unicase
    def test_EMS1_6318_deleteScheduleLogAccessLog(self):
        self.driver.find_element(By.LINK_TEXT, "Maintenance").click()
        result_links = WebDriverWait(self.driver, 30).until(
            lambda driver: [
                link for link in driver.find_elements(By.LINK_TEXT, "Result Log")
                + driver.find_elements(By.LINK_TEXT, "Result")
                if link.is_displayed() and link.is_enabled()
            ]
        )
        result_links[0].click()
        WebDriverWait(self.driver, 30).until(
            lambda driver: driver.find_elements(
                By.CSS_SELECTOR,
                "#schedule_result_table_body tbody tr",
            )
        )

        first_row_position = [1, 1]
        log_id = getElementByPositionCol(
            self,
            "schedule_result_table",
            first_row_position,
            "logID",
        ).text.strip()
        assert log_id, "The first Maintenance Result Log row has no Log ID."
        getElementByPositionCol(
            self,
            "schedule_result_table",
            first_row_position,
            "Checkbox",
        ).click()

        delete_click_time = datetime.now().replace(microsecond=0)
        self.driver.find_element(By.CSS_SELECTOR, "#i_action_delete > a").click()
        message = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.ID, "message_text"))
        )
        with assume:
            assert message.text.strip() == "Delete success.", (
                f"Maintenance Result Log {log_id} delete message: {message.text!r}"
            )
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#message_diag .button"))
        ).click()

        expected_description = (
            "[Maintenance - result log] delete success "
            f"(schedule log ID : {log_id})"
        )
        query_from = (delete_click_time - timedelta(minutes=1)).strftime(
            self.dateFormat
        )
        query_to = (datetime.now().replace(microsecond=0) + timedelta(minutes=1)).strftime(
            self.dateFormat
        )

        self.driver.find_element(By.LINK_TEXT, "System").click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Security"))
        ).click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.ID, "access_log_browse"))
        ).click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#i_action_filter > a"))
        ).click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='filter_background']/div[2]/input[@value='Reset']")
            )
        ).click()

        for field_id, value in (
            ("accesslog_datepickerFrom_filter", query_from),
            ("accesslog_datepickerTo_filter", query_to),
        ):
            field = self.driver.find_element(By.ID, field_id)
            field.click()
            field.clear()
            field.send_keys(value)
            close_buttons = [
                button for button in self.driver.find_elements(
                    By.CSS_SELECTOR,
                    ".ui-datepicker-close",
                )
                if button.is_displayed()
            ]
            if close_buttons:
                close_buttons[0].click()
        self.driver.find_element(By.ID, "accesslog_query_button").click()

        position = [-1, -1]
        deadline = time.monotonic() + 60
        while time.monotonic() < deadline:
            position = getPositionByCol(
                self,
                "accessLog_table",
                "Description",
                expected_description,
            )
            if position != [-1, -1]:
                break
            refresh_buttons = self.driver.find_elements(
                By.CSS_SELECTOR,
                "#i_action_refresh > a",
            )
            if refresh_buttons:
                refresh_buttons[0].click()
            time.sleep(2)

        print(
            f"EMS1-6318: delete_time={delete_click_time}, log_id={log_id}, "
            f"query={query_from}..{query_to}, position={position}",
            flush=True,
        )
        with assume:
            assert position != [-1, -1], (
                f"Maintenance Result Log delete Access Log was not found: "
                f"{expected_description!r} between {query_from} and {query_to}"
            )


    # Inventory / Transceiver / RESTful Device Information
    @pytest.mark.Unicase
    def test_EMS1_7072_transceiverInfo(self):
        report_dir = os.path.join(os.path.dirname(__file__), "report")
        dev_data, perf_data, paths, original_mibs = capture_restful_debug_files(
            self,
            report_dir,
        )
        for debug_name, debug_path in list(paths.items()):
            renamed_path = debug_path.with_name(
                debug_path.name.replace("EMS1-4903_", "EMS1-7072_", 1)
            )
            debug_path.replace(renamed_path)
            paths[debug_name] = renamed_path
        assert isinstance(perf_data, dict), (
            f"Downloaded performance debug file is not a JSON object: "
            f"{paths[f'{self.dutIp}_perf']}"
        )
        port_info = dev_data.get("portinfo")
        assert isinstance(port_info, list), (
            "RESTful dev JSON has no portinfo list."
        )

        def normalize(value):
            text = " ".join(str(value if value is not None else "").split())
            # Some legacy transceiver strings contain invalid source bytes.
            # EMS renders each invalid byte as U+FFFD, while the RESTful JSON
            # loader drops it with errors="ignore". Remove only that replacement
            # marker so the remaining readable value can still be compared.
            text = text.replace("\ufffd", "")
            return "" if text.casefold() in {"", "--", "null"} else text

        expected_rows = {}
        for port in port_info:
            transceiver_fields = (
                "vendorname",
                "vendorpn",
                "vendorrevision",
                "vendorsn",
                "vendordc",
                "transceiver",
                "calibration",
            )
            if not any(normalize(port.get(field)) for field in transceiver_fields):
                continue
            key = (normalize(port.get("slot")), normalize(port.get("port")))
            expected_rows[key] = {
                "DevName": normalize(self.dutName),
                "IPAddress": normalize(self.dutIp),
                "SlotID": key[0],
                "PortID": key[1],
                "VendorName": normalize(port.get("vendorname")),
                "VendorPN": normalize(port.get("vendorpn")),
                "VendorRevision": normalize(port.get("vendorrevision")),
                "VendorSN": normalize(port.get("vendorsn")),
                "VendorDc": normalize(port.get("vendordc")),
                "ModuleTypeName": normalize(port.get("transceiver")),
                "ModuleTypeCalibration": normalize(port.get("calibration")),
            }
        assert expected_rows, (
            "RESTful dev JSON portinfo contains no Transceiver entries "
            "with non-empty Transceiver vendor/module fields."
        )

        self.driver.find_element(By.LINK_TEXT, "Inventory").click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Transceiver"))
        ).click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#i_action_filter > a"))
        ).click()
        self.driver.find_element(By.ID, "inventory_transceiver_clear_btn").click()
        ip_field = self.driver.find_element(By.ID, "ip_transceiver")
        ip_field.clear()
        ip_field.send_keys(self.dutIp)
        self.driver.find_element(By.ID, "inventory_transceiver_btn").click()
        WebDriverWait(self.driver, 30).until(
            lambda _driver: totalData(self, "transceiver_inventory_div") > 0
        )

        columns = (
            "DevName",
            "IPAddress",
            "SlotID",
            "PortID",
            "VendorName",
            "VendorPN",
            "VendorRevision",
            "VendorSN",
            "VendorDc",
            "ModuleTypeName",
            "ModuleTypeCalibration",
        )
        table_id = "transceiver_inventory_div"
        page_total = pageCount(self, table_id)
        actual_rows = {}
        for _page_index in range(page_total):
            # Read every requested cell from the same DOM row in one JavaScript
            # operation. Reading one column at a time can fabricate Slot/Port
            # pairs when the live table refreshes or reorders between reads.
            page_rows = self.driver.execute_script(
                r"""
                const tableId = arguments[0];
                const requested = arguments[1];
                const headers = Array.from(document.querySelectorAll(
                    `#${tableId}_head thead tr th`
                ));
                const indexes = Object.fromEntries(requested.map(name => [
                    name,
                    headers.findIndex(header => header.getAttribute("name") === name)
                ]));
                return Array.from(document.querySelectorAll(
                    `#${tableId}_body tbody tr`
                )).map(row => {
                    const cells = Array.from(row.querySelectorAll(":scope > td"));
                    return Object.fromEntries(requested.map(name => [
                        name,
                        indexes[name] >= 0 && cells[indexes[name]]
                            ? cells[indexes[name]].innerText
                            : ""
                    ]));
                });
                """,
                table_id,
                list(columns),
            )
            for page_row in page_rows:
                actual = {
                    column: normalize(page_row.get(column, ""))
                    for column in columns
                }
                key = (actual["SlotID"], actual["PortID"])
                actual_rows[key] = actual

            if page_total > 1 and pageCurrent(self, table_id) < page_total:
                current_page = pageCurrent(self, table_id)
                self.driver.find_element(By.CSS_SELECTOR, f"#{table_id} .next").click()
                WebDriverWait(self.driver, 30).until(
                    lambda _driver: pageCurrent(self, table_id) != current_page
                )

        if page_total > 1:
            self.driver.find_element(By.CSS_SELECTOR, f"#{table_id} .first").click()

        print(
            f"EMS1-7072 EMS table Slot/Port keys={sorted(actual_rows)}",
            flush=True,
        )

        with assume:
            assert set(actual_rows) == set(expected_rows), (
                "Transceiver Slot/Port entries differ between EMS and RESTful dev JSON. "
                f"EMS-only={sorted(set(actual_rows) - set(expected_rows))}, "
                f"RESTful-only={sorted(set(expected_rows) - set(actual_rows))}"
            )

        for key in sorted(set(actual_rows) & set(expected_rows)):
            for column in columns:
                with assume:
                    assert actual_rows[key][column] == expected_rows[key][column], (
                        f"Transceiver Slot {key[0]}, Port {key[1]}, {column}: "
                        f"EMS={actual_rows[key][column]!r}, "
                        f"RESTful={expected_rows[key][column]!r}"
                    )

        print(
            f"EMS1-7072: compared {len(actual_rows)} Transceiver rows; "
            f"RESTful files={paths}; original MIB values restored="
            f"{sorted(original_mibs)}",
            flush=True,
        )


    # Inventory / Transceiver / Export
    @pytest.mark.Unicase
    def test_EMS1_7051_transceiverExport(self):
        self.driver.find_element(By.LINK_TEXT, "Inventory").click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Transceiver"))
        ).click()
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.ID, "transceiver_inventory_div"))
        )

        min_time = datetime.now()
        files_before = set(glob.glob(os.path.join(self.downloadpath, "*.xls")))
        export_table_snapshot = capture_table_and_export(
            self.driver,
            "transceiver_inventory_div",
        )

        latest_file = None
        deadline = time.monotonic() + 60
        while time.monotonic() < deadline:
            candidates = glob.glob(os.path.join(self.downloadpath, "*.xls"))
            new_candidates = [path for path in candidates if path not in files_before]
            if not new_candidates:
                new_candidates = [
                    path for path in candidates
                    if datetime.fromtimestamp(os.path.getmtime(path)) >= min_time
                ]
            if new_candidates:
                candidate = max(new_candidates, key=os.path.getmtime)
                if os.path.getsize(candidate) > 0:
                    latest_file = candidate
                    break
            time.sleep(1)

        with assume:
            assert latest_file is not None, (
                "Transceiver export file was not downloaded within 60 seconds."
            )
        if latest_file is None:
            return

        latest_file_size = os.path.getsize(latest_file)
        with assume:
            assert latest_file_size > 0, (
                f"Transceiver export file is empty: {latest_file}"
            )
        assert_export_matches(
            latest_file,
            export_table_snapshot,
            "Inventory Transceiver",
        )


    # Inventory / Transceiver / Filter
    @pytest.mark.Unicase
    def test_EMS1_7049_transceiverFilter(self):
        if "OLT14" in self.dutType.upper():
            pytest.skip("EMS1-7049 does not support the OLT14xx series.")

        def card_by_token(token):
            token = token.upper()
            for key, card in self.dutCardInfo.items():
                card_text = f"{key} {card.get('type', '')}".upper()
                if token in card_text:
                    return card
            return None

        main_card = card_by_token("NXC") or card_by_token("MSC")
        nxp_card = card_by_token("NXP")
        if not main_card:
            pytest.skip(
                "EMS1-7049 requires an NXC or MSC card in "
                "environment_parameter.json CARDINFO."
            )
        if not nxp_card:
            pytest.skip(
                "EMS1-7049 requires an NXP card in "
                "environment_parameter.json CARDINFO."
            )

        expected_slot = str(main_card["slot_id"])
        expected_port = str(nxp_card["port_id"])

        def open_filter():
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#i_action_filter > a"))
            ).click()
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.ID, "inventory_transceiver_btn"))
            )

        def set_filter(field_values):
            for field_id, value in field_values:
                field = self.driver.find_element(By.ID, field_id)
                field.clear()
                field.send_keys(value)
            self.driver.find_element(By.ID, "inventory_transceiver_btn").click()
            WebDriverWait(self.driver, 30).until(
                lambda _driver: totalData(self, "transceiver_inventory_div") >= 0
            )
            time.sleep(2)

        def assert_column(column, expected):
            values = getListByCol(self, "transceiver_inventory_div", column)
            with assume:
                assert values, (
                    f"Transceiver filter {column}={expected!r} returned no data."
                )
            with assume:
                assert all(value.strip() == expected for value in values), (
                    f"Transceiver column {column} expected every value to be "
                    f"{expected!r}, actual={values!r}"
                )

        self.driver.find_element(By.LINK_TEXT, "Inventory").click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Transceiver"))
        ).click()

        open_filter()
        set_filter((
            ("deviceName_transceiver", self.dutName),
            ("slot_transceiver", expected_slot),
        ))
        assert_column("DevName", self.dutName)
        assert_column("SlotID", expected_slot)

        open_filter()
        self.driver.find_element(By.ID, "inventory_transceiver_clear_btn").click()
        set_filter((
            ("ip_transceiver", self.dutIp),
            ("port_transceiver", expected_port),
        ))
        assert_column("IPAddress", self.dutIp)
        assert_column("PortID", expected_port)


    # Map / Device / Clear Alarm / Access Log
    @pytest.mark.Unicase
    def test_EMS1_6238_clearAlarmGeneratedAccessLog(self):
        expected_description = (
            "[Topology - clear device alarm] set success "
            f"(device name={self.dutName}, IP address={self.dutIp})"
        )

        open_map_device_status(self.driver, self.dutNodeName, self.dutIp)
        clear_click_time = datetime.now().replace(microsecond=0)
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#i_action_clear > a"))
        ).click()
        dialog_buttons = WebDriverWait(self.driver, 30).until(
            lambda driver: [
                button for button in driver.find_elements(
                    By.CSS_SELECTOR, "#message_diag .button"
                )
                if button.is_displayed() and button.is_enabled()
            ]
        )
        dialog_buttons[0].click()

        query_from_time = clear_click_time - timedelta(minutes=1)
        query_to_time = datetime.now().replace(microsecond=0) + timedelta(minutes=1)
        query_from = query_from_time.strftime(self.dateFormat)
        query_to = query_to_time.strftime(self.dateFormat)

        self.driver.find_element(By.LINK_TEXT, "System").click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Security"))
        ).click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.ID, "access_log_browse"))
        ).click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#i_action_filter > a"))
        ).click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='filter_background']/div[2]/input[@value='Reset']")
            )
        ).click()

        for field_id, value in (
            ("accesslog_datepickerFrom_filter", query_from),
            ("accesslog_datepickerTo_filter", query_to),
        ):
            field = self.driver.find_element(By.ID, field_id)
            field.click()
            field.clear()
            field.send_keys(value)
            close_buttons = [
                button for button in self.driver.find_elements(
                    By.CSS_SELECTOR, ".ui-datepicker-close"
                )
                if button.is_displayed()
            ]
            if close_buttons:
                close_buttons[0].click()
        self.driver.find_element(By.ID, "accesslog_query_button").click()

        def matching_log_position():
            return getPositionByCol(
                self,
                "accessLog_table",
                "Description",
                expected_description,
            )

        position = [-1, -1]
        deadline = time.monotonic() + 60
        while time.monotonic() < deadline:
            position = matching_log_position()
            if position != [-1, -1]:
                break
            refresh_buttons = self.driver.find_elements(
                By.CSS_SELECTOR, "#i_action_refresh > a"
            )
            if refresh_buttons:
                refresh_buttons[0].click()
            time.sleep(2)

        print(
            f"EMS1-6238: clicked={clear_click_time}, query={query_from}..{query_to}, "
            f"expected={expected_description!r}, position={position}",
            flush=True,
        )
        with assume:
            assert position != [-1, -1], (
                f"Clear-device-alarm Access Log was not found between "
                f"{query_from} and {query_to}: {expected_description}"
            )


    # Alarm / Active / Login Success from Remote Control
    @pytest.mark.Unicase
    def test_EMS1_4907_loginSuccessAlarm(self):
        def clean_cli(output):
            output = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", output or "")
            return output.replace("\r", "")

        def device_datetime(output):
            patterns = [
                (r"(\d{2}:\d{2}:\d{2})\s+(\d{2}/\d{2}/\d{4})", "%H:%M:%S %m/%d/%Y"),
                (r"(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})", "%Y-%m-%d %H:%M:%S"),
            ]
            for pattern, date_format in patterns:
                match = re.search(pattern, output)
                if match:
                    return datetime.strptime(" ".join(match.groups()), date_format)
            raise AssertionError(f"Cannot parse device time from show time: {output!r}")

        show_time = clean_cli(run_ssh_commands(
            self.dutIp,
            self.dutAdminName,
            self.dutAdminPwd,
            ["show time"],
        ))
        current_device_time = device_datetime(show_time)
        timezone_ok = bool(re.search(r"timezone\s*=\s*\+?0800", show_time, re.I))
        time_difference = abs((datetime.now() - current_device_time).total_seconds())
        if not timezone_ok or time_difference > 120:
            time_setup = clean_cli(run_ssh_commands(
                self.dutIp,
                self.dutAdminName,
                self.dutAdminPwd,
                [
                    "configure",
                    "time server",
                    "time server address 216.239.35.4",
                    "time server type ntp",
                    "time timezone 0800",
                    "time server sync",
                    "exit",
                ],
            ))
            unexpected_errors = [
                line for line in time_setup.splitlines()
                if re.search(r"(?:error|invalid|fail)", line, re.I)
                and "ntp server existed" not in line.casefold()
            ]
            with assume:
                assert not unexpected_errors, (
                    f"Unexpected device time configuration errors: {unexpected_errors}"
                )
            time.sleep(5)
            show_time = clean_cli(run_ssh_commands(
                self.dutIp,
                self.dutAdminName,
                self.dutAdminPwd,
                ["show time"],
            ))
            current_device_time = device_datetime(show_time)
            timezone_ok = bool(re.search(r"timezone\s*=\s*\+?0800", show_time, re.I))
            time_difference = abs((datetime.now() - current_device_time).total_seconds())
        with assume:
            assert timezone_ok, f"Device timezone should be +0800: {show_time!r}"
        with assume:
            assert time_difference <= 120, (
                f"Device time differs from EMS test host by {time_difference:.1f} seconds: "
                f"device={current_device_time}, host={datetime.now()}"
            )

        running_config = clean_cli(run_ssh_commands(
            self.dutIp,
            self.dutAdminName,
            self.dutAdminPwd,
            ["show running-config"],
            timeout=120,
        ))
        version_match = re.search(
            r"^\s*snmp-server\s+version\s+(\S+)",
            running_config,
            re.I | re.M,
        )
        assert version_match, "Cannot find active snmp-server version in running-config"
        active_snmp_version = version_match.group(1).casefold()
        trap_pattern = re.compile(
            r"^\s*snmp-server\s+trap-destination\s+(\d+)\s+address\s+(\S+)"
            r".*?\sversion\s+(\S+)(?:\s+username\s+(\S*))?",
            re.I | re.M,
        )
        trap_destinations = [match.groups() for match in trap_pattern.finditer(running_config)]

        def valid_ems_trap(entry):
            _index, address, version, _username = entry
            return address == self.emsIp and version.casefold() == active_snmp_version

        if not any(valid_ems_trap(entry) for entry in trap_destinations):
            empty_entry = next(
                (entry for entry in trap_destinations if entry[1] == "0.0.0.0"),
                None,
            )
            trap_index = empty_entry[0] if empty_entry else "1"
            trap_command = (
                f"snmp-server trap-destination {trap_index} address {self.emsIp} "
                f"udp-port 162 version {active_snmp_version}"
            )
            if active_snmp_version == "v3":
                trap_command += f" username {self.dutAdminName}"
            run_ssh_commands(
                self.dutIp,
                self.dutAdminName,
                self.dutAdminPwd,
                ["configure", trap_command, "exit"],
            )
            running_config = clean_cli(run_ssh_commands(
                self.dutIp,
                self.dutAdminName,
                self.dutAdminPwd,
                ["show running-config"],
                timeout=120,
            ))
            trap_destinations = [
                match.groups() for match in trap_pattern.finditer(running_config)
            ]
        assert any(valid_ems_trap(entry) for entry in trap_destinations), (
            f"No trap-destination points to EMS {self.emsIp} with SNMP "
            f"version {active_snmp_version}. destinations={trap_destinations}"
        )
        print(
            f"EMS1-4907: device_time={current_device_time}, timezone=+0800, "
            f"snmp_version={active_snmp_version}, "
            f"ems_traps={[entry for entry in trap_destinations if entry[1] == self.emsIp]}",
            flush=True,
        )

        open_map_device_status(self.driver, self.dutNodeName, self.dutIp)
        remote_click_time = datetime.now().replace(microsecond=0)
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Remote Control"))
        ).click()
        WebDriverWait(self.driver, 60, poll_frequency=0.5).until(
            lambda driver: "#" in driver.find_element(By.ID, "console").text
        )

        self.driver.find_element(By.LINK_TEXT, "Alarm").click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Active"))
        ).click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#i_action_filter > a"))
        ).click()
        reset_button = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.ID, "fault_active_clear_btn"))
        )
        reset_button.click()

        target_labels = self.driver.find_elements(
            By.XPATH,
            f"//*[@id='filter_background']//label[contains(normalize-space(.), '{self.dutIp}')]",
        )
        if not target_labels:
            for selector in (
                "#filter_background li:nth-child(1) > .arrow",
                "#filter_background li:nth-child(1) > .collapsed",
            ):
                for expander in self.driver.find_elements(By.CSS_SELECTOR, selector):
                    try:
                        expander.click()
                        time.sleep(0.5)
                    except Exception:
                        pass
            target_labels = self.driver.find_elements(
                By.XPATH,
                f"//*[@id='filter_background']//label[contains(normalize-space(.), '{self.dutIp}')]",
            )
        assert target_labels, f"Cannot find DUT {self.dutIp} in Active Alarm Target tree"
        target_labels[0].location_once_scrolled_into_view
        target_labels[0].click()

        query_from = (remote_click_time - timedelta(minutes=1)).strftime("%Y/%m/%d %H:%M:%S")
        query_to_time = datetime.now().replace(microsecond=0) + timedelta(minutes=1)
        query_to = query_to_time.strftime("%Y/%m/%d %H:%M:%S")
        for field_id, value in (
            ("alarm_datepickerFrom_filter", query_from),
            ("alarm_datepickerTo_filter", query_to),
        ):
            field = self.driver.find_element(By.ID, field_id)
            field.click()
            field.clear()
            field.send_keys(value)
            close_buttons = [
                button for button in self.driver.find_elements(
                    By.CSS_SELECTOR, ".ui-datepicker-close"
                )
                if button.is_displayed()
            ]
            if close_buttons:
                close_buttons[0].click()
        self.driver.find_element(By.ID, "fault_active_btn").click()

        found_position = [-1, -1]
        deadline = time.monotonic() + 120
        while time.monotonic() < deadline:
            found_position = getPositionByColNext(
                self,
                "alarm_activeAlarmTable",
                "Description",
                "Login Success",
            )
            if found_position != [-1, -1]:
                found_ip = getElementByPositionCol(
                    self, "alarm_activeAlarmTable", found_position, "DevIP"
                ).text
                found_log_time = getElementByPositionCol(
                    self, "alarm_activeAlarmTable", found_position, "LogTime"
                ).text
                parsed_log_time = datetime.strptime(
                    re.sub(r"\s*\(.*$", "", found_log_time),
                    self.dateFormat,
                )
                if found_ip == self.dutIp and query_from <= parsed_log_time.strftime("%Y/%m/%d %H:%M:%S") <= query_to:
                    break
                found_position = [-1, -1]
            refresh = self.driver.find_elements(By.CSS_SELECTOR, "#i_action_refresh > a")
            if refresh:
                refresh[0].click()
            time.sleep(5)

        with assume:
            assert found_position != [-1, -1], (
                f"Login Success alarm for {self.dutIp} was not found between "
                f"{query_from} and {query_to}; Remote Control clicked at {remote_click_time}"
            )


    # Alarm / Active and History / Filter Time Reset
    @pytest.mark.Unicase
    def test_EMS1_5178_alarmFilterTimeReset(self):
        def button_state(button):
            return {
                "class": button.get_attribute("class") or "",
                "style": button.get_attribute("style") or "",
                "background": button.value_of_css_property("background-color") or "",
                "disabled": button.get_attribute("disabled"),
                "aria_disabled": button.get_attribute("aria-disabled"),
            }

        def rgb_channels(css_color):
            match = re.search(
                r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)",
                css_color or "",
            )
            return tuple(map(int, match.groups())) if match else None

        def set_datetime(field, value):
            field.click()
            field.clear()
            field.send_keys(value)
            close_buttons = [
                button for button in self.driver.find_elements(
                    By.CSS_SELECTOR, ".ui-datepicker-close"
                )
                if button.is_displayed()
            ]
            if close_buttons:
                close_buttons[0].click()
            WebDriverWait(self.driver, 10).until(
                lambda _driver: field.get_attribute("value") == value
            )

        def verify_page(page_name, suffix, reset_id):
            self.driver.find_element(By.LINK_TEXT, "Alarm").click()
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.LINK_TEXT, page_name))
            ).click()
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#i_action_filter > a"))
            ).click()

            from_field = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located(
                    (By.ID, f"alarm_datepickerFrom_{suffix}")
                )
            )
            to_field = self.driver.find_element(
                By.ID, f"alarm_datepickerTo_{suffix}"
            )
            reset_button = self.driver.find_element(By.ID, reset_id)

            # Establish the gray/empty baseline even if a previous run left a filter.
            if from_field.get_attribute("value") or to_field.get_attribute("value"):
                reset_button.click()
            WebDriverWait(self.driver, 10).until(
                lambda _driver: not from_field.get_attribute("value")
                and not to_field.get_attribute("value")
            )
            inactive_state = button_state(reset_button)

            now = datetime.now().replace(microsecond=0)
            set_datetime(from_field, now.strftime("%Y/%m/%d %H:%M:%S"))
            set_datetime(to_field, (now + timedelta(minutes=10)).strftime("%Y/%m/%d %H:%M:%S"))
            WebDriverWait(self.driver, 10).until(
                lambda _driver: button_state(reset_button) != inactive_state
            )
            active_state = button_state(reset_button)
            active_rgb = rgb_channels(active_state["background"])
            print(
                f"EMS1-5178 {page_name}: inactive={inactive_state}, active={active_state}",
                flush=True,
            )
            with assume:
                assert active_state != inactive_state, (
                    f"{page_name} Reset button should change from gray to green"
                )
            if active_rgb:
                with assume:
                    assert active_rgb[1] > active_rgb[0] and active_rgb[1] > active_rgb[2], (
                        f"{page_name} Reset button should be green; state={active_state}"
                    )

            reset_button.click()
            WebDriverWait(self.driver, 10).until(
                lambda _driver: not from_field.get_attribute("value")
                and not to_field.get_attribute("value")
                and "button_gray" in button_state(reset_button)["class"]
            )
            reset_state = button_state(reset_button)
            reset_rgb = rgb_channels(reset_state["background"])
            print(
                f"EMS1-5178 {page_name}: reset={reset_state}",
                flush=True,
            )
            with assume:
                assert from_field.get_attribute("value") == ""
            with assume:
                assert to_field.get_attribute("value") == ""
            with assume:
                assert "button_gray" in reset_state["class"], (
                    f"{page_name} Reset button should return to gray; state={reset_state}"
                )
            if reset_rgb:
                with assume:
                    assert max(reset_rgb) - min(reset_rgb) <= 10, (
                        f"{page_name} Reset background should be gray; state={reset_state}"
                    )

        verify_page("Active", "filter", "fault_active_clear_btn")
        verify_page("History", "history", "fault_history_clear_btn")


    # Map / Tree Node order
    @pytest.mark.Unicase
    def test_EMS1_3906_treeNodeOrder(self):
        groups = map_tree_node_order_groups(self.driver)
        assert groups, "Map tree should contain at least one sibling group to verify"
        for group in groups:
            actual_names = group["names"]
            expected_names = sorted(actual_names, key=map_tree_node_order_key)
            print(
                f"EMS1-3906: parent={group['parent']!r}, nodes={actual_names}",
                flush=True,
            )
            with assume:
                assert actual_names == expected_names, (
                    f"Map tree nodes under {group['parent']!r} are out of order. "
                    f"actual={actual_names}; expected={expected_names}"
                )


    # Map / Device / Availability and Device Panel link
    @pytest.mark.Unicase
    def test_EMS1_4361_availabilityDevicePanelLink(self):
        open_map_device_status(self.driver, self.dutNodeName, self.dutIp)
        report_dir = os.path.join(os.path.dirname(__file__), "report")
        os.makedirs(report_dir, exist_ok=True)

        status_image = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#device_image img"))
        )
        status_source = self.driver.execute_script(
            "return document.querySelector('#device_image img').src || '';"
        )
        with assume:
            assert status_source.startswith("data:image/"), (
                "Map Status equipment image should use a non-empty data:image source"
            )
        status_image.screenshot(
            os.path.join(report_dir, f"EMS1-4361_{self.dutIp}_status_image.png")
        )

        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Device panel"))
        ).click()
        panel_image = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#device_panel_dialog_image img")
            )
        )
        panel_source = self.driver.execute_script(
            "return document.querySelector('#device_panel_dialog_image img').src || '';"
        )
        with assume:
            assert panel_source.startswith("data:image/"), (
                "Device Panel equipment image should use a non-empty data:image source"
            )
        with assume:
            assert panel_source == status_source, (
                "Map Status equipment image and Device Panel image should be identical"
            )
        panel_image.screenshot(
            os.path.join(report_dir, f"EMS1-4361_{self.dutIp}_device_panel_image.png")
        )

        buttons = WebDriverWait(self.driver, 30).until(
            lambda driver: [
                button for button in driver.find_elements(
                    By.CSS_SELECTOR,
                    ".modal-xl .button",
                )
                if button.is_displayed() and button.is_enabled()
            ]
        )
        assert buttons, "Device Panel dialog should contain an enabled OK button"
        ok_button = next(
            (
                button for button in buttons
                if (
                    button.text.strip()
                    or (button.get_attribute("value") or "").strip()
                ).casefold() == "ok"
            ),
            buttons[0],
        )
        ok_button.click()
        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, "#device_panel_dialog_image img")
            )
        )


    # Map / Device / Power Supply Display
    @pytest.mark.Unicase
    def test_EMS1_4903_powerSupplyDisplay(self):
        report_dir = os.path.join(os.path.dirname(__file__), "report")
        dev_data, perf_data, paths, original_mibs = capture_restful_debug_files(
            self,
            report_dir,
        )
        assert isinstance(perf_data, dict), (
            f"Downloaded performance debug file is not a JSON object: "
            f"{paths[f'{self.dutIp}_perf']}"
        )
        hwinfo = dev_data.get("hwinfo")
        assert isinstance(hwinfo, dict), "RESTful dev JSON has no hwinfo object"
        power_entries = hwinfo.get("power")
        assert isinstance(power_entries, list) and power_entries, (
            "RESTful dev JSON hwinfo.power should be a non-empty list"
        )

        open_map_device_status(self.driver, self.dutNodeName, self.dutIp)
        status_image_path = os.path.join(
            report_dir,
            f"EMS1-4903_{self.dutIp}_status_device_image.png",
        )
        status_image_states, unsupported_reason = power_supply_image_states(
            self.driver,
            self.dutType,
            power_entries,
            status_image_path,
        )
        if unsupported_reason:
            pytest.skip(unsupported_reason)

        def compare_power_image(source_name, image_states):
            for index, (power, image_state) in enumerate(
                zip(power_entries, image_states),
                start=1,
            ):
                expected_status = str(power.get("status", "")).strip().casefold()
                expected_mode = str(power.get("mode", "")).strip().upper()
                with assume:
                    assert expected_mode == image_state["mode"], (
                        f"{source_name} Power Supply {index}: "
                        f"RESTful mode={expected_mode!r}, "
                        f"image profile mode={image_state['mode']!r}"
                    )
                with assume:
                    assert expected_status in {"up", "down"}, (
                        f"{source_name} Power Supply {index}: unsupported "
                        f"RESTful status {expected_status!r}"
                    )
                if expected_status in {"up", "down"}:
                    expected_up = expected_status == "up"
                    with assume:
                        assert image_state["is_up"] == expected_up, (
                            f"{source_name} Power Supply {index}: "
                            f"RESTful status={expected_status}, "
                            f"image LED is_up={image_state['is_up']}, "
                            f"green_pixels={image_state['green_pixels']}, "
                            f"centre={image_state['centre']}"
                        )
                print(
                    f"EMS1-4903 {source_name}: Power Supply {index}, "
                    f"mode={expected_mode}, RESTful status={expected_status}, "
                    f"image={image_state}",
                    flush=True,
                )

        compare_power_image("Map Status", status_image_states)

        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Device panel"))
        ).click()
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#device_panel_dialog_image img")
            )
        )
        panel_image_path = os.path.join(
            report_dir,
            f"EMS1-4903_{self.dutIp}_device_panel_image.png",
        )
        panel_image_states, panel_unsupported_reason = power_supply_image_states(
            self.driver,
            self.dutType,
            power_entries,
            panel_image_path,
            image_selector="#device_panel_dialog_image img",
        )
        assert not panel_unsupported_reason, panel_unsupported_reason
        compare_power_image("Device Panel", panel_image_states)

        for close_button in self.driver.find_elements(By.CSS_SELECTOR, ".modal-xl .button"):
            if close_button.is_displayed() and close_button.is_enabled():
                close_button.click()
                break

        print(
            f"EMS1-4903: RESTful files={paths}; original MIB values restored="
            f"{sorted(original_mibs)}",
            flush=True,
        )


    # Map / Device / ONT Status / Sort
    @pytest.mark.Unicase
    def test_EMS1_4363_ontStatusSort(self):
        table_id = "Dev_ontStatusTable"
        expected_statuses = [
            "In Service",
            "OOS-LO",
            "OOS-NR",
            "OOS-CD",
            "OOS-NP",
            "OOS-LS",
            "OOS-DG",
        ]

        open_map_device_status(self.driver, self.dutNodeName, self.dutIp)
        status_blocks = WebDriverWait(self.driver, 60).until(
            lambda driver: driver.find_elements(By.CSS_SELECTOR, "#ontStatus > div")
        )
        assert len(status_blocks) >= len(expected_statuses), (
            f"ONT Status should contain {expected_statuses}; "
            f"found only {len(status_blocks)} status blocks"
        )

        for status_index, expected_status in enumerate(expected_statuses, start=1):
            status_block = self.driver.find_element(
                By.XPATH, f"//div[@id='ontStatus']/div[{status_index}]"
            )
            status_text = " ".join(status_block.text.split())
            with assume:
                assert expected_status.casefold() in status_text.casefold(), (
                    f"ONT Status position {status_index} should be "
                    f"{expected_status!r}; actual={status_text!r}"
                )

            status_link = status_block.find_element(By.XPATH, ".//a")
            dashboard_count_text = status_link.text.strip()
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", status_link
            )
            status_link.click()
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.ID, f"{table_id}_body"))
            )
            WebDriverWait(self.driver, 60).until(
                lambda driver: total_data(driver, table_id) >= 0
            )
            table_total = total_data(self.driver, table_id)
            print(
                f"EMS1-4363: {expected_status} dashboard count="
                f"{dashboard_count_text}, table total={table_total}",
                flush=True,
            )

            if dashboard_count_text.isdigit():
                with assume:
                    assert int(dashboard_count_text) == table_total, (
                        f"{expected_status}: dashboard count "
                        f"{dashboard_count_text} != table total {table_total}"
                    )
            if table_total == 0:
                print(
                    f"EMS1-4363: skip {expected_status} sorting because Total data is 0",
                    flush=True,
                )
                continue

            columns = sortable_table_columns(self.driver, table_id)
            with assume:
                assert columns, f"No sortable columns found for {expected_status}"

            for column in columns:
                column_name = column["name"]
                column_label = column.get("label", column_name)
                column_index = column["index"]

                print(
                    f"EMS1-4363: {expected_status} column [{column_label}] "
                    "direction [descending]",
                    flush=True,
                )
                with assume:
                    click_table_sort_direction(
                        self.driver,
                        table_id,
                        column_index,
                        column_name,
                        descending=True,
                    )
                    assert_column_sorted_each_page(
                        self.driver,
                        table_id,
                        column_name,
                        descending=True,
                        context=(
                            f"{expected_status}/column [{column_label}]/"
                            "direction [descending]"
                        ),
                    )

                print(
                    f"EMS1-4363: {expected_status} column [{column_label}] "
                    "direction [ascending]",
                    flush=True,
                )
                with assume:
                    click_table_sort_direction(
                        self.driver,
                        table_id,
                        column_index,
                        column_name,
                        descending=False,
                    )
                    assert_column_sorted_each_page(
                        self.driver,
                        table_id,
                        column_name,
                        descending=False,
                        context=(
                            f"{expected_status}/column [{column_label}]/"
                            "direction [ascending]"
                        ),
                    )


    def _open_ont_status_table_for_dashboard_case(self):
        if not getattr(self, "_ont_dashboard_from_map_device", False):
            self.driver.find_element(By.LINK_TEXT, "Dashboard").click()
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//div[@id='ontStatus']/div[1]/div[2]/a"),
                )
            ).click()
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".comboTreeArrowBtnImg"))
            ).click()
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//label[contains(.,'{self.dutNodeName}')]"),
                )
            ).click()
            return "All_ontStatusTable"

        self.driver.find_element(By.LINK_TEXT, "Map").click()
        navside_icon = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.ID, "navside_icon"))
        )
        navside_icon.click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//*[@id='navMenuTree']/ul/li[contains(normalize-space(.), "
                    f"'{self.dutNodeName}')]",
                )
            )
        ).click()
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.ID, "Dev_ontStatusTable"))
        )
        if self.driver.find_element(By.ID, "navside_icon").is_displayed():
            self.driver.find_element(By.ID, "navside_icon").click()
        return "Dev_ontStatusTable"


    def _run_ont_dashboard_case_from_map_device(self, case_method):
        self._ont_dashboard_from_map_device = True
        try:
            return case_method(self)
        finally:
            self._ont_dashboard_from_map_device = False


    # Map / Device / ONT Status / ONT Dashboard / Run Script and ONT Status
    @pytest.mark.Unicase
    def test_EMS1_6107_6172_ontDashboardRunScriptOntStatusFromMapDevice(self):
        return self._run_ont_dashboard_case_from_map_device(
            _UnicaseCases.test_EMS1_6077_6885_ontDashboardRunScriptOntStatus
        )


    # Map / Device / ONT Status / ONT Dashboard / Reboot and Alarm Status
    @pytest.mark.Unicase
    def test_EMS1_6108_6171_ontDashboardRebootAlarmFromMapDevice(self):
        return self._run_ont_dashboard_case_from_map_device(
            _UnicaseCases.test_EMS1_6078_6884_ontDashboardRebootAlarm
        )


    # Map / Device / ONT Status / ONT Dashboard / DDMI
    @pytest.mark.Unicase
    def test_EMS1_6109_ontDashboardDdmiFromMapDevice(self):
        return self._run_ont_dashboard_case_from_map_device(
            _CustomCases.test_EMS1_6079_ontDashboardDdmi
        )


    # Map / Device / Alarm Status / Ack and Clear
    @pytest.mark.Unicase
    def test_EMS1_6156_6144_6145_deviceDashboardAlarmAckClear(self):
        open_map_device_status(self.driver, self.dutNodeName, self.dutIp)

        alarm_total = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@id='alarmStatus']/div[1]/div[2]/a"),
            )
        )
        if int(alarm_total.text) < 1:
            pytest.skip(
                f"EMS1-6156/6144/6145 requires at least one active alarm for "
                f"device {self.dutNodeName}"
            )

        alarm_total.click()
        main_window = self.driver.current_window_handle
        previous_windows = set(self.driver.window_handles)
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.ID, "dashboard_dev_alarm_card_more"))
        ).click()
        WebDriverWait(self.driver, 30).until(
            lambda _driver: len(set(_driver.window_handles) - previous_windows) == 1
        )
        alarm_window = (set(self.driver.window_handles) - previous_windows).pop()
        self.driver.switch_to.window(alarm_window)

        def alarm_row(index_1=None, index_2=None):
            if index_1 is None:
                xpath = "(//table[@id='alarm_activeTable_body']/tbody/tr)[1]"
            else:
                xpath = (
                    "//table[@id='alarm_activeTable_body']/tbody/tr"
                    f"[@index_1='{index_1}' and @index_2='{index_2}']"
                )
            return WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )

        def select_alarm(row):
            WebDriverWait(self.driver, 30).until(
                lambda _driver: row.find_element(By.XPATH, ".//label").is_enabled()
            )
            row.find_element(By.XPATH, ".//label").click()

        def accept_success():
            WebDriverWait(self.driver, 30).until(
                lambda _driver: "success" in _driver.find_element(
                    By.ID, "message_text"
                ).text.lower()
            )
            self.driver.find_element(By.CSS_SELECTOR, "#message_diag .button").click()

        try:
            device_ip_list = getListByCol(self, "alarm_activeTable", "DevIP")
            assert device_ip_list, "Device Active Alarm table should not be empty"
            unexpected_device_ips = sorted({
                device_ip for device_ip in device_ip_list
                if device_ip != self.dutIp
            })
            with assume:
                assert not unexpected_device_ips, (
                    f"Device Active Alarm table should contain only {self.dutIp}; "
                    f"unexpected Device IP values: {unexpected_device_ips}"
                )

            target_row = alarm_row()
            index_1 = target_row.get_attribute("index_1")
            index_2 = target_row.get_attribute("index_2")
            assert index_1 and index_2, (
                "Active alarm row should expose index_1/index_2. "
                f"index_1={index_1}, index_2={index_2}"
            )

            select_alarm(target_row)
            self.driver.find_element(By.CSS_SELECTOR, "#i_action_ack > a").click()
            accept_success()

            target_row = alarm_row(index_1, index_2)
            select_alarm(target_row)
            clear_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            self.driver.find_element(By.CSS_SELECTOR, "#i_action_clear > a").click()
            clear_note = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.ID, "alarm_clear_note_text"))
            )
            clear_note.send_keys(f"$py_clearTime: {clear_time}")
            self.driver.find_element(By.ID, "alarm_clear_note_save_btn").click()
            accept_success()

            cleared_alarm_xpath = (
                "//table[@id='alarm_activeTable_body']/tbody/tr"
                f"[@index_1='{index_1}' and @index_2='{index_2}']"
            )
            WebDriverWait(self.driver, 30).until(
                lambda _driver: not _driver.find_elements(By.XPATH, cleared_alarm_xpath)
            )
        finally:
            self.driver.close()
            self.driver.switch_to.window(main_window)


    # Map / Device / Hardware Monitor
    @pytest.mark.Unicase
    def test_EMS1_4362_4398_deviceHwMonitor(self):
        ansi_escape = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")

        def clean_cli(output):
            return ansi_escape.sub("", output).replace("\r", "")

        reset_transcript = clean_cli(run_ssh_commands(
            self.dutIp,
            self.dutAdminName,
            self.dutAdminPwd,
            ["configure", "no hw-monitor", "exit"],
        ))
        assert not re.search(
            r"(?:invalid|error|out of range)", reset_transcript, re.I
        ), f"Failed to reset hardware monitor settings: {reset_transcript}"

        def read_hw_monitor(slot):
            transcript = clean_cli(run_ssh_commands(
                self.dutIp,
                self.dutAdminName,
                self.dutAdminPwd,
                [f"show hw-monitor {slot}", f"show hw-monitor statistics {slot}"],
            ))
            definitions = []
            definition_pattern = re.compile(
                r"^\s*(Temperature|Voltage)\s+(\S+)\s+\S+\s+(.+?)\s+"
                r"(\d+)\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\((C|mV)\)\s*$",
                re.MULTILINE,
            )
            for match in definition_pattern.finditer(transcript):
                definitions.append({
                    "kind": match.group(1).lower(),
                    "cardtype": match.group(2),
                    "name": " ".join(match.group(3).split()),
                    "index": int(match.group(4)),
                    "high": int(float(match.group(5))),
                    "low": int(float(match.group(6))),
                    "unit": match.group(7),
                })

            statistics = {}
            for line in transcript.splitlines():
                fields = re.split(r"\s{2,}", line.strip())
                if len(fields) != 8 or not re.search(r"\((?:C|mV)\)$", fields[-1]):
                    continue
                current_match = re.match(r"(-?\d+(?:\.\d+)?)", fields[-1])
                if current_match:
                    statistics[(fields[0], " ".join(fields[2].split()))] = float(
                        current_match.group(1)
                    )

            for definition in definitions:
                key = (definition["cardtype"], definition["name"])
                assert key in statistics, (
                    f"show hw-monitor statistics {slot} has no Current value for {key}"
                )
                definition["current"] = statistics[key]
            assert definitions, f"No Temperature or Voltage monitor found in slot {slot}"
            return definitions

        def threshold_command(slot, monitor, high, low):
            if monitor["cardtype"].casefold() in {"genni", "nni"}:
                return (
                    f"hw-monitor {monitor['kind']}-threshold "
                    f"{monitor['index']} {high} {low}"
                )
            return (
                f"hw-monitor {monitor['kind']}-threshold cardtype "
                f"{monitor['cardtype']} slot {slot} {monitor['index']} {high} {low}"
            )

        def configure_threshold(slot, monitor, high, low):
            transcript = clean_cli(run_ssh_commands(
                self.dutIp,
                self.dutAdminName,
                self.dutAdminPwd,
                ["configure", threshold_command(slot, monitor, high, low), "exit"],
            ))
            assert not re.search(r"(?:invalid|error|out of range)", transcript, re.I), (
                f"Threshold command failed for slot {slot}, {monitor['name']}: {transcript}"
            )

        def restore_thresholds(slot, monitors):
            if not monitors:
                return
            commands = ["configure"] + [
                threshold_command(slot, monitor, monitor["high"], monitor["low"])
                for monitor in monitors
            ] + ["exit"]
            transcript = clean_cli(run_ssh_commands(
                self.dutIp,
                self.dutAdminName,
                self.dutAdminPwd,
                commands,
            ))
            assert not re.search(r"(?:invalid|error|out of range)", transcript, re.I), (
                f"Failed to restore hardware thresholds for slot {slot}: {transcript}"
            )

        def icon_state(icon):
            return self.driver.execute_script(
                """
                const element = arguments[0];
                const style = getComputedStyle(element);
                const before = getComputedStyle(element, "::before");
                return {
                    className: Array.from(element.classList)
                        .filter(name => name !== "item_select")
                        .sort()
                        .join(" "),
                    backgroundImage: style.backgroundImage,
                    color: style.color,
                    beforeColor: before.color,
                    beforeBackgroundImage: before.backgroundImage,
                };
                """,
                icon,
            )

        def icon_and_status(kind):
            icon = WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(
                    (By.ID, f"dashboard_hw_status_{kind}_image")
                )
            )
            icon.click()
            warning_container = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.ID, "hw_warning"))
            )
            status = warning_container.text.strip()
            return icon, status

        def refresh_and_read(kind):
            WebDriverWait(self.driver, 60).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "#i_action_refresh > a")
                )
            ).click()
            time.sleep(3)
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located(
                    (By.ID, f"dashboard_hw_status_{kind}_image")
                )
            )
            return icon_and_status(kind)

        last_warning_check = {}

        def warning_ready(kind, expected):
            try:
                icon, status = refresh_and_read(kind)
                last_warning_check.clear()
                last_warning_check.update({
                    "kind": kind,
                    "status": status,
                    "expected": expected,
                    "reason": "checking",
                })
                warning_pattern = re.compile(
                    r"^\s*Slot\s+(\S+)\s*,\s*(.+?)\s*,\s*"
                    r"(too\s+high(?:t)?|too\s+low)\.\s*"
                    r"Current\s+value\s+(-?\d+(?:\.\d+)?)\s*"
                    r"\(\s*([^)]*?)\s*\)\s*"
                    r"Threshold\s+(-?\d+(?:\.\d+)?)\s*"
                    r"\(\s*([^)]*?)\s*\)\s*$",
                    re.I | re.MULTILINE,
                )
                warnings = []
                for match in warning_pattern.finditer(status):
                    warnings.append({
                        "slot": match.group(1),
                        "name": " ".join(match.group(2).split()),
                        "direction": "high" if "high" in match.group(3).casefold() else "low",
                        "current": float(match.group(4)),
                        "current_unit": re.sub(r"[^A-Za-z]", "", match.group(5)),
                        "threshold": float(match.group(6)),
                        "threshold_unit": re.sub(r"[^A-Za-z]", "", match.group(7)),
                    })
                unused_warning_indexes = set(range(len(warnings)))
                for item in expected:
                    tolerance = 5 if kind == "temperature" else max(
                        100, abs(item["current"]) * 0.05
                    )
                    matching_indexes = [
                        index for index in unused_warning_indexes
                        if warnings[index]["slot"] == str(item["slot"])
                        and warnings[index]["direction"] == item["direction"]
                        and warnings[index]["threshold"] == float(item["threshold"])
                        and abs(warnings[index]["current"] - item["current"]) <= tolerance
                        and warnings[index]["current_unit"].casefold() == item["unit"].casefold()
                        and warnings[index]["threshold_unit"].casefold() == item["unit"].casefold()
                        and (
                            kind == "voltage"
                            or warnings[index]["name"].casefold() == item["name"].casefold()
                        )
                    ]
                    if not matching_indexes:
                        last_warning_check["reason"] = (
                            f"no single warning row matched {item}; parsed={warnings}"
                        )
                        return False
                    unused_warning_indexes.remove(matching_indexes[0])
                last_warning_check["reason"] = "matched"
                return {"icon_state": icon_state(icon), "status": status}
            except Exception as error:
                last_warning_check.clear()
                last_warning_check.update({
                    "kind": kind,
                    "expected": expected,
                    "reason": f"{type(error).__name__}: {error}",
                })
                return False

        def wait_for_warning(kind, expected):
            try:
                return WebDriverWait(
                    self.driver, 180, poll_frequency=10
                ).until(lambda _driver: warning_ready(kind, expected))
            except TimeoutException as error:
                raise AssertionError(
                    f"Hardware warning did not match: {last_warning_check}"
                ) from error

        def normal_ready(kind):
            try:
                icon, status = refresh_and_read(kind)
                return (
                    f"icon_hwstatus_{kind}_normal" in (icon.get_attribute("class") or "")
                    and status.strip() == "Normal"
                )
            except Exception:
                return False

        def abnormal_thresholds(monitor, direction):
            current = monitor["current"]
            margin = 3 if monitor["kind"] == "temperature" else max(
                5, int(abs(current) * 0.01)
            )
            if direction == "low":
                high = monitor["high"]
                floor_current = int(current // 1)
                low = min(floor_current + margin, high - 1)
                if not high > low > current:
                    return None
            else:
                low = monitor["low"]
                ceil_current = int(-(-current // 1))
                high = max(ceil_current - margin, low + 1)
                if not current > high > low:
                    return None
            return high, low

        open_map_device_status(self.driver, self.dutNodeName, self.dutIp)
        for kind in ("cpu", "memory", "fan"):
            icon, status = icon_and_status(kind)
            with assume:
                assert f"icon_hwstatus_{kind}_" in (
                    icon.get_attribute("class") or ""
                ), f"{kind} hardware status icon is not rendered correctly"
            with assume:
                assert status.strip(), f"{kind} hardware status text is empty"

        normal_icon_states = {}
        for kind in ("temperature", "voltage"):
            icon = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (By.ID, f"dashboard_hw_status_{kind}_image")
                )
            )
            normal_icon_states[kind] = icon_state(icon)

        slots = [slot for slot in self.dutAllCardID if slot not in {"0", "--"}]
        assert slots, f"No testable card slot is configured for {self.dutName}"

        for slot in slots:
            monitors = read_hw_monitor(slot)
            for kind in ("temperature", "voltage"):
                kind_monitors = [item for item in monitors if item["kind"] == kind]
                if not kind_monitors:
                    continue

                changed = []
                try:
                    expected_warnings = []
                    for monitor in kind_monitors:
                        thresholds = abnormal_thresholds(monitor, "low")
                        if thresholds is None:
                            print(
                                f"EMS1-4362_4398 skip {kind} {monitor['name']} too low: "
                                f"no integer threshold satisfies "
                                f"{monitor['high']} > low > {monitor['current']}",
                                flush=True,
                            )
                            continue
                        high, low = thresholds
                        changed.append(monitor)
                        configure_threshold(slot, monitor, high, low)
                        expected_warnings.append({
                            "slot": slot,
                            "name": monitor["name"],
                            "direction": "low",
                            "current": monitor["current"],
                            "threshold": low,
                            "unit": monitor["unit"],
                        })
                        try:
                            warning_result = wait_for_warning(
                                kind, expected_warnings
                            )
                        except AssertionError as error:
                            with assume:
                                assert False, str(error)
                            continue
                        with assume:
                            assert warning_result["icon_state"] != normal_icon_states[kind], (
                                f"{kind} icon did not change from the normal appearance. "
                                f"normal={normal_icon_states[kind]}, "
                                f"current={warning_result['icon_state']}, "
                                f"status={warning_result['status']}"
                            )
                finally:
                    restore_thresholds(slot, changed)
                WebDriverWait(
                    self.driver, 180, poll_frequency=10
                ).until(lambda _driver: normal_ready(kind))

                changed = []
                try:
                    expected_warnings = []
                    for monitor in kind_monitors:
                        thresholds = abnormal_thresholds(monitor, "high")
                        if thresholds is None:
                            print(
                                f"EMS1-4362_4398 skip {kind} {monitor['name']} too high: "
                                f"no integer threshold satisfies "
                                f"{monitor['current']} > high > {monitor['low']}",
                                flush=True,
                            )
                            continue
                        high, low = thresholds
                        changed.append(monitor)
                        configure_threshold(slot, monitor, high, low)
                        expected_warnings.append({
                            "slot": slot,
                            "name": monitor["name"],
                            "direction": "high",
                            "current": monitor["current"],
                            "threshold": high,
                            "unit": monitor["unit"],
                        })
                        try:
                            warning_result = wait_for_warning(
                                kind, expected_warnings
                            )
                        except AssertionError as error:
                            with assume:
                                assert False, str(error)
                            continue
                        with assume:
                            assert warning_result["icon_state"] != normal_icon_states[kind], (
                                f"{kind} icon did not change from the normal appearance. "
                                f"normal={normal_icon_states[kind]}, "
                                f"current={warning_result['icon_state']}, "
                                f"status={warning_result['status']}"
                            )
                finally:
                    restore_thresholds(slot, changed)
                WebDriverWait(
                    self.driver, 180, poll_frequency=10
                ).until(lambda _driver: normal_ready(kind))


    # Dashboard / Alarm Status / Ack Clear Access Log
    @pytest.mark.Unicase
    def test_EMS1_6201_dashboardAlarmAckClearLog(self):
        self.driver.find_element(By.LINK_TEXT, "Dashboard").click()
        alarm_total = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@id='alarmStatus']/div[1]/div[2]/a"),
            )
        )
        if int(alarm_total.text) < 1:
            pytest.skip("EMS1-6201 requires at least one Dashboard active alarm")

        alarm_total.click()
        main_window = self.driver.current_window_handle
        previous_windows = set(self.driver.window_handles)
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.ID, "dashboard_all_alarm_card_more"))
        ).click()
        WebDriverWait(self.driver, 30).until(
            lambda _driver: len(set(_driver.window_handles) - previous_windows) == 1
        )
        alarm_window = (set(self.driver.window_handles) - previous_windows).pop()
        self.driver.switch_to.window(alarm_window)

        def active_alarm_row(index_1=None, index_2=None):
            if index_1 is None:
                xpath = "(//table[@id='alarm_activeTable_body']/tbody/tr)[1]"
            else:
                xpath = (
                    "//table[@id='alarm_activeTable_body']/tbody/tr"
                    f"[@index_1='{index_1}' and @index_2='{index_2}']"
                )
            return WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )

        def select_alarm(row):
            row.find_element(By.XPATH, ".//label").click()

        def accept_success():
            WebDriverWait(self.driver, 30).until(
                lambda _driver: "success" in _driver.find_element(
                    By.ID, "message_text"
                ).text.lower()
            )
            self.driver.find_element(By.CSS_SELECTOR, "#message_diag .button").click()

        try:
            target_row = active_alarm_row()
            index_1 = target_row.get_attribute("index_1")
            index_2 = target_row.get_attribute("index_2")
            assert index_1 and index_2, (
                f"Active alarm row should expose index_1/index_2. "
                f"index_1={index_1}, index_2={index_2}"
            )

            select_alarm(target_row)
            ack_time = datetime.now()
            self.driver.find_element(By.CSS_SELECTOR, "#i_action_ack > a").click()
            accept_success()

            target_row = active_alarm_row(index_1, index_2)
            select_alarm(target_row)
            clear_time = datetime.now()
            self.driver.find_element(By.CSS_SELECTOR, "#i_action_clear > a").click()
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.ID, "alarm_clear_note_save_btn"))
            ).click()
            accept_success()
        finally:
            self.driver.close()
            self.driver.switch_to.window(main_window)

        ack_description = (
            "[Alarm - acknowledge alarm] set success "
            f"(acknowledge one alarm - (id,subid)=({index_1},{index_2}))"
        )
        clear_description = (
            "[Alarm - clear alarm] set success "
            f"(clear one alarm - (id,subid)=({index_1},{index_2}))"
        )
        query_from = (ack_time - timedelta(seconds=15)).strftime(self.dateFormat)
        query_to = (clear_time + timedelta(seconds=45)).strftime(self.dateFormat)

        self.driver.find_element(By.LINK_TEXT, "System").click()
        self.driver.find_element(By.LINK_TEXT, "Security").click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.ID, "access_log_browse"))
        ).click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#i_action_filter > a"))
        ).click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='filter_background']/div[2]/input[@value='Reset']"),
            )
        ).click()

        from_field = self.driver.find_element(By.ID, "accesslog_datepickerFrom_filter")
        from_field.clear()
        from_field.send_keys(query_from)
        self.driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-close").click()
        to_field = self.driver.find_element(By.ID, "accesslog_datepickerTo_filter")
        to_field.clear()
        to_field.send_keys(query_to)
        self.driver.find_element(By.CSS_SELECTOR, ".ui-datepicker-close").click()
        self.driver.find_element(By.ID, "accesslog_query_button").click()

        def both_access_logs_exist(_driver):
            descriptions = [
                cell.text
                for cell in _driver.find_elements(
                    By.XPATH,
                    "//table[@id='accessLog_table_body']/tbody/tr/td/a",
                )
            ]
            return ack_description in descriptions and clear_description in descriptions

        WebDriverWait(self.driver, 60, poll_frequency=2).until(both_access_logs_exist)
        with assume:
            assert getPositionByCol(
                self, "accessLog_table", "Description", ack_description
            ) != [-1, -1], (
                f"Ack Access Log not found between {query_from} and {query_to}"
            )
        with assume:
            assert getPositionByCol(
                self, "accessLog_table", "Description", clear_description
            ) != [-1, -1], (
                f"Clear Access Log not found between {query_from} and {query_to}"
            )


    # Dashboard / ONT Status / ONT Dashboard / DDMI
    @pytest.mark.Unicase
    def test_EMS1_6079_ontDashboardDdmi(self):
        self.driver.find_element(By.LINK_TEXT, "Dashboard").click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@id='ontStatus']/div[1]/div[2]/a"),
            )
        ).click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".comboTreeArrowBtnImg"))
        ).click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//label[contains(.,'{self.dutNodeName}')]"),
            )
        ).click()

        main_window = self.driver.current_window_handle
        for index in range(self.ontCount):
            ont_aid = (
                f"{self.ontSlotIDList[index]}-"
                f"{self.ontPortIDList[index]}-"
                f"{self.ontOntIDList[index]}"
            )
            previous_windows = set(self.driver.window_handles)
            getPositionByColsAndClickNext(
                self,
                "All_ontStatusTable",
                {"sn": self.ontSNList[index]},
            )
            WebDriverWait(self.driver, 30).until(
                lambda _driver: len(set(_driver.window_handles) - previous_windows) == 1
            )
            ont_window = (set(self.driver.window_handles) - previous_windows).pop()
            self.driver.switch_to.window(ont_window)
            try:
                WebDriverWait(self.driver, 30).until(
                    EC.text_to_be_present_in_element(
                        (By.ID, "dashboard_ont_title_ontid"),
                        self.ontOntIDList[index],
                    )
                )

                def ddmi_charts_ready(_driver):
                    try:
                        return ont_dashboard_ddmi_chart_data(_driver)
                    except AssertionError:
                        return False

                charts = WebDriverWait(
                    self.driver,
                    120,
                    poll_frequency=1,
                ).until(ddmi_charts_ready)
                dataset_count = assert_ont_dashboard_ddmi_charts_valid(charts)
                print(
                    f"EMS1-6079: ONT {ont_aid} DDMI charts={len(charts)}, "
                    f"datasets={dataset_count}, data={charts}",
                    flush=True,
                )
            finally:
                self.driver.close()
                self.driver.switch_to.window(main_window)


    # Map / Device Card Tree Fold
    @pytest.mark.Unicase
    def test_EMS1_6123_cardTreeFold(self):
        if "OLT14" in self.dutType.upper():
            pytest.skip("EMS1-6123 is not supported on the OLT14xx series")

        self.driver.find_element(By.LINK_TEXT, "Map").click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.ID, "navside_icon"))
        ).click()

        device_xpath = (
            "//*[@id='navMenuTree']/ul/li[contains(@class,'node-navMenuTree') "
            f"and contains(normalize-space(.), '{self.dutNodeName}')]"
        )
        device = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, device_xpath))
        )
        device_node_id = int(device.get_attribute("data-nodeid"))
        device.click()
        expected_cards = {
            device_node_id + int(slot_id): f"{slot_id} - {card_type}"
            for slot_id, card_type in zip(self.dutAllCardID, self.cardTypeName)
            if slot_id not in ("0", "--")
        }
        assert expected_cards, f"No card is configured for device {self.dutNodeName}"

        expand_icon = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, device_xpath + "/span[contains(@class,'expand-icon')]"),
            )
        )
        if "oi-plus" in (expand_icon.get_attribute("class") or ""):
            expand_icon.click()

        def all_cards_expanded(_driver):
            for card_node_id, expected_text in expected_cards.items():
                cards = _driver.find_elements(
                    By.XPATH,
                    f"//*[@id='navMenuTree']/ul/li[@data-nodeid='{card_node_id}']",
                )
                if not cards or not cards[0].is_displayed() or cards[0].text != expected_text:
                    return False
            return True

        WebDriverWait(self.driver, 30, poll_frequency=0.2).until(all_cards_expanded)

        collapse_icon = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, device_xpath + "/span[contains(@class,'expand-icon') and contains(@class,'oi-minus')]"),
            )
        )
        collapse_icon.click()

        def all_cards_folded(_driver):
            return all(
                not any(card.is_displayed() for card in _driver.find_elements(
                    By.XPATH,
                    f"//*[@id='navMenuTree']/ul/li[@data-nodeid='{card_node_id}']",
                ))
                for card_node_id in expected_cards
            )

        WebDriverWait(self.driver, 30, poll_frequency=0.2).until(all_cards_folded)


    # Map / Navigation Side Icon
    @pytest.mark.Unicase
    def test_EMS1_5105_navsideIconIts(self):
        expanded_style = (
            'background-image: url("resources/images/i_action_left_arrow.png"); '
            'margin-left: 18.7%;'
        )
        collapsed_style = (
            'background-image: url("resources/images/i_action_right_arrow.png"); '
            'margin-left: calc(0px);'
        )

        self.driver.find_element(By.LINK_TEXT, "Map").click()
        navside_icon = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.ID, "navside_icon"))
        )
        navside_icon.click()
        WebDriverWait(self.driver, 30, poll_frequency=0.2).until(
            lambda _driver: _driver.find_element(By.ID, "navside_icon").get_dom_attribute("style")
            == expanded_style
        )

        self.driver.find_element(By.ID, "navside_icon").click()
        WebDriverWait(self.driver, 30, poll_frequency=0.2).until(
            lambda _driver: _driver.find_element(By.ID, "navside_icon").get_dom_attribute("style")
            == collapsed_style
        )


    # Map / Device / Remote Control
    @pytest.mark.Unicase
    def test_EMS1_5180_hostnameRemoteControlIts(self):
        temporary_hostname = "SNET-RCPD-OLT"
        original_hostname = self.dutName
        hostname_restored = False

        def console_text():
            return "\n".join(
                row.text for row in self.driver.find_elements(By.CSS_SELECTOR, "#console p")
            )

        def send_remote_command(command):
            command_field = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.ID, "manual_script_text"))
            )
            previous_text = console_text()
            command_field.click()
            command_field.send_keys(command)
            command_field.send_keys(Keys.ENTER)
            WebDriverWait(self.driver, 30, poll_frequency=0.5).until(
                lambda _driver: console_text() != previous_text
            )

        try:
            run_ssh_commands(
                self.dutIp,
                self.dutAdminName,
                self.dutAdminPwd,
                ["configure", f"hostname {temporary_hostname}"],
            )

            open_map_device_status(self.driver, self.dutNodeName, self.dutIp)
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Remote Control"))
            ).click()
            WebDriverWait(self.driver, 120, poll_frequency=0.5).until(
                lambda _driver: temporary_hostname in console_text()
            )

            send_remote_command("configure")
            send_remote_command(f"hostname {original_hostname}")
            WebDriverWait(self.driver, 60, poll_frequency=0.5).until(
                lambda _driver: original_hostname in console_text()
            )
            hostname_restored = True
        finally:
            if not hostname_restored:
                try:
                    run_ssh_commands(
                        self.dutIp,
                        self.dutAdminName,
                        self.dutAdminPwd,
                        ["configure", f"hostname {original_hostname}"],
                    )
                except Exception as restore_error:
                    print(f"EMS1-5180: SSH hostname restore failed: {restore_error}", flush=True)
'@)

$allBaseClasses = @("_IcatCases", "_RestfulCases", "_ProvisionCases", "_UnicaseCases") + $newMixinClasses + @("_CustomCases")
$baseClassText = $allBaseClasses -join ", "
$newCaseMapText = $newCaseMapEntries -join "`r`n"
$mergedParts.Add(@"

# Pytest only collects this unified class. Each case keeps its source marker,
# which selects the matching configuration and browser lifecycle implementation.
class TestGlobalCase(${baseClassText}):
    _new_case_mixins = {
${newCaseMapText}
    }

    @pytest.fixture(autouse=True, scope="function")
    def _global_case_setup(self, request, test_config):
        case_name = getattr(request.node, "originalname", None)
        if not case_name:
            case_name = request.node.name.split("[", 1)[0]
        new_case_setup = self._new_case_mixins.get(case_name)
        if new_case_setup is not None:
            mixin, setup_method_name = new_case_setup
            for key, value in vars(test_config).items():
                setattr(type(self), key, value)
            browser_lifecycle = getattr(mixin, setup_method_name)(self)
            next(browser_lifecycle)
            try:
                yield
            finally:
                try:
                    next(browser_lifecycle)
                except StopIteration:
                    pass
            return

        source_mixins = {
            "Icat": _IcatCases,
            "Restful": _RestfulCases,
            "Provision": _ProvisionCases,
            "Unicase": _UnicaseCases,
        }
        source_type = next(
            (name for name in source_mixins if request.node.get_closest_marker(name)),
            None,
        )
        if source_type is None:
            raise RuntimeError(f"Case {request.node.name} 沒有來源 marker")

        mixin = source_mixins[source_type]
        if source_type == "Restful":
            cls = type(self)
            if not getattr(cls, "_restful_config_ready", False):
                mixin._inject_config(self, request, test_config)
                cls._restful_config_ready = True
            browser_lifecycle = mixin.setup_browser(self, request, None)
        else:
            mixin._inject_config(self, request, test_config)
            browser_lifecycle = mixin.setup_browser(self, request)

        next(browser_lifecycle)
        try:
            yield
        finally:
            try:
                next(browser_lifecycle)
            except StopIteration:
                pass
"@)

$mergedContent = $mergedParts -join "`r`n"
$mergedContent = $mergedContent.Replace(
    "    wait_for_chart_with_frontend_data,",
    "    wait_for_chart_with_frontend_data,`r`n    wait_for_chart_title,"
)
$mergedContent = $mergedContent.Replace(
@'
            time.sleep(120)
            assert current_iframe_count(self.driver) >= 1
            accumulation_values = wait_for_chart_with_frontend_data(self.driver, accumulation_title)
            print(f"EMS1-4515: Interface(Accumulation) frontend data: {accumulation_values}")
'@,
@'
            accumulation_chart = wait_for_chart_title(self.driver, accumulation_title, expected_count=1)
            assert current_iframe_count(self.driver) >= 1
            print(f"EMS1-4515: Interface(Accumulation) chart appeared: {accumulation_chart['title']}")
'@
)
$mergedContent = $mergedContent.Replace(
@'
            time.sleep(120)
            assert current_iframe_count(self.driver) >= 2
            rate_values = wait_for_chart_with_frontend_data(self.driver, rate_title)
            print(f"EMS1-4515: Interface(Rate) frontend data: {rate_values}")
'@,
@'
            rate_chart = wait_for_chart_title(self.driver, rate_title, expected_count=2)
            assert current_iframe_count(self.driver) >= 2
            print(f"EMS1-4515: Interface(Rate) chart appeared: {rate_chart['title']}")
'@
)
$mergedContent = $mergedContent.Replace(
    "def test_EMS1_4369_alarmStatus(self):",
    "def test_EMS1_4369_6147_alarmStatusExport(self):"
)
$dashboardNavigation = @'
        self.driver.find_element(By.LINK_TEXT, "Dashboard").click()
        time.sleep(3)
        self.driver.find_element(By.XPATH, "//div[@id=\'ontStatus\']/div[1]/div[2]/a").click()
        self.driver.find_element(By.CSS_SELECTOR, ".comboTreeArrowBtnImg").click()
        self.driver.find_element(By.XPATH, "//label[contains(.,\'" + self.dutNodeName + "\')]").click()
        time.sleep(3)
'@
$dashboardWaitNavigation = @'
        self.driver.find_element(By.LINK_TEXT, "Dashboard").click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@id='ontStatus']/div[1]/div[2]/a"),
            )
        ).click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".comboTreeArrowBtnImg"))
        ).click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//label[contains(.,'{self.dutNodeName}')]")
            )
        ).click()
'@
$ontDashboardCasePattern = '(?ms)^    def (?<name>test_EMS1_(?:6077_6885_ontDashboardRunScriptOntStatus|6078_6884_ontDashboardRebootAlarm|6079_ontDashboardDdmi))\(self\):.*?(?=^    (?:async\s+)?def test_EMS1_|^class TestGlobalCase)'
$mergedContent = [regex]::Replace($mergedContent, $ontDashboardCasePattern, {
    param($caseMatch)
    $caseBody = $caseMatch.Value
    $caseBody = $caseBody.Replace($dashboardNavigation, "        ontDashboardTable = self._open_ont_status_table_for_dashboard_case()`r`n")
    $caseBody = $caseBody.Replace($dashboardWaitNavigation, "        ontDashboardTable = self._open_ont_status_table_for_dashboard_case()`r`n")
    $caseBody = [regex]::Replace(
        $caseBody,
        '(?s)        self\.driver\.find_element\(By\.LINK_TEXT, "Dashboard"\)\.click\(\).*?(?=        (?:p=|main_window =))',
        "        ontDashboardTable = self._open_ont_status_table_for_dashboard_case()`r`n",
        1
    )
    $caseBody = $caseBody.Replace('"All_ontStatusTable"', 'ontDashboardTable')
    return $caseBody
})
$dashboardDeviceStatusPattern = '(?s)(?<prefix>    def test_EMS1_3489_4343_5038_5179_dashboardDeviceStatus\(self\):\r?\n).*?(?=        #Check click the device can switch to map page)'
$dashboardDeviceStatusReplacement = '${prefix}' + @'
        self.driver.find_element(By.LINK_TEXT, "Dashboard").click()
        WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.ID, "devStatus"))
        )

        # Read both changing values in one browser-side snapshot. Do not poll or
        # compare with the earlier Inventory snapshot because the live data may move.
        for status in range(self.deviceStatusCount):
            status_index = status + 1
            self.driver.find_element(
                By.XPATH,
                f"//div[@id='devStatus']/div[{status_index}]/div[2]/a",
            ).click()
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (By.ID, "table_total_data_All_devStatusTable")
                )
            )
            time.sleep(2)
            counts = self.driver.execute_script(
                """
                const statusIndex = arguments[0];
                const dashboard = document.evaluate(
                    `//div[@id='devStatus']/div[${statusIndex}]/div[2]/a`,
                    document,
                    null,
                    XPathResult.FIRST_ORDERED_NODE_TYPE,
                    null
                ).singleNodeValue;
                const tableTotal = document.getElementById(
                    "table_total_data_All_devStatusTable"
                );
                return {
                    dashboard: dashboard ? dashboard.textContent.trim() : "",
                    table: tableTotal
                        ? tableTotal.textContent.replace("Total data:", "").trim()
                        : "",
                };
                """,
                status_index,
            )
            with assume:
                assert counts["dashboard"] == counts["table"], (
                    f"Device Status count mismatch for index {status_index}: "
                    f"dashboard={counts['dashboard']}, table={counts['table']}"
                )
'@
$dashboardDeviceStatusReplacement += "`r`n"
if ([regex]::Matches($mergedContent, $dashboardDeviceStatusPattern).Count -ne 1) {
    throw "Dashboard Device Status count block was not found exactly once"
}
$mergedContent = [regex]::Replace(
    $mergedContent,
    $dashboardDeviceStatusPattern,
    $dashboardDeviceStatusReplacement,
    1
)
$mergedContent = $mergedContent.Replace(
    "from libs.report import *",
    "from libs.report import *`r`nfrom libs.export_table_compare import capture_table_and_export, assert_export_matches"
)
$inventoryDeviceSnapshotPattern = '(?s)(?<casePrefix>    def test_EMS1_3579_3516_deviceInfo\(self\):.*?        self\.driver\.find_element\(By\.LINK_TEXT, "Device"\)\.click\(\)\r?\n        time\.sleep\(3\)\r?\n)        minTime = datetime\.now\(\)\r?\n        self\.driver\.find_element\(By\.CSS_SELECTOR, "#i_action_export > a"\)\.click\(\)'
$inventoryDeviceSnapshotReplacement = '${casePrefix}' + @'
        exportColumnMap = (
            ("SubmapName", "Submap Name"),
            ("DevName", "Device Name"),
            ("IPAddress", "IP Address"),
            ("DevType", "Device Type"),
            ("DevStatus", "Operational Status"),
            ("BootFwVersion", "Bootup FW Version"),
            ("FwVersion1", "Image1 FW Version"),
            ("FwVersion2", "Image2 FW Version"),
            ("DevAlarmStatus", "Alarm Status"),
            ("Contact", "Contact"),
            ("Location", "Location"),
        )
        normalizeDeviceValue = lambda value: " ".join(value.split())
        minTime = datetime.now()
        inventoryDeviceRows = self.driver.execute_script(
            """
            const columnNames = arguments[0];
            const headers = Array.from(document.querySelectorAll(
                "#dev_inventory_div_head thead tr th"
            ));
            const indexes = columnNames.map((name) =>
                headers.findIndex((header) => header.getAttribute("name") === name)
            );
            if (indexes.some((index) => index < 0)) {
                throw new Error("Inventory Device column not found: " +
                    columnNames.filter((_, index) => indexes[index] < 0).join(", "));
            }
            const rows = Array.from(document.querySelectorAll(
                "#dev_inventory_div_body tbody tr"
            )).map((row) => {
                const cells = Array.from(row.querySelectorAll(":scope > td"));
                return indexes.map((index) => cells[index].innerText);
            });
            document.querySelector("#i_action_export > a").click();
            return rows;
            """,
            [tableColumn for tableColumn, _ in exportColumnMap],
        )
        inventoryDeviceRows = [
            tuple(
                "" if normalizeDeviceValue(value) == "--" else normalizeDeviceValue(value)
                for value in row
            )
            for row in inventoryDeviceRows
        ]
'@
if ([regex]::Matches($mergedContent, $inventoryDeviceSnapshotPattern).Count -ne 1) {
    throw "Inventory Device export snapshot insertion point not found"
}
$mergedContent = [regex]::Replace(
    $mergedContent,
    $inventoryDeviceSnapshotPattern,
    $inventoryDeviceSnapshotReplacement,
    1
)

$inventoryDeviceComparePattern = '(?s)(?<caseBody>    def test_EMS1_3579_3516_deviceInfo\(self\):.*?        with assume: assert minTime <= latestFileTime <= maxTime)'
$inventoryDeviceCompareReplacement = '${caseBody}' + @'


        from collections import Counter
        from html.parser import HTMLParser

        class DeviceExportParser(HTMLParser):
            def __init__(self):
                super().__init__(convert_charrefs=True)
                self.rows = []
                self.currentRow = None
                self.currentCell = None

            def handle_starttag(self, tag, attrs):
                if tag.lower() == "tr":
                    self.currentRow = []
                elif tag.lower() == "td" and self.currentRow is not None:
                    self.currentCell = []

            def handle_data(self, data):
                if self.currentCell is not None:
                    self.currentCell.append(data)

            def handle_endtag(self, tag):
                if tag.lower() == "td" and self.currentCell is not None:
                    self.currentRow.append(normalizeDeviceValue("".join(self.currentCell)))
                    self.currentCell = None
                elif tag.lower() == "tr" and self.currentRow is not None:
                    self.rows.append(self.currentRow)
                    self.currentRow = None

        deviceExportParser = DeviceExportParser()
        with open(latestFile, encoding="utf-8-sig") as exportFile:
            deviceExportParser.feed(exportFile.read())
        assert deviceExportParser.rows, f"No table data found in {latestFile}"

        exportHeader = deviceExportParser.rows[0]
        exportColumnIndexes = []
        for _, exportColumn in exportColumnMap:
            assert exportColumn in exportHeader, (
                f"Export column {exportColumn!r} not found. Header: {exportHeader}"
            )
            exportColumnIndexes.append(exportHeader.index(exportColumn))
        exportDeviceRows = [
            tuple(row[columnIndex] for columnIndex in exportColumnIndexes)
            for row in deviceExportParser.rows[1:]
        ]
        statusIndex = next(
            index for index, (tableColumn, _) in enumerate(exportColumnMap)
            if tableColumn == "DevStatus"
        )
        validDeviceStatuses = {"Up", "Down", "Linked", "Unmanaged", "Not supported"}
        with assume: assert all(
            row[statusIndex] in validDeviceStatuses for row in inventoryDeviceRows
        ), f"Unexpected Inventory Device status: {inventoryDeviceRows}"
        with assume: assert all(
            row[statusIndex] in validDeviceStatuses for row in exportDeviceRows
        ), f"Unexpected exported Device status: {exportDeviceRows}"
        staticColumnIndexes = [
            index for index in range(len(exportColumnMap)) if index != statusIndex
        ]
        inventoryStaticRows = [
            tuple(row[index] for index in staticColumnIndexes)
            for row in inventoryDeviceRows
        ]
        exportStaticRows = [
            tuple(row[index] for index in staticColumnIndexes)
            for row in exportDeviceRows
        ]
        missingDeviceRows = Counter(inventoryStaticRows) - Counter(exportStaticRows)
        with assume: assert not missingDeviceRows, (
            "Inventory Device table and export file differ. "
            f"Missing rows: {list(missingDeviceRows.elements())[:5]}"
        )
'@
if ([regex]::Matches($mergedContent, $inventoryDeviceComparePattern).Count -ne 1) {
    throw "Inventory Device export comparison insertion point not found"
}
$mergedContent = [regex]::Replace(
    $mergedContent,
    $inventoryDeviceComparePattern,
    $inventoryDeviceCompareReplacement,
    1
)

$inventoryCardSnapshotPattern = '(?s)(?<casePrefix>    def test_EMS1_3580_3530_cardInfo\(self\):.*?        self\.driver\.find_element\(By\.LINK_TEXT, "Card"\)\.click\(\)\r?\n        time\.sleep\(3\)\r?\n)        minTime = datetime\.now\(\)\r?\n        self\.driver\.find_element\(By\.CSS_SELECTOR, "#i_action_export > a"\)\.click\(\)'
$inventoryCardSnapshotReplacement = '${casePrefix}' + @'
        exportColumnMap = (
            ("SubmapName", ("Submap Name",)),
            ("DevName", ("Device Name",)),
            ("IPAddress", ("IP Address",)),
            ("SlotID", ("Slot ID", "Slot")),
            ("RealType", ("Actual Type", "Real Type", "Card Type")),
            ("OperationStatus", ("Operation Status", "Operational Status")),
            ("AdminState", ("Admin State", "Administrative Status", "Admin Status")),
            ("AlarmStatus", ("Alarm Status",)),
            ("HwVersion", ("HW Version", "Hardware Version")),
            ("FwVersion", ("FW Version", "Firmware Version")),
            ("SerialNo", ("Serial No.", "Serial No", "Serial Number")),
        )
        normalizeCardValue = lambda value: " ".join(value.split())
        minTime = datetime.now()
        inventoryCardRows = self.driver.execute_script(
            """
            const columnNames = arguments[0];
            const headers = Array.from(document.querySelectorAll(
                "#card_inventory_div_head thead tr th"
            ));
            const indexes = columnNames.map((name) =>
                headers.findIndex((header) => header.getAttribute("name") === name)
            );
            if (indexes.some((index) => index < 0)) {
                throw new Error("Inventory Card column not found: " +
                    columnNames.filter((_, index) => indexes[index] < 0).join(", "));
            }
            const rows = Array.from(document.querySelectorAll(
                "#card_inventory_div_body tbody tr"
            )).map((row) => {
                const cells = Array.from(row.querySelectorAll(":scope > td"));
                return indexes.map((index) => cells[index].innerText);
            });
            document.querySelector("#i_action_export > a").click();
            return rows;
            """,
            [tableColumn for tableColumn, _ in exportColumnMap],
        )
        inventoryCardRows = [
            tuple(
                "" if normalizeCardValue(value) == "--" else normalizeCardValue(value)
                for value in row
            )
            for row in inventoryCardRows
        ]
'@
if ([regex]::Matches($mergedContent, $inventoryCardSnapshotPattern).Count -ne 1) {
    throw "Inventory Card export snapshot insertion point not found"
}
$mergedContent = [regex]::Replace(
    $mergedContent,
    $inventoryCardSnapshotPattern,
    $inventoryCardSnapshotReplacement,
    1
)

$inventoryCardComparePattern = '(?s)(?<caseBody>    def test_EMS1_3580_3530_cardInfo\(self\):.*?        with assume: assert minTime <= latestFileTime <= maxTime)'
$inventoryCardCompareReplacement = '${caseBody}' + @'


        from collections import Counter
        from html.parser import HTMLParser

        class CardExportParser(HTMLParser):
            def __init__(self):
                super().__init__(convert_charrefs=True)
                self.rows = []
                self.currentRow = None
                self.currentCell = None

            def handle_starttag(self, tag, attrs):
                if tag.lower() == "tr":
                    self.currentRow = []
                elif tag.lower() in {"td", "th"} and self.currentRow is not None:
                    self.currentCell = []

            def handle_data(self, data):
                if self.currentCell is not None:
                    self.currentCell.append(data)

            def handle_endtag(self, tag):
                if tag.lower() in {"td", "th"} and self.currentCell is not None:
                    value = normalizeCardValue("".join(self.currentCell))
                    self.currentRow.append("" if value == "--" else value)
                    self.currentCell = None
                elif tag.lower() == "tr" and self.currentRow is not None:
                    if self.currentRow:
                        self.rows.append(self.currentRow)
                    self.currentRow = None

        cardExportParser = CardExportParser()
        with open(latestFile, encoding="utf-8-sig") as exportFile:
            cardExportParser.feed(exportFile.read())
        assert cardExportParser.rows, f"No table data found in {latestFile}"

        exportHeader = cardExportParser.rows[0]
        exportColumnIndexes = []
        for _, exportColumnAliases in exportColumnMap:
            matchedColumn = next(
                (column for column in exportColumnAliases if column in exportHeader),
                None,
            )
            assert matchedColumn is not None, (
                f"Export columns {exportColumnAliases!r} not found. Header: {exportHeader}"
            )
            exportColumnIndexes.append(exportHeader.index(matchedColumn))
        exportCardRows = [
            tuple(row[columnIndex] for columnIndex in exportColumnIndexes)
            for row in cardExportParser.rows[1:]
            if len(row) > max(exportColumnIndexes)
        ]
        missingCardRows = Counter(inventoryCardRows) - Counter(exportCardRows)
        with assume: assert not missingCardRows, (
            "Inventory Card table and export file differ. "
            f"Missing rows: {list(missingCardRows.elements())[:5]}"
        )
'@
if ([regex]::Matches($mergedContent, $inventoryCardComparePattern).Count -ne 1) {
    throw "Inventory Card export comparison insertion point not found"
}
$mergedContent = [regex]::Replace(
    $mergedContent,
    $inventoryCardComparePattern,
    $inventoryCardCompareReplacement,
    1
)

$inventoryPortSnapshotPattern = '(?s)(?<casePrefix>    def test_EMS1_3581_3537_3582_3544_3585_3565_3881_3884_3890_3893_portInfo\(self\):.*?)(?<exportBlock>            minTime = datetime\.now\(\)\r?\n            self\.driver\.find_element\(By\.CSS_SELECTOR, "#i_action_export > a"\)\.click\(\))'
$inventoryPortSnapshotReplacement = '${casePrefix}' + @'
            minTime = datetime.now()
            inventoryPortSnapshot = capture_table_and_export(
                self.driver, "port_inventory_div"
            )
'@
if ([regex]::Matches($mergedContent, $inventoryPortSnapshotPattern).Count -ne 1) {
    throw "Inventory Port export snapshot insertion point not found"
}
$mergedContent = [regex]::Replace(
    $mergedContent,
    $inventoryPortSnapshotPattern,
    $inventoryPortSnapshotReplacement,
    1
)

$inventoryPortComparePattern = '(?s)(?<caseBody>    def test_EMS1_3581_3537_3582_3544_3585_3565_3881_3884_3890_3893_portInfo\(self\):.*?            with assume: assert minTime <= latestFileTime <= maxTime)'
$inventoryPortCompareReplacement = '${caseBody}' + @'

            with assume:
                assert_export_matches(
                    latestFile,
                    inventoryPortSnapshot,
                    f"Inventory Port ({self.cardPortTypeName[cardType]})",
                )
'@
if ([regex]::Matches($mergedContent, $inventoryPortComparePattern).Count -ne 1) {
    throw "Inventory Port export comparison insertion point not found"
}
$mergedContent = [regex]::Replace(
    $mergedContent,
    $inventoryPortComparePattern,
    $inventoryPortCompareReplacement,
    1
)

$inventoryOntSnapshotPattern = '(?s)(?<casePrefix>    def test_EMS1_4507_4510_ontInfo\(self\):.*?)(?<exportBlock>            minTime = datetime\.now\(\)\r?\n            self\.driver\.find_element\(By\.CSS_SELECTOR, "#i_action_export > a"\)\.click\(\))'
$inventoryOntSnapshotReplacement = '${casePrefix}' + @'
            normalizeOntValue = lambda value: " ".join(value.split())
            minTime = datetime.now()
            inventoryOntSnapshot = self.driver.execute_script(
                r"""
                const headers = Array.from(document.querySelectorAll(
                    "#ont_inventory_div_head thead tr th"
                ));
                const columns = headers.map((header, index) => ({
                    index: index,
                    name: header.innerText.replace(/\s+/g, " ").trim()
                })).filter((column) =>
                    column.name && !["Index", "DevID"].includes(column.name)
                );
                const rows = Array.from(document.querySelectorAll(
                    "#ont_inventory_div_body tbody tr"
                )).map((row) => {
                    const cells = Array.from(row.querySelectorAll(":scope > td"));
                    return columns.map((column) => cells[column.index].innerText);
                });
                document.querySelector("#i_action_export > a").click();
                return {headers: columns.map((column) => column.name), rows: rows};
                """
            )
            inventoryOntHeaders = [
                normalizeOntValue(value)
                for value in inventoryOntSnapshot["headers"]
            ]
            inventoryOntRows = [
                tuple(
                    "" if normalizeOntValue(value) == "--" else normalizeOntValue(value)
                    for value in row
                )
                for row in inventoryOntSnapshot["rows"]
            ]
'@
if ([regex]::Matches($mergedContent, $inventoryOntSnapshotPattern).Count -ne 1) {
    throw "Inventory ONT export snapshot insertion point not found"
}
$mergedContent = [regex]::Replace(
    $mergedContent,
    $inventoryOntSnapshotPattern,
    $inventoryOntSnapshotReplacement,
    1
)

$inventoryOntComparePattern = '(?s)(?<caseBody>    def test_EMS1_4507_4510_ontInfo\(self\):.*?            with assume: assert minTime <= latestFileTime <= maxTime)'
$inventoryOntCompareReplacement = '${caseBody}' + @'

            from collections import Counter
            from html.parser import HTMLParser

            class OntExportParser(HTMLParser):
                def __init__(self):
                    super().__init__(convert_charrefs=True)
                    self.rows = []
                    self.currentRow = None
                    self.currentCell = None

                def handle_starttag(self, tag, attrs):
                    if tag.lower() == "tr":
                        self.currentRow = []
                    elif tag.lower() in {"td", "th"} and self.currentRow is not None:
                        self.currentCell = []

                def handle_data(self, data):
                    if self.currentCell is not None:
                        self.currentCell.append(data)

                def handle_endtag(self, tag):
                    if tag.lower() in {"td", "th"} and self.currentCell is not None:
                        value = normalizeOntValue("".join(self.currentCell))
                        self.currentRow.append("" if value == "--" else value)
                        self.currentCell = None
                    elif tag.lower() == "tr" and self.currentRow is not None:
                        if self.currentRow:
                            self.rows.append(self.currentRow)
                        self.currentRow = None

            ontExportParser = OntExportParser()
            with open(latestFile, encoding="utf-8-sig") as exportFile:
                ontExportParser.feed(exportFile.read())
            assert ontExportParser.rows, f"No table data found in {latestFile}"

            exportHeader = ontExportParser.rows[0]
            exportHeaderLookup = {
                normalizeOntValue(header).casefold(): columnIndex
                for columnIndex, header in enumerate(exportHeader)
            }
            missingOntColumns = [
                header for header in inventoryOntHeaders
                if header.casefold() not in exportHeaderLookup
            ]
            assert not missingOntColumns, (
                f"Inventory ONT columns not found in export: {missingOntColumns}. "
                f"Header: {exportHeader}"
            )
            exportColumnIndexes = [
                exportHeaderLookup[header.casefold()]
                for header in inventoryOntHeaders
            ]
            exportOntRows = [
                tuple(row[columnIndex] for columnIndex in exportColumnIndexes)
                for row in ontExportParser.rows[1:]
                if len(row) > max(exportColumnIndexes)
            ]
            missingOntRows = Counter(inventoryOntRows) - Counter(exportOntRows)
            with assume: assert not missingOntRows, (
                "Inventory ONT table and export file differ. "
                f"Slot {self.ontSlotIDList[index]}, Port {self.ontPortIDList[index]}, "
                f"ONT {self.ontOntIDList[index]}. "
                f"Missing rows: {list(missingOntRows.elements())[:5]}"
            )
'@
if ([regex]::Matches($mergedContent, $inventoryOntComparePattern).Count -ne 1) {
    throw "Inventory ONT export comparison insertion point not found"
}
$mergedContent = [regex]::Replace(
    $mergedContent,
    $inventoryOntComparePattern,
    $inventoryOntCompareReplacement,
    1
)

$ontDashboardAlarmSnapshotPattern = '(?m)^            #Check the download file\r?\n            minTime = datetime\.now\(\)\r?\n            self\.driver\.find_element\(By\.CSS_SELECTOR, "#i_action_export > a"\)\.click\(\)'
$ontDashboardAlarmSnapshotReplacement = @'
            #Check the download file
            exportColumnMap = (
                ("Severity", ""),
                ("Ack", "Ack"),
                ("LogTime", "Log Time"),
                ("DevName", "Device Name"),
                ("Description", "Description"),
                ("DevIP", "Device IP"),
                ("SlotID", "Slot ID"),
                ("PortID", "Port ID"),
                ("Ont", "ONT ID"),
                ("AckUser", "Ack by"),
                ("AckTime", "Ack Time"),
                ("Category", "Category"),
                ("Note", "Note"),
            )
            normalizeAlarmValue = lambda value: " ".join(value.split())

            def activeAlarmExportValue(rowIndex, tableColumn):
                cell = getElementByPositionColNoPage(
                    self, "alarm_activeTable", rowIndex, tableColumn
                )
                if tableColumn == "Severity":
                    severityMatch = re.search(
                        r"(?:^|\s)td_(critical|major|minor|warning|info)(?:\s|$)",
                        cell.get_attribute("class") or "",
                        re.IGNORECASE,
                    )
                    assert severityMatch, (
                        "Unknown Active Alarm Severity icon class: "
                        f"{cell.get_attribute('class')!r}"
                    )
                    return severityMatch.group(1).title()
                if tableColumn == "Ack":
                    ackClass = cell.find_element(By.XPATH, ".//a").get_attribute("class") or ""
                    if "ackNotRead" in ackClass.split():
                        return "Not Acknowledged"
                    if "ackRead" in ackClass.split():
                        return "Acknowledged"
                    raise AssertionError(f"Unknown Active Alarm Ack icon class: {ackClass!r}")
                value = normalizeAlarmValue(cell.text)
                if value == "--":
                    if tableColumn in {"SlotID", "PortID", "Ont"}:
                        return "0"
                    if tableColumn in {"AckUser", "AckTime", "Note"}:
                        return ""
                return value

            activeAlarmRows = []
            visibleAlarmRowCount = len(self.driver.find_elements(
                By.XPATH, "//table[@id='alarm_activeTable_body']/tbody/tr"
            ))
            for rowIndex in range(1, visibleAlarmRowCount + 1):
                activeAlarmRows.append(tuple(
                    activeAlarmExportValue(rowIndex, tableColumn)
                    for tableColumn, _ in exportColumnMap
                ))
            minTime = datetime.now()
            self.driver.find_element(By.CSS_SELECTOR, "#i_action_export > a").click()
'@
if ([regex]::Matches($mergedContent, $ontDashboardAlarmSnapshotPattern).Count -ne 1) {
    throw "ONT Dashboard Alarm export snapshot insertion point not found"
}
$mergedContent = [regex]::Replace(
    $mergedContent,
    $ontDashboardAlarmSnapshotPattern,
    $ontDashboardAlarmSnapshotReplacement,
    1
)

$ontDashboardAlarmComparePattern = '(?m)^            with assume: assert latestFileSize > 0\r?\n            with assume: assert minTime <= latestFileTime <= maxTime\r?\n            # Alarm page function'
$ontDashboardAlarmCompareReplacement = @'
            with assume: assert latestFileSize > 0
            with assume: assert minTime <= latestFileTime <= maxTime

            from collections import Counter
            from html.parser import HTMLParser

            class AlarmExportParser(HTMLParser):
                def __init__(self):
                    super().__init__(convert_charrefs=True)
                    self.rows = []
                    self.currentRow = None
                    self.currentCell = None

                def handle_starttag(self, tag, attrs):
                    if tag.lower() == "tr":
                        self.currentRow = []
                    elif tag.lower() == "td" and self.currentRow is not None:
                        self.currentCell = []

                def handle_data(self, data):
                    if self.currentCell is not None:
                        self.currentCell.append(data)

                def handle_endtag(self, tag):
                    if tag.lower() == "td" and self.currentCell is not None:
                        self.currentRow.append(normalizeAlarmValue("".join(self.currentCell)))
                        self.currentCell = None
                    elif tag.lower() == "tr" and self.currentRow is not None:
                        self.rows.append(self.currentRow)
                        self.currentRow = None

            alarmExportParser = AlarmExportParser()
            with open(latestFile, encoding="utf-8-sig") as exportFile:
                alarmExportParser.feed(exportFile.read())
            assert alarmExportParser.rows, f"No table data found in {latestFile}"

            exportHeader = alarmExportParser.rows[0]
            exportColumnIndexes = []
            for _, exportColumn in exportColumnMap:
                assert exportColumn in exportHeader, (
                    f"Export column {exportColumn!r} not found. Header: {exportHeader}"
                )
                exportColumnIndexes.append(exportHeader.index(exportColumn))
            exportAlarmRows = [
                tuple(row[columnIndex] for columnIndex in exportColumnIndexes)
                for row in alarmExportParser.rows[1:]
            ]
            missingAlarmRows = Counter(activeAlarmRows) - Counter(exportAlarmRows)
            with assume: assert not missingAlarmRows, (
                "ONT Dashboard Active Alarm table and export file differ. "
                f"Missing rows: {list(missingAlarmRows.elements())[:5]}"
            )
            # Alarm page function
'@
if ([regex]::Matches($mergedContent, $ontDashboardAlarmComparePattern).Count -ne 1) {
    throw "ONT Dashboard Alarm export comparison insertion point not found"
}
$mergedContent = [regex]::Replace(
    $mergedContent,
    $ontDashboardAlarmComparePattern,
    $ontDashboardAlarmCompareReplacement,
    1
)

$dashboardAlarmExportPattern = '(?m)^        #Check the download file\r?\n        pageTotal = pageCount \(self, "alarm_activeTable"\)\r?\n        minTime = datetime\.now\(\)'
$dashboardAlarmExportReplacement = @'
        #Check the download file
        pageTotal = pageCount (self, "alarm_activeTable")
        exportColumnMap = (
            ("Severity", ""),
            ("Ack", "Ack"),
            ("LogTime", "Log Time"),
            ("DevName", "Device Name"),
            ("Description", "Description"),
            ("DevIP", "Device IP"),
            ("SlotID", "Slot ID"),
            ("PortID", "Port ID"),
            ("Ont", "ONT ID"),
            ("AckUser", "Ack by"),
            ("AckTime", "Ack Time"),
            ("Category", "Category"),
            ("Note", "Note"),
        )
        normalizeAlarmValue = lambda value: " ".join(value.split())

        def activeAlarmExportValue(rowIndex, tableColumn):
            cell = getElementByPositionColNoPage(
                self, "alarm_activeTable", rowIndex, tableColumn
            )
            if tableColumn == "Severity":
                severityMatch = re.search(
                    r"(?:^|\s)td_(critical|major|minor|warning|info)(?:\s|$)",
                    cell.get_attribute("class") or "",
                    re.IGNORECASE,
                )
                assert severityMatch, (
                    "Unknown Active Alarm Severity icon class: "
                    f"{cell.get_attribute('class')!r}"
                )
                return severityMatch.group(1).title()
            if tableColumn == "Ack":
                ackClass = cell.find_element(By.XPATH, ".//a").get_attribute("class") or ""
                if "ackNotRead" in ackClass.split():
                    return "Not Acknowledged"
                if "ackRead" in ackClass.split():
                    return "Acknowledged"
                raise AssertionError(f"Unknown Active Alarm Ack icon class: {ackClass!r}")
            value = normalizeAlarmValue(cell.text)
            if value == "--":
                if tableColumn in {"SlotID", "PortID", "Ont"}:
                    return "0"
                if tableColumn in {"AckUser", "AckTime", "Note"}:
                    return ""
            return value

        activeAlarmRows = []
        visibleAlarmRowCount = len(self.driver.find_elements(
            By.XPATH, "//table[@id='alarm_activeTable_body']/tbody/tr"
        ))
        for rowIndex in range(1, visibleAlarmRowCount + 1):
            activeAlarmRows.append(tuple(
                activeAlarmExportValue(rowIndex, tableColumn)
                for tableColumn, _ in exportColumnMap
            ))
        minTime = datetime.now()
'@
if ([regex]::Matches($mergedContent, $dashboardAlarmExportPattern).Count -ne 1) {
    throw "Dashboard Alarm export insertion point not found"
}
$mergedContent = [regex]::Replace(
    $mergedContent,
    $dashboardAlarmExportPattern,
    $dashboardAlarmExportReplacement,
    1
)

$dashboardAlarmComparePattern = '(?m)^            with assume: assert latestFileSize > 0\r?\n            with assume: assert minTime <= latestFileTime <= maxTime\r?\n        else:'
$dashboardAlarmCompareReplacement = @'
            with assume: assert latestFileSize > 0
            with assume: assert minTime <= latestFileTime <= maxTime

            from collections import Counter
            from html.parser import HTMLParser

            class AlarmExportParser(HTMLParser):
                def __init__(self):
                    super().__init__(convert_charrefs=True)
                    self.rows = []
                    self.currentRow = None
                    self.currentCell = None

                def handle_starttag(self, tag, attrs):
                    if tag.lower() == "tr":
                        self.currentRow = []
                    elif tag.lower() == "td" and self.currentRow is not None:
                        self.currentCell = []

                def handle_data(self, data):
                    if self.currentCell is not None:
                        self.currentCell.append(data)

                def handle_endtag(self, tag):
                    if tag.lower() == "td" and self.currentCell is not None:
                        self.currentRow.append(normalizeAlarmValue("".join(self.currentCell)))
                        self.currentCell = None
                    elif tag.lower() == "tr" and self.currentRow is not None:
                        self.rows.append(self.currentRow)
                        self.currentRow = None

            alarmExportParser = AlarmExportParser()
            with open(latestFile, encoding="utf-8-sig") as exportFile:
                alarmExportParser.feed(exportFile.read())
            assert alarmExportParser.rows, f"No table data found in {latestFile}"

            exportHeader = alarmExportParser.rows[0]
            exportColumnIndexes = []
            for _, exportColumn in exportColumnMap:
                assert exportColumn in exportHeader, (
                    f"Export column {exportColumn!r} not found. Header: {exportHeader}"
                )
                exportColumnIndexes.append(exportHeader.index(exportColumn))
            exportAlarmRows = [
                tuple(row[index] for index in exportColumnIndexes)
                for row in alarmExportParser.rows[1:]
            ]
            missingAlarmRows = Counter(activeAlarmRows) - Counter(exportAlarmRows)
            with assume: assert not missingAlarmRows, (
                "Active Alarm table and export file differ. "
                f"Missing rows: {list(missingAlarmRows.elements())[:5]}"
            )
        else:
'@
if ([regex]::Matches($mergedContent, $dashboardAlarmComparePattern).Count -ne 1) {
    throw "Dashboard Alarm export comparison insertion point not found"
}
$mergedContent = [regex]::Replace(
    $mergedContent,
    $dashboardAlarmComparePattern,
    $dashboardAlarmCompareReplacement,
    1
)

$icatAlarmStatusSnapshotPattern = '(?s)(?<casePrefix>    def test_EMS1_5491_alarmStatus\(self\):.*?        with assume: assert self\.driver\.find_element\(By\.ID, "alarm_activeTable"\)\.is_displayed\(\)\r?\n)        #Check the download file\r?\n        minTime = datetime\.now\(\)'
$icatAlarmStatusSnapshotReplacement = '${casePrefix}' + @'
        #Check the download file
        exportColumnMap = (
            ("Severity", ""),
            ("Ack", "Ack"),
            ("LogTime", "Log Time"),
            ("DevName", "Device Name"),
            ("Description", "Description"),
            ("DevIP", "Device IP"),
            ("SlotID", "Slot ID"),
            ("PortID", "Port ID"),
            ("Ont", "ONT ID"),
            ("AckUser", "Ack by"),
            ("AckTime", "Ack Time"),
            ("Category", "Category"),
            ("Note", "Note"),
        )
        normalizeAlarmValue = lambda value: " ".join(value.split())

        def activeAlarmExportValue(rowIndex, tableColumn):
            cell = getElementByPositionColNoPage(
                self, "alarm_activeTable", rowIndex, tableColumn
            )
            if tableColumn == "Severity":
                severityMatch = re.search(
                    r"(?:^|\s)td_(critical|major|minor|warning|info)(?:\s|$)",
                    cell.get_attribute("class") or "",
                    re.IGNORECASE,
                )
                assert severityMatch, (
                    "Unknown Active Alarm Severity icon class: "
                    f"{cell.get_attribute('class')!r}"
                )
                return severityMatch.group(1).title()
            if tableColumn == "Ack":
                ackClass = cell.find_element(By.XPATH, ".//a").get_attribute("class") or ""
                if "ackNotRead" in ackClass.split():
                    return "Not Acknowledged"
                if "ackRead" in ackClass.split():
                    return "Acknowledged"
                raise AssertionError(f"Unknown Active Alarm Ack icon class: {ackClass!r}")
            value = normalizeAlarmValue(cell.text)
            if value == "--":
                if tableColumn in {"SlotID", "PortID", "Ont"}:
                    return "0"
                if tableColumn in {"AckUser", "AckTime", "Note"}:
                    return ""
            return value

        activeAlarmRows = []
        visibleAlarmRowCount = len(self.driver.find_elements(
            By.XPATH, "//table[@id='alarm_activeTable_body']/tbody/tr"
        ))
        for rowIndex in range(1, visibleAlarmRowCount + 1):
            activeAlarmRows.append(tuple(
                activeAlarmExportValue(rowIndex, tableColumn)
                for tableColumn, _ in exportColumnMap
            ))
        minTime = datetime.now()
'@
if ([regex]::Matches($mergedContent, $icatAlarmStatusSnapshotPattern).Count -ne 1) {
    throw "Icat Alarm Status export snapshot insertion point not found"
}
$mergedContent = [regex]::Replace(
    $mergedContent,
    $icatAlarmStatusSnapshotPattern,
    $icatAlarmStatusSnapshotReplacement,
    1
)

$icatAlarmStatusComparePattern = '(?s)(?<caseBody>    def test_EMS1_5491_alarmStatus\(self\):.*?            with assume: assert minTime <= latestFileTime <= maxTime)'
$icatAlarmStatusCompareReplacement = '${caseBody}' + @'

            from collections import Counter
            from html.parser import HTMLParser

            class IcatAlarmExportParser(HTMLParser):
                def __init__(self):
                    super().__init__(convert_charrefs=True)
                    self.rows = []
                    self.currentRow = None
                    self.currentCell = None

                def handle_starttag(self, tag, attrs):
                    if tag.lower() == "tr":
                        self.currentRow = []
                    elif tag.lower() in {"td", "th"} and self.currentRow is not None:
                        self.currentCell = []

                def handle_data(self, data):
                    if self.currentCell is not None:
                        self.currentCell.append(data)

                def handle_endtag(self, tag):
                    if tag.lower() in {"td", "th"} and self.currentCell is not None:
                        self.currentRow.append(normalizeAlarmValue("".join(self.currentCell)))
                        self.currentCell = None
                    elif tag.lower() == "tr" and self.currentRow is not None:
                        if self.currentRow:
                            self.rows.append(self.currentRow)
                        self.currentRow = None

            alarmExportParser = IcatAlarmExportParser()
            with open(latestFile, encoding="utf-8-sig") as exportFile:
                alarmExportParser.feed(exportFile.read())
            assert alarmExportParser.rows, f"No table data found in {latestFile}"

            exportHeader = alarmExportParser.rows[0]
            exportColumnIndexes = []
            for _, exportColumn in exportColumnMap:
                assert exportColumn in exportHeader, (
                    f"Export column {exportColumn!r} not found. Header: {exportHeader}"
                )
                exportColumnIndexes.append(exportHeader.index(exportColumn))
            exportAlarmRows = [
                tuple(row[columnIndex] for columnIndex in exportColumnIndexes)
                for row in alarmExportParser.rows[1:]
                if len(row) > max(exportColumnIndexes)
            ]
            missingAlarmRows = Counter(activeAlarmRows) - Counter(exportAlarmRows)
            with assume: assert not missingAlarmRows, (
                "Icat Active Alarm table and export file differ. "
                f"Missing rows: {list(missingAlarmRows.elements())[:5]}"
            )
'@
if ([regex]::Matches($mergedContent, $icatAlarmStatusComparePattern).Count -ne 1) {
    throw "Icat Alarm Status export comparison insertion point not found"
}
$mergedContent = [regex]::Replace(
    $mergedContent,
    $icatAlarmStatusComparePattern,
    $icatAlarmStatusCompareReplacement,
    1
)

$icatExportComparisons = @(
    @{ Case = 'test_EMS1_3581_3537_3582_3544_3585_3565_3881_3884_3890_3893_portInfo'; Indent = '        '; Table = 'port_inventory_div'; Label = 'Inventory All Port'; Assume = $true },
    @{ Case = 'test_EMS1_5500_cardInfo'; Indent = '        '; Table = 'card_inventory_div'; Label = 'Icat Inventory Card' },
    @{ Case = 'test_EMS1_5501_portInfo'; Indent = '        '; Table = 'port_inventory_div'; Label = 'Icat Inventory Port' },
    @{ Case = 'test_EMS1_5502_ontInfo'; Indent = '            '; Table = 'ont_inventory_div'; Label = 'Icat Inventory ONT' },
    @{ Case = 'test_EMS1_5493_5498_deviceMap'; Indent = '        '; Table = 'alarm_activeTable'; Label = 'Device Map Active Alarm' },
    @{ Case = 'test_EMS1_5503_alarmActive'; Indent = '        '; Table = 'alarm_activeTable'; Label = 'Icat Active Alarm' },
    @{ Case = 'test_EMS1_5504_alarmHistory'; Indent = '        '; Table = 'alarm_historyTable'; Label = 'Icat History Alarm' },
    @{ Case = 'test_EMS1_4369_6147_alarmStatusExport'; Indent = '        '; Table = 'alarm_activeTable'; Label = 'Map Device Active Alarm' }
)
foreach ($spec in $icatExportComparisons) {
    $caseName = [regex]::Escape($spec.Case)
    $indent = $spec.Indent
    $escapedIndent = [regex]::Escape($indent)
    $snapshotPattern = "(?s)(?<prefix>    def $caseName\(self\):.*?${escapedIndent}minTime = datetime\.now\(\)\r?\n)${escapedIndent}self\.driver\.find_element\(By\.CSS_SELECTOR, `"#i_action_export > a`"\)\.click\(\)"
    if ([regex]::Matches($mergedContent, $snapshotPattern).Count -ne 1) {
        throw "$($spec.Case) export snapshot insertion point not found"
    }
    $snapshotReplacement = '${prefix}' + $indent + 'exportTableSnapshot = capture_table_and_export(self.driver, "' + $spec.Table + '")'
    $mergedContent = [regex]::Replace($mergedContent, $snapshotPattern, $snapshotReplacement, 1)

    $comparePattern = "(?s)(?<body>    def $caseName\(self\):.*?${escapedIndent}with assume: assert minTime <= latestFileTime <= maxTime)"
    if ([regex]::Matches($mergedContent, $comparePattern).Count -ne 1) {
        throw "$($spec.Case) export comparison insertion point not found"
    }
    $compareCall = 'assert_export_matches(latestFile, exportTableSnapshot, "' + $spec.Label + '")'
    if ($spec.Assume) {
        $compareReplacement = '${body}' + "`r`n" + $indent + 'with assume:' + "`r`n" + $indent + '    ' + $compareCall
    }
    else {
        $compareReplacement = '${body}' + "`r`n" + $indent + $compareCall
    }
    $mergedContent = [regex]::Replace($mergedContent, $comparePattern, $compareReplacement, 1)
}

$rebootPortSkipPattern = '(?<definition>    async def test_EMS1_6382_RebootPort\(self\):)'
if ([regex]::Matches($mergedContent, $rebootPortSkipPattern).Count -ne 1) {
    throw "EMS1-6382 RebootPort definition was not found exactly once"
}
$mergedContent = [regex]::Replace(
    $mergedContent,
    $rebootPortSkipPattern,
    "    @pytest.mark.skip`r`n`${definition}",
    1
)

$userRadiusPrerequisitePattern = '(?<definition>    async def test_EMS1_3638_3639_3640_usrCreateModifyDelete\(self\):\r?\n)'
if ([regex]::Matches($mergedContent, $userRadiusPrerequisitePattern).Count -ne 1) {
    throw "EMS1-3638/3639/3640 user case definition was not found exactly once"
}
$userRadiusPrerequisiteReplacement = '${definition}' + @'
        # Local EMS user authentication requires the Radius Server to be disabled.
        self.driver.find_element(By.LINK_TEXT, "System").click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "System Properties"))
        ).click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "System Setting"))
        ).click()
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Radius Server"))
        ).click()

        radius_active_xpath = (
            "//*[@id='radius_active' or @id='radiusActive' "
            "or @name='radius_active' or @name='radiusActive'] | "
            "//*[normalize-space()='Active']/following::select[1] | "
            "//*[normalize-space()='Active']/following::input[1]"
        )

        def radius_active_control():
            return WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, radius_active_xpath))
            )

        def radius_is_disabled():
            control = radius_active_control()
            if control.tag_name.casefold() == "select":
                return Select(control).first_selected_option.text.strip().casefold() in {
                    "disable", "disabled"
                }
            control_type = (control.get_attribute("type") or "").casefold()
            if control_type == "checkbox":
                return not control.is_selected()
            disabled_options = self.driver.find_elements(
                By.XPATH,
                "//label[normalize-space()='Disable' or normalize-space()='Disabled']"
                "/input | //input[@type='radio' and "
                "(@value='Disable' or @value='Disabled' or @value='0')]",
            )
            return any(option.is_selected() for option in disabled_options)

        if not radius_is_disabled():
            control = radius_active_control()
            if control.tag_name.casefold() == "select":
                radius_select = Select(control)
                disable_option = next(
                    option for option in radius_select.options
                    if option.text.strip().casefold() in {"disable", "disabled"}
                )
                radius_select.select_by_visible_text(disable_option.text)
            elif (control.get_attribute("type") or "").casefold() == "checkbox":
                control.click()
            else:
                disable_control = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        "//label[normalize-space()='Disable' or "
                        "normalize-space()='Disabled']/input | "
                        "//input[@type='radio' and (@value='Disable' or "
                        "@value='Disabled' or @value='0')]",
                    ))
                )
                disable_control.click()

            save_button = WebDriverWait(self.driver, 30).until(
                lambda _driver: next((
                    button for button in _driver.find_elements(
                        By.XPATH,
                        "//input[@type='button' or @type='submit'] | //button",
                    )
                    if button.is_displayed()
                    and (button.get_attribute("value") or button.text).strip().casefold()
                    in {"save", "apply"}
                ), False)
            )
            save_button.click()
            try:
                success_message = WebDriverWait(self.driver, 15).until(
                    EC.visibility_of_element_located((By.ID, "message_text"))
                )
                assert "success" in success_message.text.casefold(), (
                    f"Radius Server Disable save failed: {success_message.text}"
                )
                self.driver.find_element(
                    By.CSS_SELECTOR, "#message_diag .button"
                ).click()
            except TimeoutException:
                pass

        assert radius_is_disabled(), "Radius Server Active must be Disable"
'@
$userRadiusPrerequisiteReplacement += "`r`n"
$mergedContent = [regex]::Replace(
    $mergedContent,
    $userRadiusPrerequisitePattern,
    $userRadiusPrerequisiteReplacement,
    1
)

$performance6309CasePattern = '(?ms)^    def test_EMS1_6309_peformanceCurrentInterface\(self\):.*?(?=^    def _newcase_11__discover_card_targets\(self, performance_type, card\):)'
if ([regex]::Matches($mergedContent, $performance6309CasePattern).Count -ne 1) {
    throw "Cannot uniquely locate EMS1-6309 case"
}
$performance6309CaseReplacement = @'
    def test_EMS1_6309_peformanceCurrentInterface(self):
        cards = self._newcase_11__interface_cards()
        if not cards:
            pytest.skip("EMS1-6309 requires non-zero interface-card slots in environment_parameter.json CARDINFO.")

        self._newcase_11__open_ems()
        login_ems(self.driver, self.emsUsr, self.emsPwd)
        close_all_current_charts(self.driver)

        try:
            for performance_type in ["Interface(Accumulation)", "Interface(Rate)"]:
                for card_index, card in enumerate(cards, start=1):
                    print(
                        f"EMS1-6309: test {performance_type}, card {card_index}/{len(cards)} "
                        f"slot={card['slot_id']} card={card['type']}",
                        flush=True,
                    )
                    targets, initial_probe_count = self._newcase_11__discover_card_targets(
                        performance_type,
                        card,
                    )
                    self._newcase_11__create_and_verify_card_ports(
                        performance_type,
                        targets,
                        initial_probe_count,
                    )
                    close_all_current_charts(self.driver)
        finally:
            close_create_demand(self.driver)
            close_all_current_charts(self.driver)

'@
$mergedContent = [regex]::Replace(
    $mergedContent,
    $performance6309CasePattern,
    $performance6309CaseReplacement,
    1
)

$performance6309DiscoverPattern = '(?ms)^    def _newcase_11__discover_card_targets\(self, performance_type, card\):.*?(?=^    def _newcase_11__create_and_verify_card_ports\(self, performance_type, targets\):)'
$performance6309DiscoverReplacement = @'
    def _newcase_11__discover_card_targets(self, performance_type, card):
        print(
            f"EMS1-6309: open Create for {performance_type}, "
            f"slot={card['slot_id']} card={card['type']}",
            flush=True,
        )
        open_create_demand(self.driver)
        time.sleep(2)
        initial_probe_count = available_probe_count(self.driver)
        assert initial_probe_count > 0, (
            "The currently available number of probes must be greater than 0 "
            f"before the first Create. actual={initial_probe_count}"
        )
        try:
            ports = interface_port_options(
                self.driver,
                performance_type,
                self.dutNodeName,
                card["slot_id"],
                card["type"],
            )
        except Exception:
            close_create_demand(self.driver)
            raise
        targets = [{**card, "port_id": port_id} for port_id in ports]
        assert targets, (
            f"No Performance/Current port options found for {performance_type} "
            f"slot={card['slot_id']} card={card['type']}"
        )
        print(
            f"EMS1-6309: ports={ports}, initial probes={initial_probe_count}",
            flush=True,
        )
        return targets, initial_probe_count

'@
$mergedContent = [regex]::Replace(
    $mergedContent,
    $performance6309DiscoverPattern,
    $performance6309DiscoverReplacement,
    1
)

$performance6309MethodPattern = '(?ms)^    def _newcase_11__create_and_verify_card_ports\(self, performance_type, targets\):.*?(?=^    def _newcase_11__interface_cards\(self\):)'
if ([regex]::Matches($mergedContent, $performance6309MethodPattern).Count -ne 1) {
    throw "Cannot uniquely locate EMS1-6309 chart creation helper"
}
$performance6309MethodReplacement = @'
    def _newcase_11__create_and_verify_card_ports(
        self,
        performance_type,
        targets,
        initial_probe_count,
    ):
        print(
            f"EMS1-6309: create {len(targets)} {performance_type} charts "
            "continuously, then verify all charts together",
            flush=True,
        )
        previous_probe_count = initial_probe_count
        for target_index, target in enumerate(targets, start=1):
            if target_index == 1:
                probe_count = initial_probe_count
            else:
                open_create_demand(self.driver)
                time.sleep(2)
                expected_probe_count = previous_probe_count - 1
                probe_count = available_probe_count(
                    self.driver,
                    timeout=10,
                    expected=expected_probe_count,
                )
                assert probe_count == previous_probe_count - 1, (
                    "The currently available number of probes must decrease by exactly 1 "
                    f"after each Create. previous={previous_probe_count}, actual={probe_count}"
                )
            assert probe_count > 0, (
                "The currently available number of probes must be greater than 0 "
                f"before Create. actual={probe_count}"
            )
            print(
                f"EMS1-6309: Create {target_index}/{len(targets)}, "
                f"slot={target['slot_id']}, port={target['port_id']}, probes={probe_count}",
                flush=True,
            )
            previous_probe_count = probe_count
            create_interface_current_chart(
                self.driver,
                performance_type,
                self.dutNodeName,
                target["slot_id"],
                target["type"],
                target["port_id"],
            )
            print("EMS1-6309: wait 1 second after Create modal closes", flush=True)
            time.sleep(1)

        # Open Create once more so the final Create operation's -1 probe change is also verified.
        open_create_demand(self.driver)
        time.sleep(2)
        expected_final_probe_count = previous_probe_count - 1
        final_probe_count = available_probe_count(
            self.driver,
            timeout=10,
            expected=expected_final_probe_count,
        )
        assert final_probe_count == previous_probe_count - 1, (
            "The currently available number of probes must decrease by exactly 1 "
            f"after the final Create. previous={previous_probe_count}, actual={final_probe_count}"
        )
        close_create_demand(self.driver)

        time.sleep(10)
        refresh_current_page(self.driver)
        chart_states = wait_for_all_charts_with_frontend_data(
            self.driver,
            expected_count=len(targets),
            timeout=60,
        )
        print(
            f"EMS1-6309: {performance_type} frontend data states: {chart_states}",
            flush=True,
        )
        close_all_current_charts(self.driver)

'@
$mergedContent = [regex]::Replace(
    $mergedContent,
    $performance6309MethodPattern,
    $performance6309MethodReplacement,
    1
)

$performance6309CardsPattern = '(?ms)^    def _newcase_11__interface_cards\(self\):.*?(?=^    def _newcase_11__target_names\(self, performance_type, targets\):)'
$performance6309CardsReplacement = @'
    def _newcase_11__interface_cards(self):
        if "OLT14" in str(self.dutType).upper():
            return [{"slot_id": "--", "type": self.dutType}]
        cards = []
        for card in self.dutCardInfo.values():
            slot_id = str(card.get("slot_id", "")).strip()
            card_type = str(card.get("type", "")).strip()
            if slot_id and slot_id not in {"0", "--"} and card_type:
                cards.append({"slot_id": slot_id, "type": card_type})
        return sorted(
            cards,
            key=lambda card: int(card["slot_id"]) if card["slot_id"].isdigit() else card["slot_id"],
        )

'@
$mergedContent = [regex]::Replace(
    $mergedContent,
    $performance6309CardsPattern,
    $performance6309CardsReplacement,
    1
)

$performance6309Doc = @'
# EMS1-6309 peformanceCurrentInterface

## Objective

Verify that EMS can create valid Performance/Current charts for every port on every non-zero card slot, first with `Interface(Accumulation)` and then with `Interface(Rate)`.

## Test Data

- EMS URL/account: from `environment_parameter.json`
- DUT: `ZYXEL_DUT.<cmdopt>`
- Device name: `name_display`
- Cards/ports: discovered from `Performance/Current` Create dialog

## Steps

1. Go to `Performance/Current`.
2. If charts exist, quickly close all of them by clicking every `X` (`class="icon exitBlock"`).
3. Click the Create icon.
4. Wait 2 seconds and verify `The currently available number of probes is : N`. `N` must be greater than 0 before Create and must decrease by exactly 1 after every Create.
5. Select Performance Type `Interface(Accumulation)`. Do not select it again when it is already selected.
6. For chassis devices, under Device Type select the first card and its Port; every card whose Slot ID is not 0 must be tested. For an OLT140X-series device, do not select a Slot; select the device directly and test every available Port.
7. Click Create.
8. After returning to Current, immediately click Create again.
9. Repeat steps 4 to 8 until every Port on the current Slot has been created.
10. Wait 10 seconds, click Refresh, and verify that charts for every Port appear and all chart values are valid.
11. Quickly close all charts.
12. Repeat steps 3 to 11 until every non-zero Slot has been tested.
13. Repeat steps 3 to 12 using `Interface(Rate)`.

## Expected Result

- Existing charts are closed before creation starts.
- Every Create dialog is given exactly 2 seconds before its probe count is checked.
- Probe count is greater than 0 before Create and decreases by exactly 1 after every Create, including the final Port.
- After the fixed 2-second wait, if EMS still displays the previous probe count, the test polls the same Create dialog for up to 10 seconds for the expected decremented value instead of failing immediately.
- Performance Type is changed only when the requested type is not already selected.
- Every Port on every non-zero Slot is tested.
- For OLT140X-series devices, Slot selection is skipped and every Port exposed directly under the device is tested.
- No chart-presence check is performed between individual Create operations.
- After Create, the test waits for the Create modal to disappear, waits a fixed 1 second, and then clicks Create again. Alert/OK/error scanning runs only when the modal remains visible for more than 1 second.
- After all Ports on one Slot are created, the test waits 10 seconds, clicks Refresh, and verifies all charts and values together.
- All charts are quickly closed before moving to the next Slot.
- All Slots are tested with `Interface(Accumulation)` first and then with `Interface(Rate)`.
'@
[System.IO.File]::WriteAllText(
    (Join-Path $targetDocsRoot "EMS1-6309_peformanceCurrentInterface.md"),
    $performance6309Doc + "`r`n",
    $utf8NoBom
)

$lineList = [System.Collections.Generic.List[string]]::new()
$lineList.AddRange([string[]][regex]::Split($mergedContent, '\r?\n'))
$caseDefinitionIndexes = [System.Collections.Generic.List[int]]::new()
for ($index = 0; $index -lt $lineList.Count; $index++) {
    if ($lineList[$index] -match '^    (?:async\s+)?def\s+test_EMS1_') {
        $caseDefinitionIndexes.Add($index)
    }
}

# Format from bottom to top so earlier line indexes remain stable. A case header
# includes its original class-level comments and every allowed marker.
for ($caseIndex = $caseDefinitionIndexes.Count - 1; $caseIndex -ge 0; $caseIndex--) {
    $definitionIndex = $caseDefinitionIndexes[$caseIndex]
    $scanIndex = $definitionIndex - 1
    while ($scanIndex -ge 0 -and (
        [string]::IsNullOrWhiteSpace($lineList[$scanIndex]) -or
        $lineList[$scanIndex] -match '^    #' -or
        $lineList[$scanIndex] -match '^    @pytest\.mark\.(?:Restful|Icat|Provision|Unicase|skip|asyncio)'
    )) {
        $scanIndex--
    }

    $leadingBlankStart = $scanIndex + 1
    $caseHeaderStart = $leadingBlankStart
    while ($caseHeaderStart -lt $definitionIndex -and [string]::IsNullOrWhiteSpace($lineList[$caseHeaderStart])) {
        $caseHeaderStart++
    }

    $commentLines = [System.Collections.Generic.List[string]]::new()
    $decoratorLines = [System.Collections.Generic.List[string]]::new()
    for ($headerIndex = $caseHeaderStart; $headerIndex -lt $definitionIndex; $headerIndex++) {
        if ($lineList[$headerIndex] -match '^    #') {
            $commentLines.Add($lineList[$headerIndex])
        }
        elseif ($lineList[$headerIndex] -match '^    @pytest\.mark\.(?:Restful|Icat|Provision|Unicase|skip|asyncio)') {
            $decoratorLines.Add($lineList[$headerIndex])
        }
    }

    $lineList.RemoveRange($leadingBlankStart, $definitionIndex - $leadingBlankStart)
    $normalizedHeader = [System.Collections.Generic.List[string]]::new()
    $normalizedHeader.Add("")
    $normalizedHeader.Add("")
    $normalizedHeader.AddRange($commentLines)
    $normalizedHeader.AddRange($decoratorLines)
    $lineList.InsertRange($leadingBlankStart, $normalizedHeader)
}
$mergedContent = $lineList -join "`r`n"
[System.IO.File]::WriteAllText($mergedPath, $mergedContent, $utf8NoBom)
& $PythonExecutable (Join-Path $PSScriptRoot "normalize_python_imports.py") $mergedPath
if ($LASTEXITCODE -ne 0) {
    throw "Import normalization failed with exit code $LASTEXITCODE"
}
& $PythonExecutable (Join-Path $PSScriptRoot "generate_global_case_test_names.py") `
    $mergedPath `
    (Join-Path $targetRoot "EMSWebGlobalCaseTestNames.list")
if ($LASTEXITCODE -ne 0) {
    throw "Case-name list generation failed with exit code $LASTEXITCODE"
}
& $PythonExecutable (Join-Path $PSScriptRoot "merge_global_case_lists.py") `
    (Join-Path $sourceRoot "Web_EMS_ICAT.list") `
    (Join-Path $sourceRoot "Web_EMS_Restful.list") `
    (Join-Path $sourceRoot "Web_EMS_Provision.list") `
    (Join-Path $sourceRoot "Web_EMS_Unicase.list") `
    (Join-Path $newCaseSourceRoot "Web_EMS_NewCase.list") `
    (Join-Path $targetRoot "EMSWebGlobalCase.list")
if ($LASTEXITCODE -ne 0) {
    throw "Case-list generation failed with exit code $LASTEXITCODE"
}

foreach ($sourceFile in $sourceFiles) {
    Remove-Item -LiteralPath (Join-Path $targetRoot $sourceFile)
}

$unusedLibraryFiles = @("readjson.py", "screen.py")
foreach ($unusedLibraryFile in $unusedLibraryFiles) {
    $unusedLibraryPath = Join-Path (Join-Path $targetRoot "libs") $unusedLibraryFile
    if (Test-Path -LiteralPath $unusedLibraryPath) {
        Remove-Item -LiteralPath $unusedLibraryPath -Force
    }
}

$pytestIniPath = Join-Path $targetRoot "pytest.ini"
$pytestIni = [System.IO.File]::ReadAllText($pytestIniPath)
$pytestIni = [regex]::Replace(
    $pytestIni,
    '(?m)^    (?:Icat|Restful|Provision|Unicase): cases merged from [^\r\n]+\r?\n',
    ""
)
$markerLines = @(
    "    Icat: cases merged from Icat.py",
    "    Restful: cases merged from Restful.py",
    "    Provision: cases merged from Provision.py",
    "    Unicase: cases merged from Unicase.py"
)
$pytestIni = $pytestIni.TrimEnd() + "`r`n" + ($markerLines -join "`r`n") + "`r`n"
[System.IO.File]::WriteAllText($pytestIniPath, $pytestIni, $utf8NoBom)

$requirements = @(
    "pytest", "pytest-assume", "pytest-asyncio", "pytest-html", "pytest-rerunfailures",
    "selenium", "PyAutoGUI", "python-dateutil", "requests", "pandas", "openpyxl",
    "paramiko", "pyserial", "telnetlib3", "deepdiff", "Pillow"
)
[System.IO.File]::WriteAllText(
    (Join-Path $targetRoot "requirements.txt"),
    ($requirements -join "`r`n") + "`r`n",
    $utf8NoBom
)

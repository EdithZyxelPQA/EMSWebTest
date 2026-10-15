# EMS1-4538 portSpeedSelection

## Purpose

Verify EMS Port Speed selection can be applied for supported uplink and GE ports, and verify the final device configuration by SSH.

## Preconditions

- EMS URL, DUT IP, login account, and password are read from `environment_parameter.json`.
- The DUT type must contain `NeoX` or `IES`.
- `CARDINFO` must include the supported card information:
  - NeoX NNI: card key/type contains `NXC`.
  - IES GENNI: card key/type contains `MSC`.
  - NeoX GE: `CARDINFO` port type contains `Ethernet Access` or card key/type contains `NXA`.
  - IES GE: card key/type contains `GLC`.

## Test Steps

1. Login to EMS Web.
2. Enter `Provision / Configuration`.
3. Select the DUT from the Configuration device tree.
4. If DUT type contains `NeoX`, open `Port / NNI`; if DUT type contains `IES`, open `Port / GENNI`.
5. Select the slot and port from `CARDINFO.NXC.port_id` or `CARDINFO.MSC.port_id`.
6. Record the original Speed value before changing it.
7. Read every available option from the Speed dropdown.
8. If the card type is `NXC` or `NXA`, confirm the Speed dropdown contains the `Detect` option.
9. Select each Speed option one by one and click `Apply`.
10. Confirm the EMS message is `Success`.
11. Verify by SSH:
   - NeoX: `show interface nni <port_id> config`
   - IES: `show interface genni <port_id> config`
12. Confirm the CLI Speed field matches the Speed option applied on EMS.
13. Restore the original Speed value and verify it by SSH.
14. Open `Port / GE`.
15. Select each supported GE card port from `CARDINFO`.
    - NeoX uses Ethernet Access/NXA card ports because the GE page does not list the NXC network slot.
    - IES uses GLC card ports.
16. Record the original Speed value before changing it.
17. Read every available option from the Speed dropdown.
18. If the card type is `NXC` or `NXA`, confirm the Speed dropdown contains the `Detect` option.
19. Select each Speed option one by one and click `Apply`.
20. Confirm the EMS message is `Success`.
21. Verify by SSH:
   - `show interface ge <slot_id>-<port_id> config`
22. Confirm the CLI Speed field matches the Speed option applied on EMS.
23. Restore the original Speed value and verify it by SSH.

## Expected Result

`[EMS1-4538][portSpeedSelection] Result passed`

All available Speed options on supported NNI/GENNI and GE ports can be applied successfully from EMS, NXC/NXA speed dropdowns include `Detect`, the device CLI config shows the same speed setting, and each tested port is restored to its original Speed value after the test.

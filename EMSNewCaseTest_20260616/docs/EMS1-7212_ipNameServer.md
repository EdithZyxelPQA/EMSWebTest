# EMS1-7212 ipNameServer

## Scope

This case verifies IP Name Server configuration from EMS Web for NeoX devices only.

## Test Data

- Invalid special-character value: `@#$%.abc`
- Invalid IP-format value: `999.999.999.999`
- Valid first name server: `8.8.8.8`
- Valid second name server: `168.95.1.1`

## Steps

1. Read EMS and DUT information from `environment_parameter.json`.
2. Skip this case if the DUT type is not NeoX.
3. SSH to the DUT and run `configure`, `no ip nameserver 1`, and `no ip nameserver 2`.
4. This pre-clean is a temporary workaround for a current DUT bug. Remove this workaround after the DUT bug is fixed.
5. Login to EMS Web.
6. Go to `Provision / Configuration`.
7. Select the DUT under test.
8. Open `System / IP Name Server`.
9. Set the first IP Name Server to `@#$%.abc` and the second IP Name Server to `999.999.999.999`.
10. Apply the configuration.
11. Verify EMS rejects the configuration and `show ip nameserver` does not contain either invalid value.
12. Set the first IP Name Server to `8.8.8.8` and keep the second IP Name Server as `999.999.999.999`.
13. Apply the configuration.
14. Verify EMS still rejects the configuration and `show ip nameserver` does not contain `999.999.999.999`.
15. Set the second IP Name Server to `168.95.1.1`.
16. Apply the configuration.
17. Verify EMS reports `Success`.
18. SSH to the DUT and run `show ip nameserver`.
19. Verify the output contains `8.8.8.8` and `168.95.1.1`.
20. SSH to the DUT and run `configure`, `no ip nameserver 1`, and `no ip nameserver 2`.
21. This post-clean is a temporary workaround for the same current DUT bug. Remove this workaround after the DUT bug is fixed.

## Expected Result

`[EMS1-7212][ipNameServer] Result passed`

The invalid values are rejected, and the valid values are applied to the DUT.

## Cleanup

Due to a current DUT bug, this case cleans IP Name Server settings at the end:

```text
configure
no ip nameserver 1
no ip nameserver 2
```

Remove this cleanup after the DUT bug is fixed.
